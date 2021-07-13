# USER_TYPES = [
#         (USER_TYPE_SUPER_ADMIN, 'SUPER_ADMIN'),
#         (USER_TYPE_MANAGER, 'MANAGER'),
#         (USER_TYPE_CONSUMER, 'CONSUMER'),
#         (USER_TYPE_DELIVERY_AGENT, 'DELIVERY_AGENT'),
#         (USER_TYPE_BUSINESS_OWNER, 'BUSINESS_OWNER'),
#         (USER_TYPE_CUSTOMER_CARE_EXECUTIVE,'CUSTOMER_CARE')
#      ]
#
# USER_TYPES_DIC = dict(USER_TYPES)

# SERVER_PREFIX = "http://192.168.2.8:8000/"
# SERVER_PREFIX = "http://103.118.188.160:8878/"

# Enterprise | Personal | Official | SecondPerson-Agent

APP_USER_TYPE_CUSTOMER = "USR_CUSTOMER"
APP_USER_TYPE_BUSINESS_OWNER = "USR_BOWNER"
APP_USER_TYPE_BRANCH_AGENT = "USR_BAGENT"

ORDER_STATUS_INITIATED = "ORD_INITIATED"
ORDER_STATUS_AGENT_APPROVED = "ORD_APPROVED"
ORDER_STATUS_AGENT_REJECTED_NO_SLOT = "ORD_REJECTED_NO_SLOT"
ORDER_STATUS_AGENT_REJECTED_OTHERS = "ORD_REJECTED_OTHERS"
ORDER_STATUS_CANCELLED = "ORD_CANCELLED"
ORDER_STATUS_NO_SHOW = "ORD_NO_SHOW"
ORDER_STATUS_ONGOING = "ORD_ONGOING"
ORDER_STATUS_COMPLETED = "ORD_COMPLETED"


def getFcmApiKey(app_user_type):
    # hypersalon
    # if app_user_type == APP_USER_TYPE_CUSTOMER:
    #     return "AAAAz7OAjKM:APA91bGEsAA_CSXAwE0KBHx-_SUAG8Bpfj4yKAD5oBudCuD1ol9ogcjrGduByb0o7ZnVdFTYQzv342H_Rpl06N715mu4Do_7L7IXNx3wYVu_fDKI27Mkl3p0YEw0LrHj-Hpqte25Awi5"
    # elif app_user_type == APP_USER_TYPE_BRANCH_AGENT or app_user_type == APP_USER_TYPE_BUSINESS_OWNER:
    #     return "AAAAN0FaarA:APA91bFo8rvomXkSWLgAG9bzvO5HmkRP937Z8glH7YSGP50bTZoxn6nWclnGQROjG2VajXGfJDG_Tra_NBUwmTPZyA84N1lySVq0STJNx7qgYob2a3HqHbIQjl9iNnFYit47VQCkQt8H"

    # safez
    if app_user_type == APP_USER_TYPE_CUSTOMER:
        return "AAAAGOBvZ8M:APA91bFb4NF50EGwalrwgdvm__wR8cY3NIGeITqcOaAhOUqZPJf-Ge8ujkJcKVR-xAsVdXzFEOFhdvRWeiddtTC1I_14re54HgA7AxXaeg07-ftXPDfH9-Qh5YQTFbkD02xC7cV6DF2c"
    elif app_user_type == APP_USER_TYPE_BRANCH_AGENT or app_user_type == APP_USER_TYPE_BUSINESS_OWNER:
        return "AAAA5_LZ6Ac:APA91bEEIOqZsIEaOrjsKmwVxJahyIpWjj3r-Go_z-Ocn0RSOojjrhWGWCIaPJGIDejizwpW1F6Hfr3ylOKaXCME7ZMITRxP0I6Tp0p6alrhHPKw1uODa0C7a2B1q4XjjbxXkT3ubmwx"




# Communication Types
ENTERPRISE = 'ENTPRS'
PERSONAL = 'PRSNL'
OFFICIAL = 'OFICIL'
SECOND_PARTY_AGENT = 'SECPAG'

