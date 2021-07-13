


MOD_DT_SLUG =  ("MOD_DT_SLUG", 8, "Slug")
MOD_DT_EMAIL = ("MOD_DT_EMAIL", 30, "Email Address")
MOD_DT_NAME = ("MOD_DT_NAME", 30, "Name")
MOD_DT_TEXT = ("MOD_DT_TEXT", 100, "Text")
MOD_DT_BOOL = ("MOD_DT_BOOL", 1, "Select")
MOD_DT_TEXTAREA_01 = ("MOD_DT_TEXTAREA_01", 150, "Text")
MOD_DT_TEXTAREA_02 = ("MOD_DT_TEXTAREA_02", 250, "Text")
MOD_DT_PHONE = ("MOD_DT_PHONE", 10, "Phone Number")
MOD_DT_PINCODE = ("MOD_DT_PINCODE", 6, "Pincode")
MOD_DT_LAT_LONG = ("MOD_DT_LAT_LONG", 25, "Latitude/Longitude")
MOD_DT_CHOICE_LIMITED = ("MOD_DT_CHOICE_LIMITED", 250, "Choice")
MOD_DT_CHOICE_UNLIMITED = ("MOD_DT_CHOICE_UNLIMITED", 250, "Search Here")
MOD_DT_NUMBER = ("MOD_DT_NUMBER", 10, "Value")



MOD_DT = [
        (MOD_DT_SLUG[0], MOD_DT_SLUG),
        (MOD_DT_EMAIL[0], MOD_DT_EMAIL),
        (MOD_DT_NAME[0], MOD_DT_NAME),
        (MOD_DT_TEXT[0], MOD_DT_TEXT),
        (MOD_DT_BOOL[0], MOD_DT_BOOL),
        (MOD_DT_TEXTAREA_01[0], MOD_DT_TEXTAREA_01),
        (MOD_DT_TEXTAREA_02[0], MOD_DT_TEXTAREA_02),
        (MOD_DT_PHONE[0], MOD_DT_PHONE),
        (MOD_DT_PINCODE[0], MOD_DT_PINCODE),
        (MOD_DT_LAT_LONG[0], MOD_DT_LAT_LONG),
        (MOD_DT_CHOICE_LIMITED[0], MOD_DT_CHOICE_LIMITED),
        (MOD_DT_CHOICE_UNLIMITED[0], MOD_DT_CHOICE_UNLIMITED),
        (MOD_DT_NUMBER[0], MOD_DT_NUMBER),
     ]

MOD_DT_DIC = dict(MOD_DT)



#
# class dict_dt(dict):
#
#     # __init__ function
#     def __init__(self):
#         self = dict()
#
#     # Function to add key:value
#     def add(self, key, value):
#         self[key] = value
#
#
# MOD_DT_SET = dict_dt()
# MOD_DT_SET.add(model_name, field_dic)


#
# class modal_definition():

def getDataType(MOD_DT_TYPE):
    return MOD_DT_TYPE[0];

def getMaxLength(MOD_DT_TYPE):
    return MOD_DT_TYPE[1];

def getLabel(MOD_DT_TYPE):
    return MOD_DT_TYPE[2];
