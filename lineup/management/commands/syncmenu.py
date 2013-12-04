# coding=utf-8
'''
Created on Dec 4, 2013

@author: wayne
'''
from django.core.management.base import BaseCommand

from lineup.menu import Menu
from lineup.util import http_post
from django.conf import settings
import json

class Command(BaseCommand):    

    def handle(self, *args, **options):
        self.sync_menu()
    
    def sync_menu(self):
        menu = Menu()
        menu_str = json.dumps(menu.get_menu(), ensure_ascii=False)
        http_post('menu/create?access_token=%s' % settings.WECHAT_ACCESS_TOKEN, menu_str)
    