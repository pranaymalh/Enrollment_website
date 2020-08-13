import os

class Config(object):
	SECRET_KEY=os.environ.get("Secret_Key") or b'r\xc9h\x96o\x1bnI}^iD"\xee\xc0H'
	MONGODB_SETTINGS={'db':'Enrollment'}