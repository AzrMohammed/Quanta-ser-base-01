# =====================
# Request Handler - Support Modules
# =====================

# from support_generic import support_serializer, support_db, common_methods


# =====================
# Python Imports - Generic
# =====================
from DbUtils import support_serializer, support_db


def validate_save_instance(current_process_model, current_process_model_data):
    proceed_current_process_model, serializer_current_process_model = validate_serializer_data_set(current_process_model, current_process_model_data)
    if proceed_current_process_model:
        proceed_current_process_model, serializer_current_process_model = save_update_serializer(current_process_model, current_process_model_data)

    return proceed_current_process_model, serializer_current_process_model


def save_update_serializer(base_model, dataset):

    # serializer_data = support_db.createUpdateInstance(dataset, base_model, support_serializer.getGenericSerializer(base_model))

    is_valid, serializer_data = validate_serializer(base_model, dataset)

    if is_valid:
        save_response = serializer_data.save()
        # id = save_response.slug
        id = save_response.id

        response_s = {}
        # response_s["id"] = id
        response_s["id"] = id
        data_c = serializer_data.data
        data_c_2 = data_c.copy()
        response_s["data"] = data_c
        return True, response_s
    else:
        return False, serializer_data.errors

def validate_serializer(base_model, dataset):

    serializer_data = support_db.createUpdateInstance(dataset, base_model, support_serializer.getGenericSerializer(base_model))

    is_valid = False

    if serializer_data.is_valid():
        is_valid = True

    return is_valid, serializer_data


def validate_field_data(data_set, field_set):
    return "aaa"


#
# def save_update_serializer(base_model, dataset):
#
#     # serializer_data = support_db.createUpdateInstance(dataset, base_model, support_serializer.getGenericSerializer(base_model))
#
#     is_valid, serializer_data = validate_serializer(base_model, dataset)
#
#     if is_valid:
#
#         save_response = serializer_data.save()
#         id = save_response.slug
#         slug = save_response.slug
#
#         response_s = common_methods.dict_01()
#         response_s["id"] = id
#         response_s["slug"] = slug
#         data_c = serializer_data.data
#         data_c_2 = data_c.copy()
#         response_s["data"] = data_c
#
#         return response_s
#     else:
#         return serializer_data.errors

# validate form data
def validate_serializer(base_model, dataset):

    serializer_data = support_db.createUpdateInstance(dataset, base_model, support_serializer.getGenericSerializer(base_model))

    is_valid = False

    if serializer_data.is_valid():
        is_valid = True

    return is_valid, serializer_data

def validate_serializer_data_set(base_model, dataset):

    # print("recdddataset")
    # print(dataset)


    serializer_data = support_db.UpdateInstance(dataset, base_model, support_serializer.getGenericSerializer(base_model))

    is_valid = False

    if serializer_data.is_valid():
        is_valid = True

    return is_valid, serializer_data
