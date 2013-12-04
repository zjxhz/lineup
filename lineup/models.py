# coding=utf-8
'''
Created on Dec 2, 2013

@author: wayne
'''
from datetime import datetime

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.db import models

from lineup.exceptions import AlreadyJoinedException

current_ticket_no = 1

class TableType():
    Two = 1
    Four = 2
    Eight = 3
    Vip = 4
    
TABLE_TYPES = (
      (TableType.Two, u'二人桌'),
      (TableType.Four, u'四人桌'),
      (TableType.Eight, u'八人桌'),
      (TableType.Vip, u'包厢'),
) 

class Line(models.Model):
    table_type = models.SmallIntegerField(u'桌子', null=True, blank=True, choices=TABLE_TYPES)
    
    def __unicode__(self):
        return TABLE_TYPES[self.table_type - 1][1]

class Ticket(models.Model):
    ticket_no = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    line = models.ForeignKey(Line)
    time = models.DateTimeField(default=datetime.now())
    
    def __unicode__(self):
        return u"等待号：%d，用户：%s，桌子：%s，时间：%s " % (self.ticket_no, self.user, self.line, self.time)

                
class User(AbstractUser):
    name = models.CharField(u'昵称', max_length=30, null=True, blank=False)
    open_id = models.CharField(u'OpenID', max_length=128, null=True, blank=True )
    tickets = models.ManyToManyField(Line, null=True, related_name="users", through=Ticket)
    
    def wait_for_table(self, table_type):
        if self.tickets.count() > 0:
            # TODO 指出已经排了哪个队，以及是否支持重新排队？
            raise AlreadyJoinedException(u'对不起，您已经在排队，一个小时内不能重复排队')
        global current_ticket_no
        line = Line.objects.get_or_create(table_type=table_type)[0]
        ticket = Ticket(ticket_no=current_ticket_no, user=self, line=line)
        current_ticket_no += 1
        ticket.save()
        return u'您的排队号是「%d」' % ticket.ticket_no

    def cancel_ticket(self):
        ticket = self.ticket()
        if ticket:
            ticket.delete()
            return u'已取消排队'
        else:
            return u'您还未开始排队'

    def ticket(self):
        tickets = Ticket.objects.filter(user=self)
        if tickets.count() > 0:
            return tickets[0]
        
    def where(self):
        ticket = self.ticket()
        if ticket: 
            earlier_tickets = Ticket.objects.filter(ticket_no__lt = ticket.ticket_no).filter(line=ticket.line)
            return u'您前面还有%d人' % earlier_tickets.count()
        return u'您还没有开始排队'
        
def current_tickets_for(table_type):
    return Ticket.objects.filter(line__table_type=table_type).order_by("ticket_no")
    
def current_tickets():
    info = ''
    for table_type in TABLE_TYPES:
        tickets = current_tickets_for(table_type[0])
        if not tickets:
            info = info + u'「%s」：没有人在排队\n' % table_type[1]
        else:
            info = info + u'「%s」：当前到号%s，共有%d人在排队\n' % (table_type[1], tickets[0].ticket_no, len(tickets))
    return info        

def reset_tickets():
    Ticket.objects.all().delete()
    global current_ticket_no
    current_ticket_no = 1
    
admin.site.register(User)