GEN_COMMUNICATION_TYPES = [
        (ENTERPRISE, 'Enterprise'),
        (PERSONAL, 'Personal'),
        (OFFICIAL, 'Official'),
        (SECOND_PARTY_AGENT, 'SecondPerson-Agent'),
     ]

GEN_COMMUNICATION_TYPES_DIC = dict(GEN_COMMUNICATION_TYPES)



# Phone | Email | Skpye
# Communication channel  Types

PHONE = 'PHN'
EMAIL = 'EML'
SKYPE = 'SKP'

GEN_COMMUNICATION_CHANNEL_TYPES = [
        (PHONE, 'PHONE'),
        (EMAIL, 'EMAIL'),
        (SKYPE, 'SKYPE'),
     ]

GEN_COMMUNICATION_CHANNEL_TYPES_DIC = dict(GEN_COMMUNICATION_CHANNEL_TYPES)





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

# DT_ = "DT_"
# ================================================
# ================================================
# ================================================
# ================================================


# SERVER_PREFIX

NO_VALUE_STR_DEFAULT = "NO_VAL"
NULL_VALUE_STR_DB = "null"
NO_VALUE_STR_DB = None
NO_VALUE_INT_DEFAULT = -101
NO_VALUE_INT_POSITIVE_DEFAULT = 10112233


MTL_ACC_TYPE_XY_UNION = "XY_UNION"
MTL_ACC_TYPE_XY_INTERSECTION = "XY_INTERSECTION"
MTL_ACC_TYPE_X_FG = "X_FG"
MTL_ACC_TYPE_X_MATERIAL = "X_MATERIAL"

product_category_tags = "Tags"
product_category_heat_transfer = "Heat Transfer"
product_category_printed_tapes = "Printed Tapes"

material_type_direct = "Direct Material"
state_definition_fg = "X_FG"

state_definition_fg_name = "Pcs"
DB_V_Action_Title_No_val = "NO_VAL"

SUGGESTION_LIST_LIMIT = 5

# Time Set
CAL_DATE = 'CAL_DATE'
CAL_DAY = 'CAL_DAY'
CAL_MON = 'CAL_MON'
CAL_HOUR = 'CAL_HOUR'
CAL_MIN = 'CAL_MIN'
CAL_SEC = 'CAL_SEC'
CAL_YEAR = 'CAL_YEAR'

DT_STR = "DT_STR"
DT_ARR = "DT_ARR"
DT_OBJ = "DT_OBJ"

BOOL_VAL_TRUE = "BOOL_VAL_TRUE"
BOOL_VAL_FALSE = "BOOL_VAL_FALSE"
BOOL_VAL_BOTH = "BOOL_VAL_BOTH"
BOOL_VAL_NOT_SET = "BOOL_VAL_NOT_SET"

VER_ANSR_BOOL_VALS = [
    (BOOL_VAL_TRUE, 'BOOL_VAL_TRUE'),
    (BOOL_VAL_FALSE, 'BOOL_VAL_FALSE'),
    (BOOL_VAL_BOTH, 'BOOL_VAL_BOTH'),
    (BOOL_VAL_NOT_SET, 'BOOL_VAL_NOT_SET'),
]

VER_ANSR_BOOL_VALS_DIC = dict(VER_ANSR_BOOL_VALS)

# USER_TYPES = [
#         (USER_TYPE_SUPER_ADMIN, 'SUPER_ADMIN'),
#         (USER_TYPE_MANAGER, 'MANAGER'),
#         (USER_TYPE_CONSUMER, 'CONSUMER'),
#         (USER_TYPE_DELIVERY_AGENT, 'DELIVERY_AGENT'),
#         (USER_TYPE_BUSINESS_OWNER, 'BUSINESS_OWNER'),
#         (USER_TYPE_CUSTOMER_CARE_EXECUTIVE,'CUSTOMER_CARE')
#      ]
#
# USER_TYPES_DIC = dict(USER_TYPES)

# Enterprise | Personal | Official | SecondPerson-Agent


ORDERS_LIST_COUNT_BUSINESS = 10

