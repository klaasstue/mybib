#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path as p, datetime as d, json
from time import time
from flask import url_for, render_template, request, make_response
from humanfriendly import format_size
from app import app, authDB 
from catalog import Catalog
from utils import *

app.jinja_env.globals['format_size']=format_size
app.jinja_env.globals['format_author']=format_author

def url_for_other_page(page):
  "Seiten_URL für pagination"
  args = request.view_args.copy()
  args['page'] = page
  term = request.args.get('q')
  if term: args['q'] = term
  return url_for(request.endpoint, **args)

app.jinja_env.globals['url_for_other_page'] = url_for_other_page
app.jinja_env.globals['is_list']=is_list
app.jinja_env.globals['is_short']=is_short
app.jinja_env.globals['shorten']=shorten
app.jinja_env.globals['print_atts']=print_atts
cat = Catalog()
PER_PAGE    = 12

def now():
  return d.datetime.now() - d.timedelta(days=45)
  
@app.route('/', defaults={'page': 1})
@app.route('/<int:page>')
@authDB.requires_auth
def home( page ):
  '''
  Die Einstiegsseite ganz unstrukturiert
  '''
#TODO: Einstiegseite mit letzter oder zufälliger Buchauswahl 
  result  = cat.get_all()
  result, pagination = paginate( result , page, PER_PAGE )
  response = render_template('template.tpl',
      template = "gallery.tpl",
      topic = u"Meine kleine Bücherei",
      pagination  = pagination,
      entries     = result,
      topics      = cat.sachgebiete
      )
  return response

@app.route('/neu',defaults=dict(y=now().year,m=now().month,d=now().day,page=1))
@app.route('/neu/<int:y>/<int:m>/<int:d>/<int:page>')
@authDB.requires_auth
def get_latest(y,m,d,page):
  "Die neuesten Zugänge"
  result = cat.get_all_newer(y,m,d)
  result, pagination = paginate( result , page, PER_PAGE )
  response = render_template('template.tpl',
      template = "gallery.tpl",
      pagination = pagination,
      entries = result,
      topics  = cat.sachgebiete
      )
  return response
  
@app.route('/sachgebiet/<topic>/', defaults={'page': 1})
@app.route('/sachgebiet/<topic>/<int:page>')
@authDB.requires_auth
def get_topic( topic, page ):
  '''
  Alle Bücher eines Sachgebiets nach Rubriken
  '''
  "Jedes label braucht ne Nummer und ggf. ne pagination"
  i=0;
  labels = cat.get_sachgebiet_sortiert(topic).get('labels')
  for label in labels:
    items = cat.get_rubrik( topic, label.get('label') )
    pagq = get_pagination_queue( items, PER_PAGE )
    items, pagination = paginate( items, page, PER_PAGE )
    label.update( ind = i, pagination = [], pagination_queue = pagq, items = items )
    i+=1
  response = render_template('template.tpl',
      template = "panel.tpl",
      topic = topic,
      labels = labels,
      page_queues = [label.get('pagination_queue') for label in labels],
      topics  = cat.sachgebiete
      )
  return response

@app.route('/json/sachgebiet/<topic>/', defaults={'page': 1})
@app.route('/json/sachgebiet/<topic>/<page>')
@authDB.requires_auth
def get_label( topic, page ):
  '''
  Alle Bücher einer Rubrik eines Sachgebiets als JSON
  '''
  label = request.args.get('q')
  app.logger.debug('label ist ' + label)
  result  = cat.get_rubrik(topic,label)
  result, pagination = paginate( result , int(page), PER_PAGE )
  result = [
    dict(
      book  = url_for('download', filename = e.get('file'), bookId = e.get('pk')),
      image = url_for('download', filename = e.get('path'), imgId = e.get('pk')),
      size  = format_size( e.get('size') )
    ) for e in result
  ]
  response = json.dumps( result )
  return response

