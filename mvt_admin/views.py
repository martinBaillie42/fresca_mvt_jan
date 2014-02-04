# Create your views here.
import httplib2
from django.http import HttpResponse
from decorators import rewrite_response
# from fresca_mvt_jan import settings

def index(request):
    url = request.GET.get('redirecturi')
    # proxy_form = u'http://%s' % ('www.cathkidston.com')
    conn = httplib2.Http()

    response, content = conn.request(url, request.method)

    return HttpResponse(content, status=int(response['status']), mimetype=response['content-type'])

index = rewrite_response(index)