BA_ORDER_DETAIL_REQUEST_DEFAULT = "DEFAULT";
BA_ORDER_DETAIL_REQUEST_CHECKIN = "CHECKIN";
BA_ORDER_DETAIL_REQUEST_SCHEDULE = "SCHEDULE";
BA_ORDER_DETAIL_REQUEST_CHECKED_IN = "CHECKED_IN";

# Inbound | OutBound | InternalTransfer | Freeze
# Transfer Types
MIT_TRANSFER_INBOUND = 'INBD'
MIT_TRANSFER_OUTBOUND = 'OTBD'
MIT_TRANSFER_INTERNAL_TRANSFER = 'INTR'
MIT_TRANSFER_FREEZE = 'FREZ'

MIT_TRANSFER_TYPES = [
    (MIT_TRANSFER_INBOUND, 'TRANSFER_INBOUND'),
    (MIT_TRANSFER_OUTBOUND, 'TRANSFER_OUTBOUND'),
    (MIT_TRANSFER_INTERNAL_TRANSFER, 'TRANSFER_INTERNAL_TRANSFER'),
    (MIT_TRANSFER_FREEZE, 'TRANSFER_FREEZE'),
]

MIT_TRANSFER_TYPES_DIC = dict(MIT_TRANSFER_TYPES)

MIT_TRANSFER_TYPES_DIS = [
    (MIT_TRANSFER_INBOUND, 'INBOUND'),
    (MIT_TRANSFER_OUTBOUND, 'OUTBOUND'),
    (MIT_TRANSFER_INTERNAL_TRANSFER, 'INTERNAL_TRANSFER'),
    (MIT_TRANSFER_FREEZE, 'FREEZE'),
]

MIT_TRANSFER_TYPES_DIS_DIC = dict(MIT_TRANSFER_TYPES_DIS)

ENTERPRISE = 'ENTPRS'
PERSONAL = 'PRSNL'
OFFICIAL = 'OFICIL'
SECOND_PARTY_AGENT = 'SECPAG'

GEN_COMMUNICATION_TYPES = [
    (ENTERPRISE, 'Enterprise'),
    (PERSONAL, 'Personal'),
    (OFFICIAL, 'Official'),
    (SECOND_PARTY_AGENT, 'SecondPerson-Agent'),
]

GEN_COMMUNICATION_TYPES_DIC = dict(GEN_COMMUNICATION_TYPES)

# Accounting  Types
ACC_EOQ = 'ACC_EOQ'
ACC_L4L = 'ACC_L4L'
ACC_REVIEW_CONTINEOUS = 'ACC_REVIEW_CONTINEOUS'
ACC_REVIEW_PERIODIC = 'ACC_REVIEW_PERIODIC'

MTL_ACC_TYPES = [
    (ACC_EOQ, 'ACC_EOQ'),
    (ACC_L4L, 'ACC_L4L'),
    (ACC_REVIEW_CONTINEOUS, 'ACC_REVIEW_CONTINEOUS'),
    (ACC_REVIEW_PERIODIC, 'ACC_REVIEW_PERIODIC'),
]

MTL_ACC_TYPES_DIC = dict(MTL_ACC_TYPES)

# MTL Usage Types
USG_FIFO = 'USG_FIFO'
USG_LIFO = 'USG_LIFO'
USG_ANYBATCH = 'USG_ANYBATCH'

MTL_USG_TYPES = [
    (USG_FIFO, 'USG_FIFO'),
    (USG_LIFO, 'USG_LIFO'),
    (USG_ANYBATCH, 'USG_ANYBATCH'),
]

MTL_USG_TYPES_DIC = dict(MTL_USG_TYPES)

# FIFO | LIFO | AnyBatch | CustomRules
#
# EOQ | L4L | Review Contineous | Review Periodic


# Phone | Email | Skpye
# Communication channel  Types

PHONE = 'PHN'
EMAIL = 'EML'
SKYPE = 'SKP'

GEN_COMMUNICATION_CHANNEL_TYPES = [
    (PHONE, 'PHONE'),
    (EMAIL, 'EMAIL'),
    (SKYPE, 'SKYPE'),
]

