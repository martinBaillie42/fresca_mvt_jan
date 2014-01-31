__author__ = 'Martin Martin'
from django.core.urlresolvers import reverse
import re
REWRITE_REGEX = re.compile(r'((?:src|action|href)=["\'])/')

def rewrite_response(fn):
    """
    Rewrites the response to fix references to resources loaded from HTML
    files (images, etc.).
    """
    def decorate(request, *args, **kwargs):
        response = fn(request, *args, **kwargs)
        proxy_root = reverse('mvt_admin.views.index',
            kwargs={'url': ''}
        )
        response.content = REWRITE_REGEX.sub(r'\1%s' % proxy_root, response.content)
        return response

    return decorate