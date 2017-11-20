# -*- coding: utf-8 -*-
import traceback
from app import app, db
from app.model import Book
from datetime import datetime

session = None
engine = db.get_engine(app)
conn=engine.connect()
stmnt = db.text("select pk, atom_elements from (select pk, atom_elements, tsv_index from books, plainto_tsquery(:x) as q where (tsv_index @@ q) ) as t order by ts_rank_cd (t.tsv_index, plainto_tsquery(:x)) desc")
stmnt_sug = db.text("select pk, atom_elements from (select pk, atom_elements, tsv_index from books, to_tsquery(:x||':*') as q where (tsv_index @@ q) ) as t order by ts_rank_cd (t.tsv_index, plainto_tsquery(:x||':*')) desc")

class Catalog():

  def __init__( self ):
    if not session:
      _init_session()
    # Sachgebiete finden und sortieren
    sg = []
    for v in entries:
      for w in v['Sachgruppen']:
        sg.append(w.strip())
    sg = list(set(sg))
    sg.sort()
    self.sachgebiete = sg
    # Autoren finden und sortieren
    au = []
    for v in entries:
      if isinstance( v['authors'], list ):
        for w in v['authors']:
          au.append(w)
      else:
        au.append( v['authors'] )
    au = list(set(au))
    au.sort()
    self.autoren = au
    # Schlagwörter finden und sortieren
    sw = []
    swe = filter(lambda e:e.get(u'Schlagwörter'), entries)
    [[ sw.append(w) for w in e.get(u'Schlagwörter') ]  for e in swe]
    sw = list( set( sw ) )
    sw.sort()
    self.schlagworte = sw
    self.katalogisiert = filter(lambda e:e.get(u'Schlagwörter'), entries)
    # buecher nach Autoren sortieren
    self.buecher = entries
    self.buecher.sort(key = lambda e:e['authors'])
    
  def search( self, query, stmnt = stmnt ):
    res = conn.execute(stmnt, x = query ).fetchall()
    j    = app.json_decoder()
    res = [( pk, j.decode(e) ) for pk, e in res]
    for pk, e in res: e.update( pk = pk )
    return [e for pk, e in res]

  def get_suggestions( self, query ):
    if len(query.split()) > 1:
      q = ''
      for w in query.split(): q += w+' & '
      query = q.strip(' & ')
    return [( e.get('pk'),'%s: %s' % ( e.get('authors')[0], e.get('title') )) for e in self.search( query, stmnt = stmnt_sug )]

  def get_schlagwort( self, name ):
    return filter( lambda e:name in e.get(u'Schlagwörter'), self.katalogisiert ) 
    
  def get_sachgebiet( self, name ):
    return filter( lambda e:name in e['Sachgruppen'], self.buecher ) 
    
  def get_autor( self, name ):
    return filter( lambda e: name in e['authors'], self.buecher ) 
    
  def get_all( self ):
    return self.buecher

  def get_all_newer( self, y,m,d ):
    tm = datetime(y,m,d).toordinal()
    return filter( lambda entry: entry['ctime'].toordinal() >= tm, self.buecher )

  def get_book( self, pk ):
    book = session.query(Book.book_file,Book.mimetype).filter_by(pk=pk).first()
    return book

  def get_atom( self, pk ):
    book = session.query(Book.atom_elements,Book.time_added).filter_by(pk=pk).first()
    return book

  def get_img( self, pk ):
    img = session.query(Book.cover_img).filter_by(pk=pk).first()
    return img
  
  def update( self, pk, **book ):
    res = session.query(Book).filter_by(pk=pk).update( book, synchronize_session=False )
    session.flush()
    session.commit()
    return res
  
  def update_atom_elements( self, pk, atts ):
    entry = session.query(Book.atom_elements).filter_by(pk=pk).first().atom_elements
    entry.update(**atts)
    try:
      res = session.query(Book).filter_by(pk=pk).update( {Book.atom_elements:entry}, synchronize_session=False )
      session.flush()
      session.commit()
    except:
      print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
      traceback.print_exc()
      print "Es ist ein Fehler aufgetreten.\n"
    return res
    
  
def _init_session():
  global session, entries
  session = db.session
  result=session.query(Book.pk,Book.atom_elements,Book.time_added).all()
  entries = []
  for k, v, tm in result:
    v.update( pk = k, ctime=tm)
    entries.append(v)

