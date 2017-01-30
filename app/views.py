#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path as p
from flask import url_for, send_from_directory, render_template, request, redirect
from humanfriendly import format_size
from bs4 import BeautifulSoup as BS
from app import app 
from catalog import Catalog, paginate, format_author

app.jinja_env.globals['format_size']=format_size
app.jinja_env.globals['format_author']=format_author
cat = Catalog()
PER_PAGE = 12
 
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
  if request.args:
    fname = request.args.get('bookId')
  else:
    fname = 'cover.jpg'
  path = p.join(filename,fname)
  return send_from_directory( app.config['BIBLIOTHEK'], path )

def url_for_other_page(page):
  args = request.view_args.copy()
  args['page'] = page
  return url_for(request.endpoint, **args)
app.jinja_env.globals['url_for_other_page'] = url_for_other_page

def is_list( author ):
  return isinstance( author, list )
app.jinja_env.globals['is_list']=is_list

def shorten( content ):
  text = BS( content ).get_text()[:250]
  text, s, t = text.rpartition(' ')
  return text
app.jinja_env.globals['shorten']=shorten

