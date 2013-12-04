
from datetime import datetime
import hashlib
import httplib
import json
import logging
import urllib
import urllib2
from xml.etree.ElementTree import fromstring, SubElement, dump, Element, \
    tostring
import xml.etree.ElementTree

from django.conf import settings
import requests

from lineup.menu import Menu
from lineup.models import current_tickets


# Get an instance of a logger
logger = logging.getLogger(__name__)
def check_signature(data):
    try:
        return True
#         signature = data.get('signature')
#         timestamp = data.get('timestamp')
#         nonce = data.get('nonce')
#         
#         if not signature or not timestamp or not nonce:
#             return False
#         
#         my_hash = hashlib.sha1(settings.SECRET_KEY+timestamp+nonce)
#         return signature == my_hash 
    except Exception:
        return False

class RequestHandler(object):
    def handle(self, xml):
        root = fromstring(xml)
        self.devid = root.find('ToUserName').text
        self.fromuser = root.find('FromUserName').text
        eventkey = root.find('EventKey').text
        if eventkey:
            return self.handel_event(eventkey)
            
    def handel_event(self, event_key):
        
        if event_key == Menu.KEY_CURRENT_TICKETS:
            return self.response(current_tickets())

        return self.response("unknown command")
    
    def response(self, content):
        result = {"touser":self.fromuser, "msgtype":"text", "text":{"content":content}}
        return json.dumps(result)
#         xml = Element('xml')
#         fromuser = SubElement(xml, 'FromUserName')
#         fromuser.text = self.devid
#         touser = SubElement(xml, 'ToUserName')
#         touser.text = self.fromuser
#         createtime = SubElement(xml, 'CreateTime')
#         createtime.text = str(int((datetime.now() - datetime(1970, 1, 1)).total_seconds()))
#         msgtype = SubElement(xml, 'MsgType')
#         msgtype.text = 'text'
#         content = SubElement(xml, 'Content')
#         content.text = content
#         return tostring(xml)
    
def http_get(path):
    path='%s%s' % (settings.WECHAT_API_PATH, path)
    req=urllib2.Request(path)
    page=urllib2.urlopen(req).read()
    print page
    return page

def http_post(path, data):
    fetch_access_token()
    path='%s%s?access_token=%s' % (settings.WECHAT_API_PATH, path, settings.WECHAT_ACCESS_TOKEN)
    logging.debug("posting to %s with data:\n%s" % (path, data))
    r = requests.post(path, data)
    print r.text
    return r.text
    
    
def fetch_access_token():
    now = datetime.now()
    diff = 0
    if settings.WECHAT_ACCESS_TOKEN_TIMESTAMP:
        diff = (now - settings.WECHAT_ACCESS_TOKEN_TIMESTAMP).total_seconds()
    if not settings.WECHAT_ACCESS_TOKEN or diff > 3600:
        response =  http_get("token?grant_type=client_credential&appid=%s&secret=%s" % (settings.WECHAT_APP_ID, settings.WECHAT_APP_SECRET))
        dic = json.loads(response)
        settings.WECHAT_ACCESS_TOKEN = dic['access_token']
        print 'setting access token to ', settings.WECHAT_ACCESS_TOKEN 