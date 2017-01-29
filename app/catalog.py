# -*- coding: utf-8 -*-

import os.path as p, re
from app import g

entries = g.entries

from math import ceil


class Pagination(object):

  def __init__(self, page, per_page, total_count):
    self.page = page
    self.per_page = per_page
    self.total_count = total_count

  @property
  def pages(self):
    return int(ceil(self.total_count / float(self.per_page)))

  @property
  def has_prev(self):
    return self.page > 1

  @property
  def has_next(self):
    return self.page < self.pages

  def iter_pages(self, left_edge=2, left_current=2,
                 right_current=5, right_edge=2):
    last = 0
    for num in xrange(1, self.pages + 1):
      if num <= left_edge or \
       (num > self.page - left_current - 1 and \
        num < self.page + right_current) or \
       num > self.pages - right_edge:
        if last + 1 != num:
          yield None
        yield num
        last = num
              
class Catalog():

  def __init__( self ):
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
    return filter( lambda e: self._is_author( name, e['authors']), self.buecher ) 
    
  def _is_author( self, name, author ):
    print name, unicode(author)
    if isinstance( author, list ):
      return name in author
    else:
      return name==author
    
  def get_all( self ):
    return self.buecher
  
def paginate(result, page, per_page):
  '''
  Bewerte, ob result paginierte werden muss und paginiere
  '''
  nop     = len(result)
  if nop > per_page:
    offset  = (page-1)*per_page
    result  = result[offset:offset+per_page]
    pagination = Pagination(page, per_page, nop)
  else:
    pagination = None
  return result, pagination

def format_author( author ):
  '''
  Erzeuge Reihenfolge Vorname Name
  '''
  pat = re.compile(r'(.*?),(.*?)(\(.*?\))?$')
  def arrange( s ):
    res = pat.match(s)
    if res:
      name, forename,role = res.groups()
      return "%s %s %s" % (forename.strip(),name.strip(),role if role else '')  
    else:
      return s 
  return arrange(author)

