import re
from math import ceil
from bs4 import BeautifulSoup as BS

TEXT_LIMIT  = 512

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
              
def paginate(result, page, per_page):
  '''
  Bewerte, ob result paginiert werden muss und paginiere
  '''
  nop     = len(result)
  if nop > per_page:
    offset  = (page-1)*per_page
    result  = result[offset:offset+per_page]
    pagination = Pagination(page, per_page, nop)
  else:
    pagination = None
  return result, pagination

def get_pagination_queue(result, per_page):
  '''
  Das Template erwartet eine queue, aus der es mit jedem more-klick
  weitere per_page items darstellt.
  '''
  nop     = len(result)
  if nop > per_page:
    pages   = int(ceil( nop / float(per_page) ))
    pagination_queue = range( 2, pages + 1 )
  else:
    pagination_queue = list()
  return pagination_queue

def format_author( author ):
  '''
  Erzeuge Reihenfolge Vorname Name
  '''
  pat = re.compile(r'(.*?),(.*?)(\(.*?\))?$')
  res = pat.match(author)
  if res:
    name, forename,role = res.groups()
    return "%s %s %s" % (forename.strip(),name.strip(),role if role else '')  
  else:
    return author 

def is_list( author ):
  return isinstance( author, list )

def is_short( content ):
  text = BS( content ).get_text()[:TEXT_LIMIT]
  return len(text) < TEXT_LIMIT

def shorten( content ):
  text = BS( content ).get_text()[:TEXT_LIMIT]
  text, s, t = text.rpartition(' ')
  return text
  
def print_atts( args ):
  out = ''
  for kv in args.items():
    out+=' %s="%s"' % kv
    return out

