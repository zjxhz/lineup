from django.http import HttpResponse
from django.http.response import HttpResponseForbidden
from lineup import util


def wechat(request):
    if request.method == 'GET':
        if not util.check_signature(request.GET):
            return HttpResponseForbidden("Forbidden")
        return HttpResponse(request.GET.get('echostr'))
