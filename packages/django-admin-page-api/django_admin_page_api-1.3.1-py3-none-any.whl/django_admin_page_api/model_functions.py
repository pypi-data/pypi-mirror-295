import os
import datetime
from django.contrib import admin
from django.db import models
from .utils import *
import enum
import json 

def get_all_models():
    return admin.site._registry.items()

def get_model_by_name(app: str, model_name: str):
    for model, adminModel in admin.site._registry.items():
        if model_name.lower() == str(model.__name__).lower():
            if app == model._meta.app_label:
                return model
            
def get_admin_model_by_name(app: str, model_name: str):
    for model, adminModel in admin.site._registry.items():
        if model_name.lower() == str(model.__name__).lower():
            if app == model._meta.app_label:
                return adminModel
            
def get_model_with_admin(app: str, model_name: str):
    return get_model_by_name(app, model_name), get_admin_model_by_name(app, model_name)

def get_fields_of_model(model):
    return [field for field in model._meta.get_fields() if field.editable]

def get_app_json(app):
    return {
        'label': app.label,
        'name': app.name,
        'verbose_name': app.verbose_name,
        'models': [model[0].__name__ for model in admin.site._registry.items() if model[0]._meta.app_label == app.label]
    }

def get_model_json(model):
    is_registered = admin.site._registry.get(model) is not None
    return {
        'model_name': model.__name__,
        'app': get_app_json(model._meta.app_config),
        'is_registered': is_registered,
        'list_display': admin.site._registry.get(model).list_display if is_registered else ['__str__'],
        'fields': [get_field_json(field) for field in get_fields_of_model(model)],
        
    }

def get_field_json(field):
    internal_type = field.get_internal_type()
    return {
        'name': field.name,
        'type': 'ImageField' if isinstance(field, models.ImageField) else field.get_internal_type(),
        'relation': {
            'is_relation': field.is_relation,
            'model': {
                'model_name': field.related_model.__name__, 
                'app_label': field.related_model._meta.app_label
            } if field.is_relation else None,
        },
        'max_length': field.max_length if internal_type == 'CharField' else None,
        'choices': dict((key, val) for key, val in field.choices) if internal_type == 'CharField' and field.choices else None,
        'null': field.null,
        'blank': field.blank if not field.is_relation else None,
        'auto_created': field.auto_created,
        'in_list_display': field.name in admin.site._registry.get(field.model).list_display,
        'decimal_places': field.decimal_places if internal_type == 'DecimalField' else None,
        'max_digits': field.max_digits if internal_type == 'DecimalField' else None,
        'unique': field.unique,
        'help_text': field.help_text,
        'default': (field.default() if callable(field.default) else field.default) if field.default != models.NOT_PROVIDED else None,
        'auto_now_add': field.auto_now_add if field.get_internal_type() in ['DateTimeField'] else False
    }


def pagination(items: list, limit: int, offset: int) -> list:
    return items[offset:limit+offset]

def serialize_field_to_json(value: any, type: str):
    if type in ['AutoField', 'BigAutoField']:
        return value
    if type in ['CharField', 'TextField']:
        return str(value)
    if type == 'BooleanField':
        return value
    if type == 'IntegerField':
        return int(value)
    if type == 'FileField':
        if not value:
            return {
                'value': False
            }
        
        return {
            'value': True,
            'name': value.name, 
            'path': value.path, 
            'size': value.size, 
            'url': value.url,
            'filename': os.path.basename(value.path),
            'extension': None if not '.' in os.path.basename(value.path) else os.path.basename(value.path).split('.')[-1]
        }

    if type in ['DateField', 'TimeField', 'DateTimeField']:
        return value
    if type in ['FloatField', 'DecimalField']:
        return float(value)
    if type in ['OneToOneField', 'ForeignKey']:
        return {
            'pk': value.pk if value is not None else None, 
            'model_name': value.__class__.__name__ if value else None, 
            'app_label': value.__class__._meta.app_label if value else None
        }
    if type in ['ManyToManyField']:
        return {
            'model_name': value.model.__name__, 
            'app_label': value.model._meta.app_label, 
            'items': [item.pk for item in value.all()]
        }
    if type == 'JSONField':
        return json.dumps(value) if value else ''
    return None

def item_to_json(item):
    return {
        '__str__': str(item),
        'pk': item.pk,
        'fields': dict((field.name, serialize_field_to_json(getattr(item, field.name), field.get_internal_type())) for field in get_fields_of_model(item.__class__))
    }
    
