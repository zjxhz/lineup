import logging

from django.http import HttpResponse
from django.http.response import HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from lineup.util import RequestHandler, check_signature, http_post


# Get an instance of a logger
logger = logging.getLogger(__name__)

@csrf_exempt
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

@csrf_exempt
def test(request):
    if request.method == 'GET':
        print request.GET
    if request.method == 'POST':
        print request.body
    return HttpResponse('OK')