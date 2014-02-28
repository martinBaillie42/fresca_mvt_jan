__author__ = 'Martin Martin'
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register


@dajaxice_register
def multiply(request):
    dajax = Dajax()
    result = 'aaa'
    dajax.assign('#id_number', 'value', str(result))
    return dajax.json()


