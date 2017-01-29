#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################################################
#
# Der Flask-Server kann mit folgenden Optionen gestratet
# werden. 
# 
# Usage: python server.py [-p n] [--options 'key1=value1,...'] [-d] [-o]
#
#  -p,  --port n      n ist Port des Servers, default ist 8000
#       --options kv  Weitere Flask-Server-Optionen als kommaseparierte kv-Paare
#  -d,  --debug       Schaltet debug mode ein
#  -o,  --open        Öffnet den Server für LAN und ggf. WAN
#
################################################################################
from werkzeug.contrib.fixers import ProxyFix
from flask import request
from app import app
app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__=='__main__':
  '''
  Appserver starten
  '''
  # configure Flask logging
  from logging import FileHandler, DEBUG, ERROR
  logger = FileHandler('error.log')
  app.logger.setLevel(ERROR)
  app.logger.addHandler(logger)
    
  # allow for server options
  import argparse
    
  server = argparse.ArgumentParser(description="Startet den Appserver")
  server.add_argument("-p", "--port", help="Port des Servers", type=int, default=8000)
  server.add_argument("--options", help="Weitere Flask-Server-Optionen als kommaseparierte key=value-Paare", type=str, default=None)
  server.add_argument("-d", "--debug", help="Schaltet debug mode ein", action='store_true')
  server.add_argument("-o", "--open", help="Öffnet den Server für LAN und ggf. WAN", action='store_true')
  opts = server.parse_args()
  server_opts = dict(debug=opts.debug,port=opts.port)
  port = opts.port
  if opts.debug:
    app.logger.setLevel( DEBUG )
  if opts.open: 
    server_opts.update(host='0.0.0.0')
  if opts.options:
    key_value_pattern = re.compile('[a-zA-Z0-9_]*=.*')
    kvs=opts.options.split(',')
    for kv in kvs:
      if key_value_pattern.match( kv ):
        key, value = kv.split('=')
        if value.isdigit(): value = int( value )
        if value=='True': value = True 
        if value=='False': value = False 
        server_opts.update({key:value})
      else:
        app.logger.error('%s will be ignored, because it is not a key value pair!',kv)

  # log Flask events
  from time import asctime
  app.logger.debug(u"Flask server started " + asctime())
  @app.after_request
  def write_access_log(response):
      app.logger.debug(u"%s %s -> %s" % (asctime(), request.path, response.status_code))
      return response

  app.run( **server_opts )

  
