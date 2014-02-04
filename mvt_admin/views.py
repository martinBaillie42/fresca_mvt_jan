# Create your views here.
import httplib2
from django.http import HttpResponse
# from fresca_mvt_jan import settings

def index(request):
    proxy_form = u'http://%s' % ('www.cathkidston.com')
    conn = httplib2.Http()

    response, content = conn.request(proxy_form, request.method)

    return HttpResponse(content, status=int(response['status']), mimetype=response['content-type'])