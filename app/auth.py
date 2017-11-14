#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from functools import wraps
import Crypto.PublicKey.RSA as RSA
import Crypto.Hash.MD5 as MD5
from binascii import a2b_hex as decode
from flask import request
from utilities import authdigest

MSG_VERIFICATION_FAILURE = "Die Signaturprüfung ist fehlgeschlagen. Sind die Nutzerdaten manipuliert?"


def load_user_data( filename, keyfile ):
    with open(keyfile) as f:
        pubkey = RSA.importKey( f.read() )

    with open( filename ) as f:
        out = decode( f.read() )

    user_data, more_bytes = out[:-308], out[-308:]
    signature = (long(more_bytes),)
    checksum = MD5.new( user_data ).hexdigest()
    assert pubkey.verify( checksum, signature ), MSG_VERIFICATION_FAILURE
    return json.loads('{"%s"}'%user_data )
            

class FlaskRealmDigestDB(authdigest.RealmDigestDB):
    def requires_auth(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not self.isAuthenticated(request):
                return self.challenge()

            return f(*args, **kwargs)

        return decorated
