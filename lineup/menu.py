# coding=utf-8
class Menu(object):
    KEY_CURRENT_TICKETS = "KEY_CURRENT_TICKETS"
    KEY_WAIT_FOR_TABLE_TWO = "KEY_WAIT_FOR_TABLE_TWO"
    KEY_WAIT_FOR_TABLE_FOUR = "KEY_WAIT_FOR_TABLE_FOUR"
    KEY_WAIT_FOR_TABLE_EIGHT = "KEY_WAIT_FOR_TABLE_EIGHT"
    KEY_WAIT_FOR_TABLE_VIP = "KEY_WAIT_FOR_TABLE_VIP"
    KEY_CANCEL_MY_TICKET = "KEY_CANCEL_MY_TICKET"
    KEY_RESET_TICKETS = "KEY_RESET_TICKETS"
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
           },
           {
                "name": u"其他", 
                "sub_button": [
                {
                    "type": "click", 
                    "name": u"取消排队", 
                    "key": self.KEY_CANCEL_MY_TICKET,
                }, 
                {
                    "type": "click", 
                    "name": u"清空所有队伍", 
                    "key": self.KEY_RESET_TICKETS,
                }, 
            ]
        }]
        }
        return menu