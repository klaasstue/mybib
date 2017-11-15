#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################################################
#
################################################################################
import uuid, os
from Crypto.Cipher import AES
from binascii import hexlify, unhexlify
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSON
from app import app,db

cipher = AES.new( unhexlify( os.environ.get('BIBLIO_NUMBER') ) )

def decrypt(data):
    return cipher.decrypt(unhexlify(data)).rstrip()

def encrypt(data):
    data = data + (" " * (16 - (len(data) % 16)))
    return hexlify(cipher.encrypt(data))

class EncLargeBinary(db.TypeDecorator):
	impl = db.LargeBinary
	
	def process_bind_param( self, value, dialect ):
		return encrypt( value )
		
	def process_result_value( self, value, dialect ):
		return decrypt( value )
		
class Book(db.Model):
  """
  This model stores the book file.

  """

  __tablename__   = 'books'

  pk              = db.Column( db.Integer, primary_key=True )
  mimetype        = db.Column( db.String(200), nullable=True )
  book_file       = db.Column( EncLargeBinary() )
  time_added      = db.Column( db.DateTime(timezone=True), server_default=func.now() )
  cover_img       = db.Column( db.LargeBinary() )
  atom_elements   = db.Column( JSON )

#  file_sha256sum  = db.Column( db.String(64), unique=True )
  
#  tags = TaggableManager(blank=True)
#  a_id = UUIDField('atom:id')
#  a_status = models.ForeignKey(Status, blank=False, null=False,
#                               default=settings.DEFAULT_BOOK_STATUS)
#  a_title = models.CharField('atom:title', max_length=200)
#  a_author = models.CharField('atom:author', max_length=200)
#  a_updated = models.DateTimeField('atom:updated', auto_now=True)
#  a_summary = models.TextField('atom:summary', blank=True)
#  a_category = models.CharField('atom:category', max_length=200, blank=True)
#  a_rights = models.CharField('atom:rights', max_length=200, blank=True)
#  dc_language = models.ForeignKey(Language, blank=True, null=True)
#  dc_publisher = models.CharField('dc:publisher', max_length=200, blank=True)
#  dc_issued = models.CharField('dc:issued', max_length=100, blank=True)
#  dc_identifier = models.CharField('dc:identifier', max_length=50, \
#  help_text='Use ISBN for this', blank=True)

  def __init__( self, book_file, cover_img, mimetype, atom_elements ):
    self.book_file      = book_file
    self.cover_img      = cover_img
    self.mimetype       = mimetype
    self.atom_elements  = atom_elements

  def __repr__(self):
    return '<isbn:{}, book {}>'.formatself.atom_elements['isbn'],(self.atom_elements['title'])