GEN_COMMUNICATION_CHANNEL_TYPES_DIC = dict(GEN_COMMUNICATION_CHANNEL_TYPES)

MATERIAL_DIRECT = 'MDI'
MATERIAL_INDIRECT = 'MID'

MTL_MATERIAL_TYPE = [
    (MATERIAL_DIRECT, 'MATERIAL_DIRECT'),
    (MATERIAL_INDIRECT, 'MATERIAL_INDIRECT'),
]

MTL_MATERIAL_TYPE_DIC = dict(MTL_MATERIAL_TYPE)

MTL_MATERIAL_TYPE_DISPLAY = [
    (MATERIAL_DIRECT, 'Direct Material'),
    (MATERIAL_INDIRECT, 'Indirect Material'),
]

MTL_MATERIAL_TYPE_DISPLAY_DIC = dict(MTL_MATERIAL_TYPE_DISPLAY)

MTL_MATERIAL_USAGE_PRODUCTION = 'MUP'
MTL_MATERIAL_USAGE_MRO = 'MUM'

MTL_MATERIAL_USAGE = [
    (MTL_MATERIAL_USAGE_PRODUCTION, 'MTL_MATERIAL_USAGE_PRODUCTION'),
    (MTL_MATERIAL_USAGE_MRO, 'MTL_MATERIAL_USAGE_MRO'),
]

MTL_MATERIAL_USAGE_DIC = dict(MTL_MATERIAL_USAGE)

MTL_MATERIAL_USAGE_DIS = [
    (MTL_MATERIAL_USAGE_PRODUCTION, 'Production'),
    (MTL_MATERIAL_USAGE_MRO, 'Maintainance'),
]

MTL_MATERIAL_USAGE_DIS_DIC = dict(MTL_MATERIAL_USAGE_DIS)

# ============
# WBS_STORE_TYPE
# ============
# WBS_STORE_TYPE_RM

WBS_STORE_TYPE_RM = 'SRM'
WBS_STORE_TYPE_PRODUCTION = 'SPN'
WBS_STORE_TYPE_FG = 'SFG'

WBS_STORE_TYPE = [
    (WBS_STORE_TYPE_RM, 'WBS_STORE_TYPE_RM'),
    (WBS_STORE_TYPE_PRODUCTION, 'WBS_STORE_TYPE_PRODUCTION'),
    (WBS_STORE_TYPE_FG, 'WBS_STORE_TYPE_FG'),
]

WBS_STORE_TYPE_DIC = dict(WBS_STORE_TYPE)

WBS_STORE_TYPE_DIS = [
    (WBS_STORE_TYPE_RM, 'Raw Material'),
    (WBS_STORE_TYPE_PRODUCTION, 'Production'),
    (WBS_STORE_TYPE_FG, 'Finished Goods'),
]

WBS_STORE_TYPE_DIS_DIC = dict(WBS_STORE_TYPE_DIS)

MOD_DT_SLUG = ("MOD_DT_SLUG", 8, "Slug")
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

# DT_ = "DT_"

TRN_Material_Inbound = "MTL_TRN_INB"
TRN_Material_Stock = "MTL_TRN_STK"
TRN_Material_Request_Intitated = "MTL_TRN_RIN"
TRN_Material_Assigned = "MTL_TRN_ASD"
TRN_Material_Alloted = "MTL_TRN_ALT"
TRN_Material_Transfer_Approved = "MTL_TRN_TAP"
TRN_Material_Transfer_Initiated = "MTL_TRN_TIN"
TRN_Material_Transfer_Completed = "MTL_TRN_CMP"
TRN_Material_Rejected_and_Returned_To_Store = "MTL_TRN_RRS"
TRN_Material_Wastage = "MTL_TRN_WST"
TRN_Material_Adjusted = "MTL_TRN_ADJ"
TRN_Material_In_Production_Floor = "MTL_TRN_INP"
TRN_Material_Consumed_In_Production = "MTL_TRN_CMD"
TRN_Material_Purchase_Planning = "MTL_TRN_PPL"
TRN_Material_Purchase_Scheduled = "MTL_TRN_PSL"
TRN_Material_Production_Scheduled = "MTL_TRN_PDS"
TRN_Material_Scheduled_without_Stock = "MTL_TRN_SWS"

