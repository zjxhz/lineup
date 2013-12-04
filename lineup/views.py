import logging

from django.http import HttpResponse
from django.http.response import HttpResponseForbidden

from lineup.util import RequestHandler, check_signature


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
        return HttpResponse(result)
