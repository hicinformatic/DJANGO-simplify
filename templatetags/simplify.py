from django import template
from django.templatetags.static import static
from django.utils.html import format_html
from django.db.models.fields import NOT_PROVIDED
from django.core.exceptions import FieldDoesNotExist

import re
numeric_test = re.compile("^\d+$")
register = template.Library()

@register.filter(name='boolean_icon')
def boolean_icon(field_val):
    svg = {True: 'yes', False: 'no', None: 'unknown', '': 'unknown' }
    return format_html('<img src="{}" alt="{}" />', static('admin/img/icon-{}.svg'.format(svg[field_val])), field_val) if field_val in svg else field_val

@register.simple_tag(name='getattribute_field')
def getattribute_field(instance, field_name, attribute, boolean_img=True):
    try:
        field = instance._meta.get_field(field_name)
        if field and hasattr(field, attribute):
            attr = getattr(field, attribute)
            if attribute == 'verbose_name':
                return attr.title() 
            return attr if attr is not NOT_PROVIDED else boolean_icon(None)
    except FieldDoesNotExist:
        if attribute == 'verbose_name':
            return field_name
        return getattribute(instance, field_name)
    return boolean_icon(None) if boolean_img else None

@register.simple_tag(name='getattribute')
def getattribute(obj, attribute, boolean_img=True):
    if hasattr(obj, str(attribute)):
        return getattr(obj, attribute)() if callable(getattr(obj, attribute)) else getattr(obj, attribute)
    elif hasattr(obj, 'has_key') and obj.has_key(attribute):
        return obj[attribute]
    elif numeric_test.match(str(attribute)) and len(obj) > int(attribute):
        return obj[int(attribute)]
    return boolean_icon(None) if boolean_img else None

@register.simple_tag(name='getrelation', takes_context=True)
def getrelation(context, obj, attribute):
    fields = context['fields_relation'][attribute]
    if hasattr(obj, '%s_set' % attribute):
        relations = getattr(obj, '%s_set' % attribute).all()
    else:
        relations = getattr(obj, attribute).all()
    size = len(fields) * relations.count()
    return {'fields': fields, 'relations': relations, 'size': size }