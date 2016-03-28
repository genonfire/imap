#!/usr/bin/env python
#
# Very basic example of using Python and IMAP to iterate over emails in a
# gmail folder/label.  This code is released into the public domain.
#
# RKI July 2013
# http://www.voidynullness.net/blog/2013/07/25/gmail-email-with-python-via-imap/
# 
# in case of gmail,
# would fail to login unless allow https://www.google.com/settings/security/lesssecureapps
# please check below for more 
# https://support.google.com/mail/answer/14257
#
import sys
import os
import imaplib
import getpass
import email
import email.header
import calendar
import string
import time
from datetime import date, timedelta, datetime

EMAIL_SERVER = "imap.gmail.com"
EMAIL_ACCOUNT = "@gmail.com"
EMAIL_PASSWORD = ""
EMAIL_FOLDER = "INBOX"
FILE_PATH = "./files"
TIMESTAMP_PATH = "./timestamp.log"
POLLING_SEC = 600 # 10 min

def process_mailbox(M):
    new_mail = 0;
    recover_stamp = 946706400 # Jan 1 2000
    now = datetime.now()
    now_stamp = calendar.timegm(now.utctimetuple())

    if os.path.exists(TIMESTAMP_PATH):
      fp = open(TIMESTAMP_PATH, 'r')
      recover_stamp = float(fp.read());
      fp.close()
    else:
      print "not exists %s so using default timestamp" % TIMESTAMP_PATH
    recover = datetime.utcfromtimestamp(recover_stamp)
    print "recovered time: %s" % recover

    rv, data = M.search(None, "ALL")
    if rv != 'OK':
        print "No messages found!"
        return

    for num in data[0].split():
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print "ERROR getting message", num
            return

        msg = email.message_from_string(data[0][1])
        date_tuple = email.utils.parsedate_tz(msg['Date'])
        if date_tuple:
            local_date = datetime.fromtimestamp(
                email.utils.mktime_tz(date_tuple))
            if (local_date < recover):
              continue
            else:
              decode = email.header.decode_header(msg['Subject'])[0]
              subject = unicode(decode[0])
              print '< %s > %s' % (num, subject)
              print "Local Date:", local_date.strftime("%a, %d %b %Y %H:%M:%S")
              new_mail += 1

        if msg.is_multipart():
          for part in msg.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))
            if 'attachment' in cdispo :
              print "content_type: %s" % ctype
              attachment = cdispo.split('=')
              filename = num + '_' + attachment[1].strip('"')

              if not os.path.exists(FILE_PATH):
                os.mkdir(FILE_PATH)

              fp = open(FILE_PATH+"/"+filename, 'w')
              fp.write(part.get_payload(decode=True))
              fp.close()
              print "+ saved filename: %s" % filename
              
        else:
          print 'not multiparted'

    print " %d mail downloaded at %s" % (new_mail, now)
    fp = open(TIMESTAMP_PATH, 'w')
    fp.write("%s" % now_stamp)
    fp.close()

def check_mail():
  M = imaplib.IMAP4_SSL(EMAIL_SERVER)
  # imaplib.IMAP4(EMAIL_SERVER) for non-SSL

  try:
      # rv, data = M.login(getpass.getuser(), getpass.getpass()) to get password from user input
      rv, data = M.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
  except imaplib.IMAP4.error:
      print "LOGIN FAILED!!! "
      sys.exit(1)

  print rv, data

  rv, mailboxes = M.list()
  if rv == 'OK':
      print "Mailboxes:"
      print mailboxes

  rv, data = M.select(EMAIL_FOLDER)
  if rv == 'OK':
      print "Processing mailbox...\n"
      process_mailbox(M)
      M.close()
  else:
      print "ERROR: Unable to open mailbox ", rv

  M.logout()

reload(sys)
sys.setdefaultencoding('utf8')

# recover_stamp = 946706400 # Jan 1 2000
# now = datetime.now()
# now_stamp = calendar.timegm(now.utctimetuple())
# recover = datetime.fromtimestamp(now_stamp)
# print "now : %s" % now
# print "now_stamp : %s" % now_stamp
# print "recover : %s" % recover

while(True):
  check_mail()
  time.sleep(POLLING_SEC)
