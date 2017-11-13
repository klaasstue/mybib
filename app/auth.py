#!/usr/bin/python
# -*- coding: utf-8 -*-

from functools import wraps
from flask import request
from utilities import authdigest

class FlaskRealmDigestDB(authdigest.RealmDigestDB):
    def requires_auth(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not self.isAuthenticated(request):
                return self.challenge()

            return f(*args, **kwargs)

        return decorated
