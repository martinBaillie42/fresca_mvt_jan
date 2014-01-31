# Create your views here.

import httplib2
from mvt_admin.decorators import rewrite_response

# from fresca_mvt_jan import settings
# from httpproxy.decorators import normalize_request, rewrite_response
from django.http import HttpResponse



def index(request):

    proxy_form = u'http://%s' % ('www.cathkidston.com')
    conn = httplib2.Http()
    url = request.path

    # url_ending = '%s?%s' % (url, request.GET.urlencode())
    # url = proxy_form % url_ending

    response, content = conn.request(url, proxy_form, request.method)

    return HttpResponse(content, status=int(response['status']), mimetype=response['content-type'])

index = rewrite_response(index)