import datetime
import random
import string

from GEN import GEN_Constants as constants


def get_percent(a, b, can_exceed_100=False, decimal_c = 1):
    percent = 0
    if a>0 and b>0:
        percent = b/(a/100)
    if (can_exceed_100 == False) and percent >100:
        percent = 100

    percent = round(percent, 1)

    return percent


class dict_01(dict):

    # __init__ function
    def __init__(self):
        self = dict()

    # Function to add key:value
    def add(self, key, value):
        self[key] = value

def MergeDict(dict1, dict2):
    (dict2.update(dict1))
    return dict2


def get_post_form_data(request):
    form_data  = dict_01()

    # form_data = {"CMN_CommunicationVirtualModel__slug":"TEST","CMN_CommunicationVirtualModel__id":"TEST",  "CMN_CommunicationPhysicalModel__pincode":"601201", "CMN_CommunicationPhysicalModel__slug":"601201"}
    if request.method == "POST":
        if not bool(request.POST.items()):
            for key, value in request.POST.items():
                print(key,value)
                form_data.add(key,value)
                # print("not post req 12")
        elif request.data:
            # for key, value in request.data:
            #     print(key,value)
            #     form_data.add(key,value)
            # print("not post req 13")
            form_data =  request.data
            # print("not post req 1")
    # form_data = {"vendor_slug":"bhjiokhj", "material_slug" : "SKM69U9B" }
    # print("p_req_form_Data")

    # print("req_items")
    # print(request.POST.items())
    form_data_a = form_data.copy()
    # print(form_data_a)

    return form_data_a

def get_dict_param_val(key, dict_r, data_type):
    if key in dict_r:
        return dict_r[key]
    else:
        if data_type == constants.DT_OBJ:
            dict_aa = dict_01()
            return dict_aa
        else:
            return constants.NO_VALUE_STR_DEFAULT

def check_if_key_exist(dict01, key):
    if key in dict01:
        return True
    else:
        return False

def check_if_dict_empty(dict_rec):
    dict_aa = dict_01()
    dict_aa = dict_rec.copy()
    is_empty = True
    for key in dict01:
        is_empty = False
        break
    return is_empty

def get_display_date_time(date_time):
     return date_time.strftime('%H:%M %p, %d %b %Y')

def get_display_time(date_time):
     return date_time.strftime('%H:%M %p')

def get_display_date(date_time):
     return date_time.strftime('%d %b %Y')

def get_time_set(now):

    dict = dict_01()

    now = datetime.datetime.now()

    dict[constants.CAL_DATE] = now.day
    dict[constants.CAL_DAY] = now.day
    dict[constants.CAL_MON] = now.month
    dict[constants.CAL_HOUR] = now.hour
    dict[constants.CAL_MIN] = now.minute
    dict[constants.CAL_SEC] = now.second
    dict[constants.CAL_YEAR] = now.year

    return dict



def random_string_generator(size=8, chars=string.ascii_uppercase +string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