@app.route('/json/books/<bookId>')
@authDB.requires_auth
def get_book( bookId ):
  "Eine Detailseite"
  item = cat.get_book_md( int(bookId) )
  detail = dict(
      title = item.get( 'title'),
      summary = item.get('summary'),
      authors = [ (url_for('get_author', author = a), format_author(a)) for a in item.get('authors')],
      content = item.get('content'),
      book  = url_for('download', filename = item.get('file'), bookId = item.get('pk')),
      image = url_for('download', filename = item.get('path'), imgId = item.get('pk')),
      size  = format_size( item.get('size') )
  )
  return json.dumps( detail )

@app.route('/suggest/')
@authDB.requires_auth
def suggest(  ):
  '''
  Ein JSON mit suggestions, und zwar 
  '''
  term = request.args.get('q')
  result  = cat.get_suggestions(term)
  response = [(key,txt) for key, txt in result]
  return json.dumps( response )

@app.route('/schlagworte/')
@authDB.requires_auth
def schlagworte(  ):
  '''
  Ein JSON mit suggestions, und zwar 
  '''
  term = request.args.get('q')
  response  = cat.get_schlagworte(term)
  return json.dumps( response )

@app.route('/search/', defaults={'page': 1})
@app.route('/search/<int:page>')
@authDB.requires_auth
def search( page ):
  '''
  Allgemeine Textsuche
  '''
  term = request.args.get('q')
  result  = cat.search(term)
  result, pagination = paginate( result , page, PER_PAGE )
  response = render_template('template.tpl',
      template = "gallery.tpl",
      pagination = pagination,
      entries = result,
      topics  = cat.sachgebiete
      )
  return response

@app.route('/by_author/<author>/', defaults={'page': 1})
@app.route('/by_author/<author>/<int:page>')
@authDB.requires_auth
def get_author( author, page ):
  '''
  Alle Bücher eines Autors
  '''
  result  = cat.get_autor(author)
  result, pagination = paginate( result , page, PER_PAGE )
  response = render_template('template.tpl',
       template = "gallery.tpl",
      pagination = pagination,
      entries = result,
      authors  = cat.autoren
      )
  return response

@app.route('/res/<path>')
@authDB.requires_auth
def static_proxy(path):
  '''
  Alles unterhalb template_ressources
  '''
  # send_static_file will guess the correct MIME type
  app.logger.debug(u"%s %s -> %s" % (time(), request.path, u"Anfrage erhalten!"))
  return app.send_static_file( path )

@app.route('/covers/<path:filename>')
@app.route('/books/<bookId>/<path:filename>')
@authDB.requires_auth
def download( filename, bookId=None ):
  "Die Buch-Cover oder Bücher"
  app.logger.debug(u"%s %s -> %s" % (time(), request.path, u"Anfrage erhalten!"))
  if bookId:
    pk = bookId
    result, mimetype = cat.get_book(pk)
    response = make_response( result )
    response.mimetype = mimetype
  else:
    pk = request.args.get('imgId')
    result = cat.get_img(pk)
    response = make_response( result )
    response.mimetype = 'JPEG image data, JFIF standard 1.01'
  return response

#TODO  
@app.route('/sachgebiet')
@authDB.requires_auth
def get_sachgebiete():
  result = cat.sachgebiete

#TODO  
@app.route('/autoren')
@authDB.requires_auth
def get_autoren():
  result = cat.autoren
  
#TODO
def make_ODPS_Fields():
  pass

#TODO
@app.route('/katalog')
@authDB.requires_auth
def opds_entry():
  content = dict(
    urn = 'Entry',
    links = [dict( rel = 'self', href = url_for('opds_entry'))],
    entries = [
      dict(
        urn = 'Sachgebiete',
        title = 'Sachgebiete',
        summary = u'Die Katalogisierung der Deutschen Nationalbibliothek wird übernommen',
        links = [ dict( type = 'application/atom+xml', href = url_for('get_sachgebiete'))]
      ),
      dict(
        urn = 'Autoren',
        title = 'Autoren',
        summary = u'Die Katalogisierung der Deutschen Nationalbibliothek wird übernommen',
        links = [ dict( type = 'application/atom+xml', href = url_for('get_autoren'))]
      )
    ]
  )
  return render_template('atom.tpl', **content)
