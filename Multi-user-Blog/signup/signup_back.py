import re
import random
import string
import hashlib
import hmac

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def valid_username(username):
    return USER_RE.match(username)

def valid_password(password):
    return PASSWORD_RE.match(password)

def valid_email(email):
    if not email:
        return True
    else:
        return EMAIL_RE.match(email)

def verify_password(password, verify):
    # if password == verify:
    #     return True
    # else:
    #     return False
    return password == verify

def hash_str(s):
    return hmac.new(SECRET, s).hexdigest()

def make_secure_val(val):
    return "%s|%s" % (val, hash_str(val))

def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val

SECRET = "oiahsf.wqefhh8qwy~ehrkfji$^asndf"

def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))

def make_pw_hash(name, pw, salt =None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s|%s' % (h, salt)

def valid_pw(name, pw, h):
    salt = h.split('|')[1]
    return h == make_pw_hash(name, pw, salt)
