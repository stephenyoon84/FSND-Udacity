import re

EMAIL_RE = re.compile(r"^[\S]+@[\S]+..[\S]+$")

def valid_email(email):
    return EMAIL_RE.match(email)

if valid_email('aaa@aaa'):
    print "True"
else:
    print "False"
