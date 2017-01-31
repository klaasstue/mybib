#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path as p
from flask import url_for, render_template, request, make_response
from humanfriendly import format_size
from app import app 
from catalog import Catalog
from utils import *

app.jinja_env.globals['format_size']=format_size
app.jinja_env.globals['format_author']=format_author
def url_for_other_page(page):
  args = request.view_args.copy()
  args['page'] = page
  return url_for(request.endpoint, **args)

app.jinja_env.globals['url_for_other_page'] = url_for_other_page
app.jinja_env.globals['is_list']=is_list
app.jinja_env.globals['is_short']=is_short
app.jinja_env.globals['shorten']=shorten

cat = Catalog()
PER_PAGE    = 12
 
@app.route('/', defaults={'page': 1})
@app.route('/<int:page>')
def home( page ):
  '''
  Die Einstiegsseite a la ARD & ZDF. Mit alphabetischer und thematischer Navigation
  '''
  result  = cat.get_all()
  result, pagination = paginate( result , page, PER_PAGE )
  response = render_template('template.tpl',
      pagination  = pagination,
      entries     = result,
      topics      = cat.sachgebiete
      )
  return response

@app.route('/katalog/<topic>/', defaults={'page': 1})
@app.route('/katalog/<topic>/<int:page>')
def get_topic( topic, page ):
  '''
  DNB Sortierung, auch wenn die etwas seltsam ist
  '''
  result  = cat.get_sachgebiet(topic)
  result, pagination = paginate( result , page, PER_PAGE )
  response = render_template('template.tpl',
      pagination = pagination,
      entries = result,
      topics  = cat.sachgebiete
      )
  return response

@app.route('/by_author/<author>/', defaults={'page': 1})
@app.route('/by_author/<author>/<int:page>')
def get_author( author, page ):
  '''
  DNB Sortierung, auch wenn die etwas seltsam ist
  '''
  result  = cat.get_autor(author)
  result, pagination = paginate( result , page, PER_PAGE )
  response = render_template('template.tpl',
      pagination = pagination,
      entries = result,
      authors  = cat.autoren
      )
  return response

@app.route('/res/<path>')
def static_proxy(path):
  '''
  Alles unterhalb template_ressources
  '''
  # send_static_file will guess the correct MIME type
  return app.send_static_file( path )

@app.route('/covers/<path:filename>')
@app.route('/books/<path:filename>')
def download( filename ):
  if request.args.has_key('bookId'):
    pk = request.args.get('bookId')
    result, mimetype = cat.get_book(pk)
    response = make_response( result )
    response.mimetype = mimetype
  else:
    pk = request.args.get('imgId')
    result = cat.get_img(pk)
    response = make_response( result )
  return response
  
#TODO
def make_ODPS_Fields():
  pass

