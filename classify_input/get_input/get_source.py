# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.getdefaultencoding = 'utf-8'
import os, time
from os import path, stat
import datetime
from mimetypes import MimeTypes
from pwd import getpwuid
import textract
from unidecode import unidecode_expect_nonascii
import re
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
class GetText(object):
    def __init__(self, object):
        self.time_stamp = self.timestamp()
        self.source = object
        self.classification = None
        self.full_text = None
        self.classification = self.type_determination(self.source)

    def type_determination(self, source):
        if os.path.isfile(self.source):
            classification = "file"
            self.file_handler(source)
        elif isinstance(self.source, str):
            classification = "plaintext"
            self.raw_text = str(source)
        elif isinstance(self.source, unicode):
            classification = "unicode"
        else:
            classification = None
        return classification
    def timestamp(self, fmt='%Y-%m-%d %H:%M'):
        """
        Set the date and time a document was uploaded.

        Record the datetime a document is uploaded or
        a paste is submitted.

        returns:
           Data and Time in US format, separated by space.
        """
        return datetime.datetime.now().strftime(fmt)
    def file_handler(self, source):
        self.abs_path = os.path.abspath(source)
        self.file_size = os.path.getsize(self.source)
        self.filename = os.path.basename(self.source)
        self.mime = MimeTypes()
        self.guessed_file_type = self.mime.guess_type(self.source)
        self.file_type = self.guessed_file_type[0]
        self.last_file_mod = time.ctime(os.path.getctime(self.abs_path))
        self.file_owner = getpwuid(os.stat(self.abs_path).st_uid).pw_name
        self.file_extension = os.path.splitext(self.abs_path)[1]
        self.file_access = os.access(self.abs_path, os.R_OK)
        self.read_file(source)
    def read_file(self, source):
        if self.file_access:
            if self.file_type == \
                        "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                self.raw_text = textract.process(source)
            elif self.file_type == "text/plain":
                self.raw_text = open(self.abs_path).read()
            elif self.file_type == 'application/pdf':
                self.raw_text = self.pdf_to_text(source)
                #self.raw_text = textract.process(source)
                #self.raw_text = re.sub(r'''([!.\?\!"':])^0013''', r'\1', self.raw_text.rstrip())
                #.raw_text_u = unicode(self.raw_text, 'utf-8')

                #self.raw_text_u = re.sub('\n\n', 'ORANGE_CLOWN ', self.raw_text_u)
                #self.raw_text_u = self.raw_text_u.replace('\n', ' ')
                #.raw_text_u = re.sub('ORANGE_CLOWN ', '\n\n', self.raw_text_u)
                #self.text_clean = unidecode_expect_nonascii(self.text_clean)
                #self.text_clean_u = unicode(self.text_clean, 'utf-8', 'ignore')



                #self.txt_clean = unicode(self.raw_text, 'utf-8')
                #try:
                #    self.txt_clean = re.sub(pattern=r'(\S)[ \t]*(?:\r\n|\n)[ \t]*(\S)', repl='\1 \2', string=self.raw_text, flags=re.MULTILINE)
                #except:
                #    print("no txt_clean")
                #new_text = re.sub(pattern=r'(.+?)(?:\r\n|\n)(.+[.!?]+[\s|$])', repl='\g<1>\g<2>', string=self.raw_text, flags=re.MULTILINE)
            else:
                print "unknown filetype"
            self.utxt = unicode(self.raw_text, 'utf-8')
    def pdf_to_text(self, source):
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        fp = file(source, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos=set()

        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
            interpreter.process_page(page)

        text = retstr.getvalue()

        fp.close()
        device.close()
        retstr.close()
        newtext = re.sub(r'''([!.\?\!"':])^0013''', r'\1', text.rstrip())
        newtext = newtext.replace('\n\n', 'ORANGECLOWNS ')
        newtext = newtext.replace('\n', ' ')
        newtext = newtext.replace('ORANGECLOWNS ', '\n\n')



        return newtext
