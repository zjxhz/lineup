import logging

from django.http import HttpResponse
from django.http.response import HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView
from lineup.models import Line, Ticket

from lineup.util import RequestHandler, check_signature, http_post


# Get an instance of a logger
logger = logging.getLogger(__name__)

def wechat(request):
    if request.method == 'GET':
        logger.info("get request: %s" % request.GET)
        if not check_signature(request.GET):
            return HttpResponseForbidden("Forbidden")
        echostr = request.GET.get('echostr')
        if echostr:
            return HttpResponse(echostr)
    if request.method == 'POST':
        body = request.body
        logger.info("post body: %s" % body)
        handler = RequestHandler()
        result = handler.handle(body)
        http_post('message/custom/send', result)
        return HttpResponse(result)

def test(request):
    if request.method == 'GET':
        print request.GET
    if request.method == 'POST':
        print request.body
    return HttpResponse('OK')


class WaiterAdminView(TemplateView):
    template_name = 'waiter_admin.html'

    def get_context_data(self, **kwargs):
        context = super(WaiterAdminView, self).get_context_data(**kwargs)
        context['lines'] = Line.objects.all()
        return context

@require_POST
def next_user_avaliable(request, line_id):
    line = Line.objects.get(pk=line_id)
    tickets = Ticket.objects.filter(line=line)[:1]
    if tickets:
        tickets[0].delete()
    next_user_no = line.next_user_no()
    return HttpResponse(content=next_user_no)

@require_POST
def get_next_no(request, line_id):
    line = Line.objects.get(pk=line_id)
    ticket = Ticket(line=line)
    ticket.save()
    return HttpResponse(content=ticket.ticket_no)