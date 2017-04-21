import re
import random
import string
import hashlib
import hmac

# this file contains functions related with validation and account security

# regular expression & validation

USER_RE = re.compile(r"^[a-zA-z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")


def valid_username(username):
    # validate username
    return USER_RE.match(username)


def valid_password(password):
    # validate password
    return PASSWORD_RE.match(password)


def valid_email(email):
    # validate email if exist
    if not email:
        return True
    else:
        return EMAIL_RE.match(email)


def verify_password(password, verify):
    # verify password matching
    return password == verify

# secret word
SECRET = 'dkssud$gktpdy.durlsms^wjdml!cjtqjsWo@qmffhrmdlqslek.'
# security related user ID part


def hash_str(s):
    # create hash for input with SECRET
    return hmac.new(SECRET, s).hexdigest()


def make_secure_val(val):
    # create secure value with user id and hash separate with '|'
    return "%s|%s" % (val, hash_str(val))


def check_secure_val(secure_val):
    # check and return user id
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val

# security related user password part


def make_salt():
    # create salt with 5 random characters
    return ''.join(random.choice(string.letters) for x in xrange(5))


def make_pw_hash(name, pw, salt=None):
    # create password hash with user id, pw, and salt
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return "%s,%s" % (salt, h)


def valid_pw(name, pw, h):
    # validate password and return boolean
    salt = h.split(',')[0]
    return h == make_pw_hash(name, pw, salt)
