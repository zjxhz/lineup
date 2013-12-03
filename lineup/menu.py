# coding=utf-8
import json
import urllib2
from django.conf import settings

class Menu(object):
    KEY_CURRENT_TICKETS = "KEY_CURRENT_TICKETS"
    KEY_WAIT_FOR_TABLE_TWO = "KEY_WAIT_FOR_TABLE_TWO"
    KEY_WAIT_FOR_TABLE_FOUR = "KEY_WAIT_FOR_TABLE_FOUR"
    KEY_WAIT_FOR_TABLE_EIGHT = "KEY_WAIT_FOR_TABLE_EIGHT"
    KEY_WAIT_FOR_TABLE_VIP = "KEY_WAIT_FOR_TABLE_VIP"
    def get_menu(self):
        menu = {
         "button":[
         {    
              "type":"click",
              "name":u"当前到号",
              "key": self.KEY_CURRENT_TICKETS
          },
          {
               "name":u"排队",
               "sub_button":[
               {    
                   "type":"click",
                   "name":u"二人桌",
                   "key": self.KEY_WAIT_FOR_TABLE_TWO,
                },
                {
                   "type":"click",
                   "name":u"四人桌",
                   "key": self.KEY_WAIT_FOR_TABLE_FOUR,
                },
                {
                   "type":"click",
                   "name":u"八人桌",
                   "key": self.KEY_WAIT_FOR_TABLE_EIGHT,
                },
                {
                   "type":"click",
                   "name":u"包厢",
                   "key": self.KEY_WAIT_FOR_TABLE_VIP,
                },       ]
           }]
        }
        return json.dumps(menu)


def push_menu():
    menu = Menu()
    menu_str = menu.get_menu()
    path=' https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s' % settings.WECHAT_TOKEN   #the url you want to POST to
    req=urllib2.Request(path)
    req.add_header('Content-Type', 'application/json')
    page=urllib2.urlopen(req, menu_str).read()
    print page