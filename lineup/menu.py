# coding=utf-8
import json
import urllib2

from django.conf import settings

from lineup.util import http_post
from util import fetch_access_token


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
        return menu

temp='中文'
def push_menu():
    fetch_access_token()
    menu = Menu()
#     menu_str = json.dumps(menu.get_menu(), ensure_ascii=False)
    http_post('menu/create?access_token=%s' % settings.WECHAT_ACCESS_TOKEN, menu.get_menu())