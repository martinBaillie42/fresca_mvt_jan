# import json

from django.core import serializers
import json


__author__ = 'Martin Martin'
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from mvt_admin.models import Variant, Element, Declaration



@dajaxice_register
def multiply(request):
    dajax = Dajax()
    result = 'baa'
    dajax.assign('#id_number', 'value', str(result))
    return dajax.json()

@dajaxice_register
def variant_css(request):
    dajax = Dajax()
    this_variant = 1
    # all_elements = serializers.serialize('json', Element.objects.filter(variant=this_variant))
    all_declarations = serializers.serialize('json', Declaration.objects.filter(element__variant__id=this_variant),
                                             fields=('element', 'property', 'value'), use_natural_keys=True)

    dajax.add_data(json.loads(all_declarations), 'print_ajax')
    return dajax.json()
    # return json.dump(all_declarations)




    # dajax = Dajax()
    # e_key = Element.objects.get(variant_id=1)
    # e = serializers.serialize('json', Element.objects.filter(variant=1))
    # # d = Declaration.objects.filter(element_id=e.id)
    # d = serializers.serialize('json', Declaration.objects.filter(element=e_key.id), fields=('element', 'property', 'value'))
    # # json.dumps
    # data =
    # dajax.add_data(data, 'print_ajax')
    # # dajax.assign('#vjq_display', 'innerHTML', d)
    # return dajax.json()




