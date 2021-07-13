import random
import string


from django.core.files.base import ContentFile
import base64

from DbUtils import db_operations_support


def random_string_generator(size=8, chars=string.ascii_uppercase +string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def random_numeric_generator(size=8, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_string_generator(Klass, key_name, new_key=None):
    if new_key is not None:
        key = new_key
    else:
        key = random_string_generator(size=8)

    # Klass = instance.__class__
    key_set = {key_name : key}

    qs_exists = Klass.objects.filter(**key_set).exists()

    if qs_exists:
        new_key = random_string_generator(size=8)
        return unique_key_generator(Klass, key_name, new_key= new_key)
    return key;

def unique_numeric_generator(Klass, key_name, new_key=None):
    if new_key is not None:
        key = new_key
    else:
        key = random_numeric_generator(size=8)

    # Klass = instance.__class__
    key_set = {key_name : key}

    qs_exists = Klass.objects.filter(**key_set).exists()

    if qs_exists:
        new_key = random_string_generator(size=8)
        return unique_key_generator(Klass, key_name, new_key= new_key)
    return key;

def unique_key_generator(Klass, key_name, new_key=None):
    if new_key is not None:
        key = new_key
    else:
        key = random_string_generator(size=8)

    # Klass = instance.__class__
    key_set = {key_name : key}

    qs_exists = Klass.objects.filter(**key_set).exists()

    if qs_exists:
        new_key = random_string_generator(size=8)
        return unique_key_generator(Klass, key_name, new_key= new_key)
    return key;


def unique_id_generator(Klass, new_id=None):
    if new_id is not None:
        id = new_id
    else:
        id = random_string_generator(size=8)

    # Klass = instance.__class__
    qs_exists = Klass.objects.filter(id= id).exists()
    if qs_exists:
        new_id = random_string_generator(size=8)
        return unique_id_generator(Klass, new_id= new_id)
    return id;

def unique_token_generator(Klass, new_token=None):

    if new_token is not None:
        token = new_token
    else:
        token = random_string_generator(size=22)

    # Klass = instance.__class__
    qs_exists = Klass.objects.filter(token= token).exists()
    if qs_exists:
        newz_id = random_string_generator(size=18)
        return unique_token_generator(Klass, new_token= new_token)
    return token;


def createUpdateInstance(data_set, model_base, serializer_base):
    # print("called create update idg ")
    if 'id' in data_set:
        # print("camesdsdfsd")
        # print(data_set["id"])
        # print(data_set)
        model_obj = model_base.objects.get(id=data_set["id"])
        serializer_obj = serializer_base(instance = model_obj, data=data_set, partial=True)
        return serializer_obj
    else:
        # print("camesdsdfsd create id")
        # id = unique_id_generator(model_base)
        # data_set["id"] = id
        serializer_obj = serializer_base(data=data_set, partial=True)
        return serializer_obj

def UpdateInstance(data_set, model_base, serializer_base):
    # print("called create update idg ")
    if 'id' in data_set:
        # print("camesdsdfsd")
        # print(data_set["id"])
        # print(data_set)
        model_obj = model_base.objects.get(id=data_set["id"])
        serializer_obj = serializer_base(instance = model_obj, data=data_set, partial=True)
        return serializer_obj
    else:
        # print("camesdsdfsd create id")
        # id = unique_id_generator(model_base)
        # data_set["id"] = id
        serializer_obj = serializer_base(data=data_set, partial=True)
        return serializer_obj



def getidFromId(model_class, id):

    material_data = model_class.objects.get(pk = id)
    return material_data.id

def getIdFromid(model_class, id):

    material_data = model_class.objects.get(id = id)
    return material_data.id

def create_update_image(model, id, column_key, image_b64):

    format, imgstr = image_b64.split(';base64,')
    ext = format.split('/')[-1]

    image_file = ContentFile(base64.b64decode(imgstr), name=str(id)+'__'+column_key+'_bi.' + ext)

    key_set = {"id":id}
    material_q = db_operations_support.get_db_object_g(model, key_set)

    dict_temp = {column_key : image_file}
    material_q.__dict__.update(dict_temp)
    # material_q.base_image = image_file
    material_q.save()
