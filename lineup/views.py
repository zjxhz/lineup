from django.http import HttpResponse
from django.http.response import HttpResponseForbidden

from lineup import util
from lineup.util import RequestHandler


def wechat(request):
    if request.method == 'GET':
        if not util.check_signature(request.GET):
            return HttpResponseForbidden("Forbidden")
        echostr = request.GET.get('echostr')
        if echostr:
            return HttpResponse(echostr)
    if request.method == 'POST':
        body = request.body
        handler = RequestHandler()
        result = handler.handle(body)
        return HttpResponse(result)
