from django.template import Context
from django.template.loader import get_template
from django import template

register = template.Library()

@register.filter
def bootstrap(element):
    markup_classes = {'label': '', 'value': '', 'single_value': ''}
    return render(element, markup_classes)


@register.filter
def bootstrap_inline(element):
    markup_classes = {'label': 'sr-only', 'value': '', 'single_value': ''}
    return render(element, markup_classes)


@register.filter
def bootstrap_horizontal(element, label_cols=""):
    if len(label_cols) == 0:
        label_cols = 'col-sm-2 col-lg-2'

    d = label_cols.split(",")
    if len(d) > 1:
        label_cols = d[0]
        total = int(d[1])
    else:
        total = 12

    markup_classes = {'label': label_cols,
            'value': '',
            'single_value': ''}

    for cl in label_cols.split(' '):
        splited_class = cl.split('-')

        try:
            value_nb_cols = int(splited_class[-1])
        except ValueError:
            value_nb_cols = total

        if value_nb_cols >= total:
            splited_class[-1] = total
        else:
            offset_class = cl.split('-')
            offset_class[-1] = 'offset-' + str(value_nb_cols)
            splited_class[-1] = str(total - value_nb_cols)
            markup_classes['single_value'] += ' ' + '-'.join(offset_class)
            markup_classes['single_value'] += ' ' + '-'.join(splited_class)

        markup_classes['value'] += ' ' + '-'.join(splited_class) + ' text-left'

    return render(element, markup_classes)


def add_input_classes(field):
    if not is_checkbox(field) and not is_multiple_checkbox(field) and not is_radio(field):
        field_classes = field.field.widget.attrs.get('class', '')
        field_classes += ' form-control'
        field.field.widget.attrs['class'] = field_classes

def add_placeholder(field):
    if not is_checkbox(field) and not is_multiple_checkbox(field) and not is_radio(field):
        if not field.field.widget.attrs.has_key('placeholder'):
            if hasattr(field.field, 'help_text'):
                field.field.widget.attrs['placeholder'] = field.field.help_text
		field.field.help_text = ''

def render(element, markup_classes):
    element_type = element.__class__.__name__.lower()

    if element_type == 'boundfield':
        add_input_classes(element)
        template = get_template("bootstrapform/field.html")
        context = Context({'field': element, 'classes': markup_classes})
    else:
        has_management = getattr(element, 'management_form', None)
        if has_management:
            for form in element.forms:
                for field in form.visible_fields():
                    add_input_classes(field)

            template = get_template("bootstrapform/formset.html")
            context = Context({'formset': element, 'classes': markup_classes})
        else:
            for field in element.visible_fields():
                add_input_classes(field)
                add_placeholder(field)

            template = get_template("bootstrapform/form.html")
            context = Context({'form': element, 'classes': markup_classes})

    return template.render(context)


@register.filter
def is_checkbox(field):
    return field.field.widget.__class__.__name__.lower() == "checkboxinput"

@register.filter
def is_multiple_checkbox(field):
    return field.field.widget.__class__.__name__.lower() == "checkboxselectmultiple"

@register.filter
def is_radio(field):
    return field.field.widget.__class__.__name__.lower() == "radioselect"
