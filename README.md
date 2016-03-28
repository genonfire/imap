# imap
simple script downloading attachment via imap
using (http://www.voidynullness.net/blog/2013/07/25/gmail-email-with-python-via-imap/)

# HowTo
edit configuration then run python imap.py

EMAIL_SERVER = "imap.gmail.com"
EMAIL_ACCOUNT = "@gmail.com"
EMAIL_PASSWORD = ""
EMAIL_FOLDER = "INBOX"
FILE_PATH = "./files"
TIMESTAMP_PATH = "./timestamp.log"
POLLING_SEC = 600 # 10 min

M = imaplib.IMAP4_SSL(EMAIL_SERVER) // SSL server
M = imaplib.IMAP4(EMAIL_SERVER) // non-SSL

# TODO
handle multiple attachments