MTL_TRN_event_type = {
    TRN_Material_Inbound: "Material Inbound",
    TRN_Material_Stock: "Material Stock",
    TRN_Material_Request_Intitated: "Material Request Intitated",
    TRN_Material_Assigned: "Material Assigned",
    TRN_Material_Alloted: "Material Alloted",
    TRN_Material_Transfer_Approved: "Material Transfer Approved",
    TRN_Material_Transfer_Initiated: "Material Transfer Initiated",
    TRN_Material_Transfer_Completed: "Material Transfer Completed",
    TRN_Material_Rejected_and_Returned_To_Store: "Material Rejected and Returned To Store",
    TRN_Material_Wastage: "Material Wastage",
    TRN_Material_Adjusted: "Material Adjusted",
    TRN_Material_In_Production_Floor: "Material In Production Floor",
    TRN_Material_Consumed_In_Production: "Consumed in Production",
    TRN_Material_Purchase_Planning: "Purchase Planning",
    TRN_Material_Purchase_Scheduled: "Purchase Scheduled",
    TRN_Material_Production_Scheduled: "Material Production Scheduled",
    TRN_Material_Scheduled_without_Stock: "Material Scheduled without Stock"

}

PO_EVT_ORDER_IN_TRANSIT = "PR_INT"
PO_EVT_ORDER_RECEIVED = "PR_RCP"
PO_EVT_PO_RAISED_TO_VENDOR = "PR_RTV"
PO_EVT_REQUEST_APPROVED = "PR_APD"
PO_EVT_REQUEST_CREATED = "PR_CRD"
PO_EVT_REQUEST_INITIATED = "PR_INI"
PO_EVT_REQUEST_REJECTED = "PR_RJD"
PO_EVT_ORDER_RECEIVED_COMPLETE = "PR_RCC"
PO_EVT_ORDER_AMENDMENT = "PR_AMD"

PO_EVT_TYPE = {
    PO_EVT_ORDER_IN_TRANSIT: "Order in Transit",
    PO_EVT_ORDER_RECEIVED_COMPLETE: "Order Received",
    PO_EVT_ORDER_RECEIVED: "Order Received Partial",
    PO_EVT_PO_RAISED_TO_VENDOR: "Order Raised to Vendor",
    PO_EVT_REQUEST_APPROVED: "Request Approved",
    PO_EVT_REQUEST_CREATED: "Request Created",
    PO_EVT_REQUEST_INITIATED: "Request Initiated",
    PO_EVT_REQUEST_REJECTED: "Request Rejected",
    PO_EVT_ORDER_AMENDMENT: "Order Amendment"
}

Order_Drafted = "OR_DTD"
Order_Draft_Amended = "OR_DAM"
Raised_by_customer = "OR_RBC"
Order_Scheduled = "OR_SCH"
Order_Amended = "OR_AMD"
Order_Item_Scheduled_Partial = "OR_ISP"
Order_Item_scheduled_Complete = "OR_ISC"
Order_Item_Delivered_Partial = "OR_IDP"
Order_Item_Delivered_Complete = "OR_IDC"
Order_Complete = "OR_CMP"
Order_InHold = "OR_IHO"
Order_Discarded = "OR_DIS"

ORDER_EVT_TYPE = {
    Order_Drafted: "Order Drafted",
    Order_Draft_Amended: "Order Draft Amended",
    Raised_by_customer: "Raised by customer",
    Order_Scheduled: "Order Scheduled",
    Order_Amended: "Order Amended",
    Order_Item_Scheduled_Partial: "Order Item Scheduled Partial",
    Order_Item_scheduled_Complete: "Order Item scheduled Complete",
    Order_Item_Delivered_Partial: "Order Item Delivered Partial",
    Order_Item_Delivered_Complete: "Order Item Delivered Complete",
    Order_Complete: "Order Complete",
    Order_InHold: "Order InHold",
    Order_Discarded: "Order Discarded"
}

