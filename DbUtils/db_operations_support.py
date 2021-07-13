# =====================
# DB Model support
# =====================

# =====================
# Base Import
# =====================

from django.apps import apps


# from MTL.models import MTL_SPT_MaterialPurchaseRequestCH01Model

# exact
# iexact
# contains
# icontains
# in
# gt
# gte
# lt
# lte
# startswith
# istartswith
# endswith
# iendswith
# range
# year
# month
# day
# week_day
# isnull
# search
# regex
# iregex

def get_choice_initital(model_name):
    model = get_model_class_sp(model_name)
    print("gdfgdfg model")
    print(model)
    try:
        obj = model.objects.filter(is_initial = True).first()
        return obj.slug
    except model.DoesNotExist:
        try:
            obj = model.objects.filter(is_active = True).first()
            return obj.slug
        except model.DoesNotExist:
            return None


def get_choice_final(model_name):
    model = get_model_class_sp(model_name)
    try:
        obj = model.objects.filter(is_final_successful = True).first()
        return obj.slug
    except model.DoesNotExist:
        return None

def get_choice_final_successful(model_name):
    model = get_model_class_sp(model_name)
    try:
        obj = model.objects.filter(is_final_successful = True).first()
        return obj.slug
    except model.DoesNotExist:
        return None


def get_choice_final_failure(model_name):
    model = get_model_class_sp(model_name)
    try:
        obj = model.objects.filter(is_final_failure = True).first()
        return obj.slug
    except model.DoesNotExist:
        return None

def get_choice_default(model_name):
    model = get_model_class_sp(model_name)
    try:
        obj = model.objects.filter(is_default = True).first()
        print("err tr")
        return obj.slug
    except model.DoesNotExist:
        print("err fal")
        return None

def get_db_object_by_code(model, value):

    if value is None or model is None:
        return None
    try:
        return model.objects.filter(code_enterprise = value).first()
    except model.DoesNotExist:
        return None

def get_db_object_g(model, key_set):
    try:
        return model.objects.filter(**key_set).first()
    except model.DoesNotExist:
        return None

def get_db_object_g_last(model, key_set):
    try:
        return model.objects.filter(**key_set).last()
    except model.DoesNotExist:
        return None

def get_db_object_g_list(model, key_set):
    try:
        return model.objects.filter(**key_set)
    except model.DoesNotExist:
        return None

def get_db_object(model, slug):
    try:
        return model.objects.get(pk = slug)
    except model.DoesNotExist:
        return None

def get_db_object_list(model, slug_set):
    return model.objects.filter(slug__in = slug_set)

def get_model_class_sp(app_name__model_name):
    splits = app_name__model_name.split("__")

    return get_model_class(splits[0], splits[1])

def get_model_class(app_name, model_name):
    return apps.get_model(app_name, model_name)
