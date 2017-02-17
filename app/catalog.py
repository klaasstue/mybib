# -*- coding: utf-8 -*-
import traceback
from app import db
from app.model import Book

session = None
#session = True
#import json
#with open('data/base.json') as fd:
#  entries = json.load(fd).values()

class Catalog():

  def __init__( self ):
    if not session:
      _init_session()
    # Sachgebiete finden und sortieren
    sg = []
    for v in entries:
      for w in v['Sachgruppen']:
        sg.append(w)
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
    # buecher nach Autoren sortieren
    self.buecher = entries
    self.buecher.sort(key = lambda e:e['authors'])
  
  def get_sachgebiet( self, name ):
    return filter( lambda e:name in e['Sachgruppen'], self.buecher ) 
    
  def get_autor( self, name ):
    return filter( lambda e: name in e['authors'], self.buecher ) 
    
  def get_all( self ):
    return self.buecher
  
  def get_book( self, pk ):
    book = session.query(Book.book_file,Book.mimetype).filter_by(pk=pk).first()
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
    print entry
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
  result=session.query(Book.pk,Book.atom_elements).all()
  entries = []
  for k, v in result:
    v.update( pk = k)
    entries.append(v)