Order_Item_Created = "OI_CRT"
Order_Item_Amended = "OI_AMD"
Order_Item_Accepted = "OI_ACT"
Order_Item_Scheduled = "OI_SCH"
Order_Item_Removed = "OI_RMD"
Order_Item_Assigned_Partial = "OI_ASP"
Order_Item_Assigned_Complete = "OI_ASC"
Order_InHold = "OI_IHO"
Order_Discarded = "OI_DIS"

ORDER_ITEM_EVT_TYPE = {
    Order_Item_Created: "Order Item Created",
    Order_Item_Amended: "Order Item Amended",
    Order_Item_Accepted: "Order Item Accepted",
    Order_Item_Scheduled: "Order Item Scheduled",
    Order_Item_Removed: "Order Item Removed",
    Order_Item_Assigned_Partial: "Order Item Assigned Partial",
    Order_Item_Assigned_Complete: "Order Item Assigned Complete",
    Order_InHold: "Order InHold",
    Order_Discarded: "Order Discarded"
}

# Product_Assigned = "ITMV_ASD"
# Product_Assigned_Partial = "ITMV_APL"
# Product_Assigned_Pending_Production = "ITMV_APP"
# Product_Assigned_Pending_Inbound = "ITMV_API"
# Product_Assignment_Reversed = "ITMV_ARS"
# Product_Assignment_Planned = "ITMV_ASP"
#
# ORDER_ITEM_SUBVARIANT_TRANS_TYPE = {
#
#                                     Product_Assigned : "Product_Assigned",
#                                     Product_Assigned_Partial : "Product_Assigned_Partial",
#                                     Product_Assigned_Pending_Production : "Product_Assigned_Pending_Production",
#                                     Product_Assigned_Pending_Inbound : "Product_Assigned_Pending_Inbound",
#                                     Product_Assignment_Reversed : "Product_Assignment_Reversed",
#                                     Product_Assignment_Planned : "Product_Assignment_Planned"
# }


PRT_ALT_Allotment_Restricted = "PALT_RTD"
PRT_ALT_No_Allotment_pending = "PALT_NPL"
PRT_ALT_No_Stock_for_Allotment = "PALT_NST"
PRT_ALT_Full_Allotment_available = "PALT_FAA"
PRT_ALT_Partial_Allotment_available = "PALT_PAA"
PRT_ALT_Force_Allotment = "PALT_FAL"

ORDER_ITEM_SUBVARIANT_TRANS_TYPE = {

    PRT_ALT_Allotment_Restricted: "PRT_ALT_Allotment_Restricted",
    PRT_ALT_No_Allotment_pending: "PRT_ALT_No_Allotment_pending",
    PRT_ALT_No_Stock_for_Allotment: "PRT_ALT_No_Stock_for_Allotment",
    PRT_ALT_Full_Allotment_available: "PRT_ALT_Full_Allotment_available",
    PRT_ALT_Partial_Allotment_available: "PRT_ALT_Partial_Allotment_available",
    PRT_ALT_Force_Allotment: "PRT_ALT_Force_Allotment"
}


VIEW_TYPE_CUSDAT = "CUSDAT"

CUSDAT_TYPE_BG_COLOR = "BG_COLOR"
CUSDAT_TYPE_TEXT_COLOR = "TEXT_COLOR"
# data = {"pc":[{"t":"BG_COLOR","v":obj.request_status.color_percent}], "dt":obj.request_status.name}
CUSDAT_TYPE_STATUS_PERCENT_RAW = "STATUS_PERCENT_RAW"
# data = {"pc":[{"t":"STATUS_PERCENT_RAW","v":color_percent}], "dt":str(color_percent)}
CUSDAT_TYPE_IMG_THUMB = "IMG_THUMB"

STORE_CAPCITY_DEF = 111453
# data = {"pc":[{"t":"CUSDAT_TYPE_IMG_THUMB","v":<url>}], "dt":<product_name>}
