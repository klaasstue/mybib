# -*- coding: utf-8 -*-
import traceback, os
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
      sg.append(v.get(u'panel'))
#      for w in v['Sachgruppen']:
#        sg.append(w.strip())
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
    swe = filter(lambda e:e.get(u'Schlagworte'), entries)
    [[ sw.append(w) for w in e.get(u'Schlagworte') ]  for e in swe]
    sw = list( set( sw ) )
    sw.sort()
    self.schlagworte = sw
    self.katalogisiert = filter(lambda e:e.get(u'Schlagworte'), entries)
    # buecher nach Autoren sortieren
    self.buecher = entries
    self.buecher.sort(key = lambda e:e['authors'])
    self.buecher_sortiert = strukturierte_liste
    
  def search( self, query, stmnt = stmnt_sug ):
    "Volltextsuche auf allen Textfeldern in atom-elements"
    if len(query.split()) > 1:
      q = ''
      for w in query.split():
        w = filter(lambda b: b.isalnum(),w)
        q += w + ' & '
      query = q.strip(' & ')
    res = conn.execute(stmnt, x = query ).fetchall()
    j    = app.json_decoder()
    res = [( pk, j.decode(e) ) for pk, e in res]
    for pk, e in res: e.update( pk = pk )
    return [e for pk, e in res]

  def get_suggestions( self, query ):
    "pk und Autor, Titel für die aufklappende suggestionsliste"
    return [( e.get('pk'),'%s: %s' % ( e.get('authors')[0], e.get('title') )) for e in self.search( query )]

  def get_book_md( self, pk ):
    "Gib metadaten zum Busch mit primary key pk"
    return pk_map.get(pk)
    
  def get_schlagworte( self, term ):
    return filter(lambda w: term.lower()  in w.lower(), self.schlagworte ) 
    
  def get_sachgebiet( self, name ):
#    return filter( lambda e:name in e['Sachgruppen'], self.buecher ) 
    return filter( lambda e:name in e['panel'], self.buecher ) 
    
  def get_sachgebiet_sortiert( self, name ):
    return filter(lambda e:e['panel'] == name, self.buecher_sortiert )[0]    
    
  def get_rubrik( self, name, label ):
    return filter(lambda e:e['panel'] == name and e['label'] == label, self.buecher )   
    
  def get_autor( self, name ):
    return filter( lambda e: name in e['authors'], self.buecher ) 
    
  def get_all( self ):
    return self.buecher

  def get_all_sortiert( self ):
    return self.buecher_sortiert

  def get_all_newer( self, y,m,d ):
    tm = datetime(y,m,d).toordinal()
    return filter( lambda entry: entry['ctime'].toordinal() >= tm, self.buecher )

  def get_book( self, pk ):
    book = session.query(Book.book_file,Book.mimetype).filter_by(pk=pk).first()
    return book

  def get_atom( self, pk ):
    book = session.query(Book.atom_elements,Book.time_added).filter_by(pk=pk).first()
    return book

  def get_atom_by_isbn( self, isbn ):
    book = session.query(Book.atom_elements,Book.time_added).filter(Book.atom_elements['isbn'].astext == isbn).first()
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
  
  def add_book( self, fd_book, fd_img, entry ):
    '''
    Add book where fd_book and fd_img must be file descriptor like objects or 
    binary data. Entry must be a jsonizable object, that at least must contain
    the key mimetype.
    '''
    if not isinstance(fd_book, str):
      book_binary = fd_book.read()
    else:
      book_binary = fd_book
    if not isinstance(fd_img, str):
      img_binary  = fd_img.read()
    else:
      img_binary   = fd_img
    session.add(
      Book(
        book_file       = book_binary, 
        cover_img       = img_binary, 
        mimetype      = entry['mimetype'], 
        atom_elements = entry
      )
    )
    session.flush()
    session.commit()
  
def _init_session():
  global session, entries, strukturierte_liste, pk_map, isbn_map, file_map 
  session = db.session
  result=session.query(Book.pk,Book.atom_elements,Book.time_added).all()
  entries = []
  pk_map = {}
  isbn_map = {}
  file_map = {}
  for k, v, tm in result:
    v.update( pk = k, ctime=tm)
    entries.append(v)
    pk_map[k] = v
    isbn_map[v['isbn']] = v
    file_map[v['file']] = v
  'Eine strukturieret Liste vorbereiten'
  l=list(set(['%s/%s'% (e.get('panel'),e.get('label')) for k,e,tm in result]))
  l.sort()
  ll=list(set([e.get('panel') for k,e,tm in result]))
  ll.sort()
  "Die strukturierte Liste enthält für jedes Sachgebiet eine Liste mit Unterrubriken"
  strukturierte_liste = [dict(panel=e,labels=[]) for e in ll]
  for i in l:
    for e in strukturierte_liste:
        if e.get('panel') in i:
            e.get('labels').append(dict(label=os.path.basename(i),items=[]))

