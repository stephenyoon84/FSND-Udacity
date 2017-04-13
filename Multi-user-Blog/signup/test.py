import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_username(username):
    return USER_RE.match(username)
def valid_password(password):
    return PASSWORD_RE.match(password)
def valid_email(email):
    return EMAIL_RE.match(email)

if valid_email('aaa@aaa'):
    print "True"
else:
    print "False"


if valid_username("St"):
    print "True"
else:
    print "False"

if valid_password("12"):
    print "True"
else:
    print "False"

def verify_password(password, verify):
    if password == verify:
        return True
    else:
        return False
# def valid_email(email):
#     if email == "":
#         return True
#     elif email != "":
#         return EMAIL_RE.match(email)
