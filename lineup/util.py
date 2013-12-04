
# coding=utf-8
from datetime import datetime
import json
import logging
import urllib2
from xml.etree.ElementTree import fromstring

from django.conf import settings
import requests

from lineup.exceptions import AlreadyJoinedException
from lineup.menu import Menu
from lineup.models import current_tickets, TableType, User, reset_tickets


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
        if event_key == Menu.KEY_WAIT_FOR_TABLE_TWO:
            return self.hanlde_wait_request(TableType.Two)
        if event_key == Menu.KEY_WAIT_FOR_TABLE_FOUR:
            return self.hanlde_wait_request(TableType.Four)
        if event_key == Menu.KEY_WAIT_FOR_TABLE_EIGHT:
            return self.hanlde_wait_request(TableType.Eight)
        if event_key == Menu.KEY_WAIT_FOR_TABLE_VIP:
            return self.hanlde_wait_request(TableType.Vip)
        if event_key == Menu.KEY_CANCEL_MY_TICKET:
            return self.handle_cancel_ticket()
        if event_key == Menu.KEY_RESET_TICKETS:
            return self.handle_reset_tickets()
        
        return self.response("unknown command")
    
    def hanlde_wait_request(self, table_type):
        user = self.get_user()
        try:
            ticket_no_info = user.wait_for_table(table_type)
            return self.response(u'%s，%s' % (ticket_no_info,user.where()) )
        except AlreadyJoinedException as e:
            return self.response(unicode(e))
        except Exception as e:
            return self.response(u'发生未知错误')
    
    def get_user(self):
        user = User.objects.filter(open_id = self.fromuser)
        if not user:
            user = User.objects.create_user(self.fromuser)
            user.open_id = self.fromuser
            user.name = self.fromuser
            user.save()
        else:
            user = user[0]
        return user
    
    def handle_cancel_ticket(self):
        return self.response(self.get_user().cancel_ticket())
    
    def handle_reset_tickets(self):
        reset_tickets()
        return self.response(u'所有排队信息已经清空')
    
    def response(self, content):
        result = {"touser":self.fromuser, "msgtype":"text", "text":{"content":content}}
        return json.dumps(result,ensure_ascii=False)
    
def http_get(path):
    path='%s%s' % (settings.WECHAT_API_PATH, path)
    req=urllib2.Request(path)
    page=urllib2.urlopen(req).read()
    print page
    return page

def http_post(path, data):
    fetch_access_token()
    path='%s%s?access_token=%s' % (settings.WECHAT_API_PATH, path, settings.WECHAT_ACCESS_TOKEN)
    logger.debug(u"posting to %s with data:\n%s" % (path, data))
    r = requests.post(path, data=data.encode('utf-8'), headers={'content-type': 'application/json; charset=utf-8', })
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