def set_item_field(item, field, value: any, type: str):
    if value == '\0': 
        setattr(item, field.name, None)
        return
    if type in ['CharField', 'TextField']:
        setattr(item, field.name, str(value))
    if type in ['FloatField', 'DecimalField']:
        try: setattr(item, field.name, float(value))
        except: ...
    if type in ['IntegerField']:
        try: setattr(item, field.name, int(value))
        except: ...
    if type in ['FileField']:
        setattr(item, field.name, value)
    if type in ['BooleanField']:
        setattr(item, field.name, True if value == 'true' else False if value == 'false' else None)
    if type in ['DateField', 'TimeField', 'DateTimeField']:
        if type == 'DateField':
            try:
                d = datetime.date.fromisoformat(value)
                setattr(item, field.name, d)
            except: setattr(item, field.name, None)
        elif type == 'TimeField':
            try:
                t = datetime.time.fromisoformat(value)
                setattr(item, field.name, t)
            except: setattr(item, field.name, None)
        elif type == 'DateTimeField':
            try:
                dt = datetime.datetime.fromisoformat(value)
                setattr(item, field.name, dt)
            except: setattr(item, field.name, None)
    if type in ['OneToOneField', 'ForeignKey']:
        if value: setattr(item, field.name, field.related_model.objects.filter(pk=value).first())
        else: setattr(item, field.name, None)
    if type in ['ManyToManyField']:
        try:
            keys = convert_comma_array(value)
            if len(keys): getattr(item, field.name).set(field.related_model.objects.filter(pk__in=keys))
            else: getattr(item, field.name).clear()
        except:
            ...

class UpadateException(Exception):
    ...

def update_item(model, item, post, files):

    errors = []

    for field in get_fields_of_model(model):
        try:
            if field.get_internal_type() == 'ManyToManyField':
                continue
            if field.get_internal_type() == 'FileField':
                if files.get(field.name) is None:
                    print(f"{post.get(field.name)=}")
                    if post.get(field.name) == '\x01':
                        set_item_field(item, field, None, field.get_internal_type())
                    elif not getattr(item, field.name) and field.blank:
                        set_item_field(item, field, None, field.get_internal_type())
                    elif not getattr(item, field.name):
                        raise UpadateException(f"File for '{field.name}' not sent!")
                else: set_item_field(item, field, files.get(field.name), field.get_internal_type())
            else:
                if post.get(field.name) is None and not field.blank:
                    raise UpadateException(f"Value for '{field.name}' not sent!")
                else: set_item_field(item, field, post.get(field.name), field.get_internal_type())
        except Exception as e: errors.append([field.name, repr(e)])

    try:

        if not len(errors):
            item.save()

            for field in get_fields_of_model(model):
                try:
                    if field.get_internal_type() != 'ManyToManyField':
                        continue
                    if post.get(field.name) is None and not field.blank:
                        raise UpadateException(f"Value for '{field.name}' not sent!")
                    else: set_item_field(item, field, post.get(field.name), field.get_internal_type())
                except Exception as e: errors.append([field.name, repr(e)])
            
            try: item.save()
            except Exception as e: errors.append(repr(e))

    except Exception as e: errors.append(repr(e))
    
    return item, errors  


def get_model_permission_json(admin_model, request):
    return {
        'add': admin_model.has_add_permission(request),
        'change': admin_model.has_change_permission(request),
        'delete': admin_model.has_delete_permission(request),
        'view': admin_model.has_view_permission(request),
    }
    
def add_some_json_to_model(model_json, admin_model, request, model):
    model_json['permissions'] = get_model_permission_json(admin_model, request)
    model_json['actions'] = [(action) for action in admin.site._registry.get(model).get_action_choices(request)]
    return model_json

def create_new_item(model, post, files):
    item = model()
    item, errors = update_item(model, item, post, files)
    return item, errors

class Actions(enum.Enum):
    VIEW = 'view'
    ADD = 'add'
    CHANGE = 'change'
    DELETE = 'delete'

def have_permission(request, admin_model, action):
    if not request.user.is_authenticated: return False
    if request.user.is_superuser: return True
    
    if action == Actions.VIEW:
        return admin_model.has_view_permission(request) 
    
    if action == Actions.ADD:
        return admin_model.has_add_permission(request) 
    
    if action == Actions.CHANGE:
        return admin_model.has_change_permission(request) 
    
    if action == Actions.DELETE:
        return admin_model.has_delete_permission(request) 
    
    return False