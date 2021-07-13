import datetime
import json
import random
import string

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from fcm_django.models import FCMDevice
from rest_framework.response import Response
from rest_framework.views import APIView

from DbUtils import db_operations_support, support_serializer_submit, support_db
from GEN import GEN_Constants
from GEN import dbconstants
from GEN import value_constant
from GEN.forms import UserFormCustomer, UserProfileInfoForm, IOrderForm, IOrderItemForm, OrderLogForm, OrderItemLogForm, \
    UserHealthProfileForm
from .models import Order, UserProfileInfo, OrderItem, \
    ProductCategory, Product, ProductBase, ItemMeasuementUnit, C19SymptomSet, BrandBranchBasicInfo, \
    BranchServisableCategory, BranchServisableProduct, \
    BranchServisableProductBase, AppUserType, BrandBasicInfo, OrderStatus, ServisableDaysCriteria, \
    BrandAppspecificDetails
from .serialiserBase import EnterPriseForm, \
    CMN_CommunicationPhysicalModelSerializer, ProductCategorySerializer, ProductSerializer, ProductBaseSerializer, \
    ItemMeasuementUnitSerializer, C19SymptomSetSerializer, UserProfileInfoSerializer, UserProfileSuggestionSerializer, \
    ProductSuggestionListSerializer, \
    BrandBranchBasicInfoSerializer, BranchAgentListSerializer, BranchOrderListSerializer, OrderDetail01Serializer, \
    ProductCategorySerializerBranchUser, ServisableProductSerializerBranchUser, ServisableProductSerializerCustomer, \
    CustomerAllOrderSerializer, BranchDetailAdminSerializer, ProductCategorySerializerAd, StoreUomSerializer, \
    BrandBranchBasicInfoSerializerAD, BranchAgentDetailSerializer, BranchServisableProductSerializerAd, \
    ProductADFeedSerializer, BrandOrderListSerializer, OrderDetail01SerializerWithActions, OrderAgentResponseSerializer

import base64
from django.core.files.base import ContentFile
from datetime import datetime, timedelta
from django.db.models import Sum

from .value_constant import get_display_translated_value

def change_order_status_auto(request):
    print("1")
    change_order_status_upon_time_expiry()
    print("3")
    return HttpResponse(json.dumps({"SUCCESS":True, "RESPONSE_MESSAGE":"Successa"}),
                        content_type="application/json")



def change_order_status_upon_time_expiry(expiry_checked_in = 7, expiry_scheduled= 10, expiry_requested_befor_schedule_time= 1):
    # https: // stackoverflow.com / questions / 13685201 / how - to - add - hours - to - current - time - in -python
    print("2")
    # order_list = Order.objects.filter(brand__id=brand_id, branch=brandbranch_id,
    # order_list = Order.objects.filter(order_status__code=GEN_Constants.ORDER_STATUS_ONGOING, checked_in_time__lt =  )

    # order_list.filter()

    # order_list = Order.objects.filter(schedule_requested_time__lt=datetime.now()).order_by(
    #     'schedule_requested_time')

    # order_list = order_list.order_by('-updated_at')

    # marking checkedin customer as completed after expiry time

    print("aaa")
    exp_dt_checked_in = datetime.now() - timedelta(hours=expiry_checked_in)
    qs_order_checkedin = Order.objects.filter(checked_in_time__lt =  exp_dt_checked_in, order_status__code=GEN_Constants.ORDER_STATUS_ONGOING)

    order_status_q = db_operations_support.get_db_object_g(OrderStatus,
                                                           {"code": GEN_Constants.ORDER_STATUS_COMPLETED})
    qs_order_checkedin.update(order_status=order_status_q)

    # marking booked and confirmed customer as no show after expiry time of scheduled time

    exp_dt_scheduled = datetime.now() - timedelta(hours=expiry_scheduled)
    qs_order_scheduled = Order.objects.filter(schedule_requested_time__lt = exp_dt_scheduled, order_status__code=GEN_Constants.ORDER_STATUS_AGENT_APPROVED)

    order_status_scheduled_q = db_operations_support.get_db_object_g(OrderStatus,
                                                           {"code": GEN_Constants.ORDER_STATUS_NO_SHOW})
    qs_order_scheduled.update(order_status=order_status_scheduled_q)

    # marking scheduled requested customer as rejected after expiry time of request time

    exp_dt_requested = datetime.now() + timedelta(hours=expiry_requested_befor_schedule_time)

    print("exp_dt_requested")
    print(exp_dt_requested)
    qs_order_requested = Order.objects.filter(schedule_requested_time__lt = exp_dt_requested, order_status__code=GEN_Constants.ORDER_STATUS_INITIATED)

    order_status_req_q = db_operations_support.get_db_object_g(OrderStatus,
                                                           {"code": GEN_Constants.ORDER_STATUS_AGENT_REJECTED_NO_SLOT})
    qs_order_requested.update(order_status=order_status_req_q)




def get_api_language_preference(received_data):


    try:
        if "lang" in received_data:
            if received_data["lang"] == value_constant.KEY_LANGUAGE_TA:
                return value_constant.KEY_LANGUAGE_TA
            else:
                return value_constant.KEY_LANGUAGE_EN

        return value_constant.KEY_LANGUAGE_EN

    except:
        return value_constant.KEY_LANGUAGE_EN



def get_file_from_base64(b64_string):

    image_data = b64_string
    format, imgstr = image_data.split(';base64,')
    print("format", format)
    ext = format.split('/')[-1]

    data = ContentFile(base64.b64decode(imgstr))
    return data

    # file_name = "'myphoto." + ext
    # user.image.save(file_name, data, save=True)

class BrandBranchOrdersOngoing(APIView):

    def post(self,request):
        received_json_data=json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)
        print("reee")
        print(received_json_data)

        # phone = received_json_data["user_phone"]
        # user_p = UserProfileInfo.objects.get(phone_primary=phone)

        brandbranch_id = received_json_data["brand_branch_id"]
        brand_id = received_json_data["brand_id"]


        # order_list = Order.objects.filter(brand__id = brand_id, branch = brandbranch_id).order_by('-updated_at')

        order_list = Order.objects.filter(brand__id = brand_id, branch = brandbranch_id, order_status__code = GEN_Constants.ORDER_STATUS_ONGOING)

        order_list.filter()

        order_list = order_list.order_by('-updated_at')

        order_list_s = BranchOrderListSerializer(order_list, many=True)

        base_data = {}
        base_data["order"] = order_list_s.data
        base_data["delivery_text"] = "Order will bw delivered by 11 AM tomorrow"
        base_data["status_text"] = "RECEIVED"

        return Response(base_data)

class BrandBranchOrdersPendingApproval(APIView):

    def post(self,request):
        received_json_data=json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)
        print("reee")
        print(received_json_data)

        # phone = received_json_data["user_phone"]
        # user_p = UserProfileInfo.objects.get(phone_primary=phone)

        brandbranch_id = received_json_data["brand_branch_id"]
        brand_id = received_json_data["brand_id"]


        # order_list = Order.objects.filter(brand__id = brand_id, branch = brandbranch_id).order_by('-updated_at')

        order_list = Order.objects.filter(brand__id = brand_id, branch = brandbranch_id, order_status__code = GEN_Constants.ORDER_STATUS_INITIATED)
        # order_list = Order.objects.filter(brand__id = brand_id, branch = brandbranch_id)
        # order_list.filter()

        order_list = order_list.order_by('-updated_at')

        order_list_s = BranchOrderListSerializer(order_list, many=True)

        base_data = {}
        base_data["order"] = order_list_s.data
        base_data["delivery_text"] = "Order will bw delivered by 11 AM tomorrow"
        base_data["status_text"] = "RECEIVED"

        print("respisfssssssssssssss")
        print(base_data)

        return Response(base_data)

class BrandBranchOrdersUpcoming(APIView):

    def post(self,request):
        received_json_data=json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)

        print("reee")
        print(received_json_data)

        # phone = received_json_data["user_phone"]
        # user_p = UserProfileInfo.objects.get(phone_primary=phone)

        brandbranch_id = received_json_data["brand_branch_id"]
        brand_id = received_json_data["brand_id"]


        # order_list = Order.objects.filter(brand__id = brand_id, branch = brandbranch_id).order_by('-updated_at')

        order_list = Order.objects.filter(brand__id = brand_id, branch = brandbranch_id, order_status__code = GEN_Constants.ORDER_STATUS_AGENT_APPROVED)

        order_list.filter()

        order_list = order_list.order_by('schedule_requested_time')

        order_list_s = BranchOrderListSerializer(order_list, many=True)

        base_data = {}
        base_data["order"] = order_list_s.data
        base_data["delivery_text"] = "Order will bw delivered by 11 AM tomorrow"
        base_data["status_text"] = "RECEIVED"

        return Response(base_data)


def get_order_filter_type(filter_group):

    dataset = {}

    if filter_group == "ORD_GR_ONGOING":
        dataset["order_status__code"] = GEN_Constants.ORDER_STATUS_ONGOING
    elif filter_group == "ORD_GR_UPCOMING":
        dataset["order_status__code"] = GEN_Constants.ORDER_STATUS_AGENT_APPROVED
    elif filter_group == "ORD_GR_PENDING_APPROVAL":
        dataset["order_status__code"] = GEN_Constants.ORDER_STATUS_INITIATED
    elif filter_group == "ORD_GR_REJECTED_ALL":
        dataset["order_status__code"] = GEN_Constants.ORDER_STATUS_INITIATED
    elif filter_group == "GR_ALL":
        pass

    return dataset



class BrandOrders(APIView):

    def post(self, request):
        received_json_data=json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)
        print("reee")
        print(received_json_data)
        brand_id = received_json_data["brand_id"]
        order_list = Order.objects.filter(brand__id = brand_id)


        if "page_no" in received_json_data:
            page_no = received_json_data["page_no"]
        else:
            page_no = 1

        if "branch_id" in received_json_data:
            order_list = order_list.filter(branch__id = received_json_data["branch_id"])

        # print("order_status_code===1")
        if "order_status_code" in received_json_data:
            # print("order_status_code===2")
            order_status_code = received_json_data["order_status_code"]
            if order_status_code != "ORD_ALL":
                # print("order_status_code===3")
                # print(order_status_code)
                order_list = order_list.filter(order_status__code = order_status_code)
                # order_list = order_list.filter(order_status__code = "ORD_APPROVED")


        # print("final liste count")
        # print("==="+str(order_list.count()))

        if "filter_start_date" in received_json_data:
            filter_start_date = received_json_data["filter_start_date"]
            order_list = order_list.filter(schedule_requested_time__gte = filter_start_date+" 00:00:00")

        if "filter_end_date" in received_json_data:
            filter_end_date = received_json_data["filter_end_date"]
            order_list = order_list.filter(schedule_requested_time__lte = filter_end_date+" 23:59:59")

        # print("c2==="+str(order_list.count()))
        order_list = order_list.order_by('-updated_at')


        order_list = get_paginated_data(order_list, page_no, page_size=GEN_Constants.ORDERS_LIST_COUNT_BUSINESS)
        # print("c3==="+str(order_list.count()))
        order_list_s = BrandOrderListSerializer(order_list, many=True)

        # order_list_s


        base_data = {}
        base_data["order"] = order_list_s.data
        base_data["delivery_text"] = "Order will bw delivered by 11 AM tomorrow"
        base_data["status_text"] = "RECEIVED"

        return Response(base_data)

class BrandBranchOrders(APIView):

    def post(self,request):
        received_json_data=json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)
        print("reee")
        print(received_json_data)

        # phone = received_json_data["user_phone"]
        # user_p = UserProfileInfo.objects.get(phone_primary=phone)

        brandbranch_id = received_json_data["brand_branch_id"]
        brand_id = received_json_data["brand_id"]


        # order_list = Order.objects.filter(brand__id = brand_id, branch = brandbranch_id).order_by('-updated_at')

        order_list = Order.objects.filter(brand__id = brand_id, branch = brandbranch_id)

        order_list.filter()

        order_list = order_list.order_by('-updated_at')

        order_list_s = BranchOrderListSerializer(order_list, many=True)

        base_data = {}
        base_data["order"] = order_list_s.data
        base_data["delivery_text"] = "Order will bw delivered by 11 AM tomorrow"
        base_data["status_text"] = "RECEIVED"

        return Response(base_data)

class BrandBranchOrdersFiltered(APIView):

    def post(self,request):
        received_json_data=json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)
        print("reee")
        print(received_json_data)

        # phone = received_json_data["user_phone"]
        # user_p = UserProfileInfo.objects.get(phone_primary=phone)

        brandbranch_id = received_json_data["brand_branch_id"]
        brand_id = received_json_data["brand_id"]

        type = received_json_data["upcoming"]


        order_list = Order.objects.filter(brand__id = brand_id, branch = brandbranch_id)

        # order_list.filter()
        order_list = order_list.order_by('-updated_at')
        order_list_s = BranchOrderListSerializer(order_list, many=True)


        base_data = {}
        base_data["order"] = order_list_s.data
        base_data["delivery_text"] = "Order will bw delivered by 11 AM tomorrow"
        base_data["status_text"] = "RECEIVED"

        return Response(base_data)

class GetBrandBranchDetailAdmin(APIView):


    def post(self,request):
        received_json_data=json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)
        print("reee")
        print(received_json_data)

        brandbranch_id = received_json_data["brand_branch_id"]

        branch_detail = BrandBranchBasicInfo.objects.get(id = brandbranch_id)

        order_list_s = BranchDetailAdminSerializer(branch_detail, many=False)


        base_data = {}
        base_data["SUCCESS"] = True
        base_data["RESPONSE_MESSAGE"] = "Details Fetched Successful"
        base_data["RESPONSE_DATA"] = order_list_s.data

        return Response(base_data)


class CreateProduct(APIView):

    def update_product_in_servisable_branches(self, product_id, product_dataset):
        # class BranchServisableProduct(models.Model):
        #     product = models.ForeignKey(Product, on_delete=models.CASCADE)
        #     branch = models.ForeignKey(BrandBranchBasicInfo, on_delete=models.CASCADE)
        #     price = models.FloatField(default=0, blank=True)
        #     status = models.CharField(max_length=2, choices=dbconstants.STATUS, default=dbconstants.STATUS_ACTIVE)
        #     created_at = models.DateTimeField(auto_now_add=True)
        #     updated_at = models.DateTimeField(auto_now=True)
        #     is_available = models.BooleanField(default=True)
        #     is_online = models.BooleanField(default=True)

        key_set = {"brand__id":product_dataset["brand"]}
        BrandBranchBasicInfo_q = db_operations_support.get_db_object_g_list(BrandBranchBasicInfo, key_set)

        for e_BrandBranchBasicInfo in BrandBranchBasicInfo_q:

            current_process_model = BranchServisableProduct

            current_process_model_data = {}

            current_process_model_data["product"] = product_id
            current_process_model_data["branch"] = e_BrandBranchBasicInfo.id
            current_process_model_data["price"] =product_dataset["price"]

            proceed_current_process_model, serializer_current_process_model = support_serializer_submit.validate_save_instance(current_process_model, current_process_model_data)



    def post(self,request):
        received_json_data=json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)
        print("reee")
        print(received_json_data)

        is_create_record = True

        # create category
        # create default category sub

        Product_dataset = received_json_data["product_basic"]
        current_process_model_data = Product_dataset
        current_process_model = Product

        if "id" in current_process_model_data:
            is_create_record = False


        branch_image_file = None

        if "pic" in Product_dataset:
            branch_image_file = "data:image/jpeg;base64,"+Product_dataset["pic"]
            del Product_dataset["pic"]

        # measurement_unit
        # product_base

        category_id = Product_dataset["category"]
        del Product_dataset["category"]

        key_set = {"name":"DEFAULT", "product_category__id":category_id}
        ProductBase_q = db_operations_support.get_db_object_g_last(ProductBase, key_set)

        current_process_model_data["product_base"] = ProductBase_q.id



        proceed_current_process_model, serializer_current_process_model = support_serializer_submit.validate_save_instance(current_process_model, current_process_model_data)


        if proceed_current_process_model:
            product_id = serializer_current_process_model["id"]

            if branch_image_file is not None:
                support_db.create_update_image(current_process_model, product_id, "pic", branch_image_file)

            if is_create_record:
                # proceed creating default product base
                self.update_product_in_servisable_branches(product_id, current_process_model_data)

                ProductBase_dataset = {}

        base_data = {}
        base_data["SUCCESS"] = False
        base_data["RESPONSE_MESSAGE"] = "Details Updation Failed"

        if proceed_current_process_model:
            base_data["SUCCESS"] = True
            base_data["RESPONSE_MESSAGE"] = "Details Updated Successfully"
        else:
            print("errorssdd")
            print("serialisdfff=="+ str(serializer_current_process_model.errors))

        return Response(base_data)

class CreateProductCategory(APIView):



    def post(self,request):
        received_json_data=json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)
        print("reee")
        print(received_json_data)

        is_create_record = True




        # create category
        # create default category sub


        ProductCategory_dataset = received_json_data["category_basic"]
        current_process_model_data = ProductCategory_dataset
        current_process_model = ProductCategory

        if "id" in current_process_model_data:
            is_create_record = False


        branch_image_file = None
        if "pic" in ProductCategory_dataset:
            branch_image_file = "data:image/jpeg;base64,"+ProductCategory_dataset["pic"]
            del ProductCategory_dataset["pic"]

        proceed_current_process_model, serializer_current_process_model = support_serializer_submit.validate_save_instance(current_process_model, current_process_model_data)


        if proceed_current_process_model:
            category_id = serializer_current_process_model["id"]

            category_dataset = current_process_model_data

            if branch_image_file is not None:
                support_db.create_update_image(ProductCategory, category_id, "pic", branch_image_file)

            if is_create_record:
                # proceed creating default product base

                ProductBase_dataset = {}
                ProductBase_dataset["name"] = "DEFAULT"
                ProductBase_dataset["sub_text"] = ""
                ProductBase_dataset["description"] = ""
                ProductBase_dataset["status_note"] = " Default product group created upon creating new Category"
                ProductBase_dataset["product_category"] = category_id
                ProductBase_dataset["has_view"] = False

                proceed_current_process_model, serializer_current_process_model = support_serializer_submit.validate_save_instance(
                    ProductBase, ProductBase_dataset)

                product_base_id = serializer_current_process_model["id"]

                key_set = {"brand__id": current_process_model_data["brand"]}
                BrandBranchBasicInfo_q = db_operations_support.get_db_object_g_list(BrandBranchBasicInfo, key_set)

                for e_BrandBranchBasicInfo in BrandBranchBasicInfo_q:

                    # create servisable category
                    current_process_model = BranchServisableCategory

                    current_process_model_data = {}

                    current_process_model_data["product_category"] = category_id
                    current_process_model_data["branch"] = e_BrandBranchBasicInfo.id
                    proceed_current_process_model, serializer_current_process_model = support_serializer_submit.validate_save_instance(
                        current_process_model, current_process_model_data)

                    # create servisable product base
                    current_process_model = BranchServisableProductBase

                    current_process_model_data = {}

                    current_process_model_data["product_base"] = product_base_id
                    current_process_model_data["branch"] = e_BrandBranchBasicInfo.id
                    proceed_current_process_model, serializer_current_process_model = support_serializer_submit.validate_save_instance(
                        current_process_model, current_process_model_data)

        base_data = {}
        base_data["SUCCESS"] = False
        base_data["RESPONSE_MESSAGE"] = "Details Updation Failed"

        if proceed_current_process_model:
            base_data["SUCCESS"] = True
            base_data["RESPONSE_MESSAGE"] = "Details Updated Successfully"
        else:
            print("errorssdd")
            print("serialisdfff=="+ str(serializer_current_process_model.errors))

        return Response(base_data)

class CreateBrandBranch(APIView):


    def create_product_copy_on_branch(self, brand_id, branch_id):

        # copy category
        # copy category sub
        # copy product list with active and available status

        ProductCategory_q = ProductCategory.objects.filter(brand__id = brand_id)
        proceed_current_process_model = False
        serializer_current_process_model = {"test":"error"}



        # print(brand_id, branch_id)
        for e_ProductCategory in ProductCategory_q:
            print("eact cat")

            BranchServisableCategory_data = {}
            BranchServisableCategory_data["branch"] = branch_id
            BranchServisableCategory_data["product_category"] = e_ProductCategory.id
            # BranchServisableCategory_data["status"] =
            BranchServisableCategory_data["is_available"] = e_ProductCategory.is_available
            BranchServisableCategory_data["is_online"] = True

            proceed_current_process_model, serializer_current_process_model = support_serializer_submit.validate_save_instance(
                BranchServisableCategory, BranchServisableCategory_data)

            ProductBase_q = ProductBase.objects.filter(product_category__id = e_ProductCategory.id)

            for e_ProductBase in ProductBase_q:
                print("eact cat p base")
                BranchServisableProductBase_data = {}

                BranchServisableProductBase_data["product_base"] = e_ProductBase.id
                BranchServisableProductBase_data["branch"] = branch_id
                BranchServisableProductBase_data["is_available"] = e_ProductBase.is_available

                proceed_current_process_model, serializer_current_process_model = support_serializer_submit.validate_save_instance(
                    BranchServisableProductBase, BranchServisableProductBase_data)
                if proceed_current_process_model == False:
                    break


        if proceed_current_process_model:
            Product_q = Product.objects.filter(product_base__product_category__brand__id = brand_id)
            for e_Product in Product_q:
                print("eact cat product")
                BranchServisableProduct_data = {}
                BranchServisableProduct_data["product"] = e_Product.id
                BranchServisableProduct_data["branch"] = branch_id
                BranchServisableProduct_data["is_available"] = e_Product.is_available
                BranchServisableProduct_data["is_online"] = e_Product.is_available

                proceed_current_process_model, serializer_current_process_model = support_serializer_submit.validate_save_instance(
                    BranchServisableProduct, BranchServisableProduct_data)

        if proceed_current_process_model ==  False:
            print(str(serializer_current_process_model))



    def post(self,request):
        received_json_data=json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)
        print("reee")
        print(received_json_data)

        BrandBranchBasicInfo_dataset = received_json_data["store_basic"]

        response_text_failure = "Details Updation Failed"

        is_create = True



        current_process_model_data = BrandBranchBasicInfo_dataset
        current_process_model = BrandBranchBasicInfo
        proceed_current_process_model = True

        if "id" in BrandBranchBasicInfo_dataset:
            is_create = False
        else:
            print("came0000000000000000000000001")
            place_google_id = BrandBranchBasicInfo_dataset["place_google_id"]
            brand_id = BrandBranchBasicInfo_dataset["brand"]
            print("came00000000000000000000000012")
            if BrandBranchBasicInfo.objects.filter(brand__id = brand_id, place_google_id=place_google_id).count() >0:
                proceed_current_process_model = False
                print("came00000000000000000000000013")
                response_text_failure = "Branch with this address already exist.Please select some other branch from List"



        if proceed_current_process_model:
            branch_image_file = None
            if "branch_image" in BrandBranchBasicInfo_dataset:
                # branch_image_file = get_file_from_base64("data:image/jpeg;base64,"+BrandBranchBasicInfo_dataset["branch_image"])
                branch_image_file = "data:image/jpeg;base64,"+BrandBranchBasicInfo_dataset["branch_image"]
                del BrandBranchBasicInfo_dataset["branch_image"]

            proceed_current_process_model, serializer_current_process_model = support_serializer_submit.validate_save_instance(current_process_model, current_process_model_data)



        if proceed_current_process_model:
            brand_branch_id = serializer_current_process_model["id"]
            brand_id = current_process_model_data["brand"]

            if branch_image_file is not None:
                # BrandBranchBasicInfo_q = BrandBranchBasicInfo.objects.get(id = brand_branch_id)
                # BrandBranchBasicInfo_q.branch_base_image = branch_image_file
                # support_db.create_update_image(PBS_ProductSampleModel, PBS_ProductSampleModel_slug, "image_1", image_1)
                support_db.create_update_image(BrandBranchBasicInfo, brand_branch_id, "branch_base_image", branch_image_file)



            ServisableDaysCriteria_dataset_arr = received_json_data["store_servisable_details"]
            current_process_model = ServisableDaysCriteria
            print("Send brand isssss")
            print(brand_id)

            if is_create:
                response_text_success = "Branch Created Successfully."
                self.create_product_copy_on_branch(brand_id, brand_branch_id)
            else:
                response_text_success = "Branch Details updated Successfully."

            for ServisableDaysCriteria_dataset in ServisableDaysCriteria_dataset_arr:
                current_process_model_data = ServisableDaysCriteria_dataset
                current_process_model_data["branch"] = brand_branch_id
                if (current_process_model_data["service_start_time"] == 24):
                    current_process_model_data["service_start_time"] = 0
                # current_process_model_data["service_start_time"] = 5

                if (current_process_model_data["service_end_time"] == 24):
                    current_process_model_data["service_end_time"] = 0
                # current_process_model_data["service_end_time"] = 15
                print("creahh data")
                print(current_process_model_data)
                current_process_model_data["service_start_time"] = str(current_process_model_data["service_start_time"])+":00:00"
                current_process_model_data["service_end_time"] = str(current_process_model_data["service_end_time"])+":00:00"
                proceed_current_process_model, serializer_current_process_model = support_serializer_submit.validate_save_instance(
                    current_process_model, current_process_model_data)

                if proceed_current_process_model == False:

                    print("error tesfdsfsdf===================9890-098")
                    print(current_process_model_data["id"])
                    print(str(serializer_current_process_model.errors))


            # ServisableDaysCriteria
        # {"SUCCESS": False, "RESPONSE_DATA": base_data}
        base_data = {}
        base_data["SUCCESS"] = False
        base_data["RESPONSE_MESSAGE"] = response_text_failure

        if proceed_current_process_model:
            base_data["SUCCESS"] = True
            base_data["RESPONSE_MESSAGE"] = response_text_success
        else:
            print("errorssdd")
            # print("serialisdfff=="+ str(serializer_current_process_model.errors))

        return Response(base_data)


class CreateUpdateDataset(APIView):


    def post(self,request):
        received_json_data=json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)
        print("reee")
        print(received_json_data)


        current_process_model_data = received_json_data["reference_dataset"]
        current_process_model_name = received_json_data["reference_model"]
        current_process_model = db_operations_support.get_model_class("GEN", current_process_model_name)

        proceed_current_process_model, serializer_current_process_model = support_serializer_submit.validate_save_instance(current_process_model, current_process_model_data)

        if proceed_current_process_model:
            brand_branch_id = serializer_current_process_model["id"]

        base_data = {}
        base_data["SUCCESS"] = False
        base_data["RESPONSE_MESSAGE"] = "Details Updation Failed"

        if proceed_current_process_model:
            base_data["SUCCESS"] = True
            base_data["RESPONSE_MESSAGE"] = "Details Updated Successfully"
        else:
            print("errorssdd")
            print("serialisdfff=="+ str(serializer_current_process_model.errors))

        return Response(base_data)




class UpdateUserDetails(APIView):

    def post(self,request):
        received_json_data=json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)
        print("reee")
        print(received_json_data)

        # phone = received_json_data["user_phone"]
        # user_p = UserProfileInfo.objects.get(phone_primary=phone)

        current_process_model_data = received_json_data
        current_process_model = UserProfileInfo

        proceed_current_process_model, serializer_current_process_model = support_serializer_submit.validate_save_instance(current_process_model, current_process_model_data)
        # {"SUCCESS": False, "RESPONSE_DATA": base_data}
        base_data = {}
        base_data["SUCCESS"] = False
        base_data["RESPONSE_MESSAGE"] = "Details Updation Failed"

        if proceed_current_process_model:
            base_data["SUCCESS"] = True
            base_data["RESPONSE_MESSAGE"] = "Details Updated Successfully"


        return Response(base_data)

class UpdateServisableCategoryDetails(APIView):

    def post(self,request):
        received_json_data=json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)
        print("reee")
        print(received_json_data)

        # phone = received_json_data["user_phone"]
        # user_p = UserProfileInfo.objects.get(phone_primary=phone)

        current_process_model_data = received_json_data
        current_process_model = BranchServisableCategory

        proceed_current_process_model, serializer_current_process_model = support_serializer_submit.validate_save_instance(current_process_model, current_process_model_data)
        # {"SUCCESS": False, "RESPONSE_DATA": base_data}
        base_data = {}
        base_data["SUCCESS"] = False
        base_data["RESPONSE_MESSAGE"] = "Details Updation Failed"

        if proceed_current_process_model:
            base_data["SUCCESS"] = True
            base_data["RESPONSE_MESSAGE"] = "Details Updated Successfully"


        return Response(base_data)

class UpdateServisableProduct(APIView):

    def post(self,request):
        received_json_data=json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)
        print("reee")
        print(received_json_data)

        # phone = received_json_data["user_phone"]
        # user_p = UserProfileInfo.objects.get(phone_primary=phone)

        current_process_model_data = received_json_data
        current_process_model = BranchServisableProduct

        proceed_current_process_model, serializer_current_process_model = support_serializer_submit.validate_save_instance(current_process_model, current_process_model_data)
        # {"SUCCESS": False, "RESPONSE_DATA": base_data}
        base_data = {}
        base_data["SUCCESS"] = False
        base_data["RESPONSE_MESSAGE"] = "Details Updation Failed"

        if proceed_current_process_model:
            base_data["SUCCESS"] = True
            base_data["RESPONSE_MESSAGE"] = "Details Updated Successfully"


        return Response(base_data)

class UpdateCategoryDetails(APIView):

    def post(self,request):
        received_json_data=json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)
        print("reee")
        print(received_json_data)

        # phone = received_json_data["user_phone"]
        # user_p = UserProfileInfo.objects.get(phone_primary=phone)

        current_process_model_data = received_json_data
        current_process_model = ProductCategory

        proceed_current_process_model, serializer_current_process_model = support_serializer_submit.validate_save_instance(current_process_model, current_process_model_data)
        # {"SUCCESS": False, "RESPONSE_DATA": base_data}
        base_data = {}
        base_data["SUCCESS"] = False
        base_data["RESPONSE_MESSAGE"] = "Details Updation Failed"

        if proceed_current_process_model:
            base_data["SUCCESS"] = True
            base_data["RESPONSE_MESSAGE"] = "Details Updated Successfully"


        return Response(base_data)

class BaGetOrderDetailswithActions(APIView):

    def post(self,request):
        received_json_data=json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)


        # print("reee")
        # print(received_json_data)

        # phone = received_json_data["user_phone"]
        # user_p = UserProfileInfo.objects.get(phone_primary=phone)

        id = received_json_data["order_base_id"]



        base_data = {}
        order_item = Order.objects.get(id = id)
        if order_item is not None:
            order_list_s = OrderDetail01SerializerWithActions(order_item,  many=False)
            base_data["order"] = order_list_s.data
        else:
            base_data["order"] = None


        base_data["delivery_text"] = "Order will bw delivered by 11 AM tomorrow"
        base_data["status_text"] = "RECEIVED"

        return Response(base_data)

class GetOrderDetails01(APIView):

    def post(self,request):
        received_json_data=json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)
        print("reee")
        print(received_json_data)

        # phone = received_json_data["user_phone"]
        # user_p = UserProfileInfo.objects.get(phone_primary=phone)

        id = received_json_data["order_base_id"]



        base_data = {}
        order_item = Order.objects.get(id = id)
        if order_item is not None:
            order_list_s = OrderDetail01Serializer(order_item, many=False)
            base_data["order"] = order_list_s.data
        else:
            base_data["order"] = None


        base_data["delivery_text"] = "Order will bw delivered by 11 AM tomorrow"
        base_data["status_text"] = "RECEIVED"

        return Response(base_data)

class GetOrderAgentResponse(APIView):

    def post(self,request):
        received_json_data=json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)

        print("reee")
        print(received_json_data)

        # phone = received_json_data["user_phone"]
        # user_p = UserProfileInfo.objects.get(phone_primary=phone)

        id = received_json_data["order_base_id"]



        base_data = {}
        order_item = Order.objects.get(id = id)
        if order_item is not None:
            order_list_s = OrderAgentResponseSerializer(order_item, many=False)
            base_data["order"] = order_list_s.data
        else:
            base_data["order"] = None

        return Response(base_data)


def proceedPush(brand_id, app_user_type, device_id, title, message, datapayload):

    # api_key = GEN_Constants.getFcmApiKey(app_user_type)

    brand_app_details = db_operations_support.get_db_object_g_last(BrandAppspecificDetails, {"brand_id": brand_id})

    if app_user_type == GEN_Constants.APP_USER_TYPE_CUSTOMER:
        api_key = brand_app_details.api_key_customer
    else:
        # api_key = brand_app_details.api_key_customer
        api_key = brand_app_details.api_key_business

# teddd
    f = FCMDevice()

    f.name = "Test"
    f.registration_id = device_id
    f.active = True
    f.type = "android"

    f.send_message(title = title, body = message, data = datapayload, api_key = api_key)
    # title = "Title", body = "Message", api_key = "[project 1 api key]")
    return Response({"ressa": True})


class SamplePush(APIView):

    def get(self,request):
        received_json_data = request.POST
        api_lang = get_api_language_preference(received_json_data)

        f =  FCMDevice()

        f.name = "Test"
        f.registration_id = "cIDDhkvAQyea-Vhluvlo8s:APA91bGdIDibu4SNxrFu_XKffv4VjDUf_eyUTsz_AC-4w6T3uEn4_s3biuUUfUYzzvYtlCX04INAb4oHRscxX1iM4S3fVj2qMmecW54b5sOL86lt9sfsm-ppd5CohrazrFUaEcGJLr27"
        f.active = True
        f.type = "android"

        # f.send_message("Title", "test message for impl")

        # customer
        message = "Json has semt a new schedule Request"
        data = {
                    "app_user_type" :GEN_Constants.APP_USER_TYPE_CUSTOMER,
                    "push_type":"SCHEDULE_RESPONSE",
                    "order_id":10
                    }

        # agent
        data = {
            "app_user_type": GEN_Constants.APP_USER_TYPE_BRANCH_AGENT,
            "push_type": "SCHEDULE_REQUEST",
            "order_id": 27
        }

        # data = {app_user_type=USR_BAGENT, push_type=SCHEDULE_REQUEST, order_id=5}


        brand_id = 2
        proceedPush(brand_id, GEN_Constants.APP_USER_TYPE_BRANCH_AGENT, f.registration_id, "Sample Title", message, data)
        # update_order_request_to_branch_user(9)
        return Response({"ressa":True})


class OrderAcceptedByAgent(APIView):

    def post(self,request):
        received_json_data=json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)


        print("reee")
        print(received_json_data)

        order_base_id = received_json_data["order_base_id"]



        order_status_q= db_operations_support.get_db_object_g(OrderStatus, {"code": GEN_Constants.ORDER_STATUS_AGENT_APPROVED})

        order_dataset = {}

        order_dataset["id"] = order_base_id
        order_dataset["order_status"] = order_status_q.id

        proceed_current_process_model, serializer_current_process_model = support_serializer_submit.validate_save_instance(Order, order_dataset)

        if proceed_current_process_model == False:
            print("error savin")
            print(serializer_current_process_model.errors)

        if proceed_current_process_model:
            # OrderRejectedByAgent
            proceed_client_approval_notification(order_base_id, api_lang)

        base_data = {"SUCCESS":True, "RESPONSE_MESSAGE":get_display_translated_value(value_constant.KEY_D_ORDER_MARKED_AS_ACCEPTED,api_lang)}
        return Response(base_data)


class OrderCancelledByAgent(APIView):

    def post(self,request):
        received_json_data=json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)


        print("reee")
        print(received_json_data)

        order_base_id = received_json_data["order_base_id"]



        order_status_q= db_operations_support.get_db_object_g(OrderStatus, {"code": GEN_Constants.ORDER_STATUS_CANCELLED})

        order_dataset = {}

        order_dataset["id"] = order_base_id
        order_dataset["order_status"] = order_status_q.id

        proceed_current_process_model, serializer_current_process_model = support_serializer_submit.validate_save_instance(Order, order_dataset)

        if proceed_current_process_model == False:
            print("error savin")
            print(serializer_current_process_model.errors)

        if proceed_current_process_model:
            # OrderRejectedByAgent
            proceed_client_approval_notification(order_base_id, api_lang)


        base_data = {"SUCCESS":True, "RESPONSE_MESSAGE":get_display_translated_value(value_constant.KEY_D_ORDER_MARKED_AS_REJECTED,api_lang)}
        return Response(base_data)

class OrderRejectedByAgent(APIView):

    def post(self,request):
        received_json_data=json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)


        print("reee")
        print(received_json_data)

        order_base_id = received_json_data["order_base_id"]



        order_status_q= db_operations_support.get_db_object_g(OrderStatus, {"code": GEN_Constants.ORDER_STATUS_AGENT_REJECTED_NO_SLOT})

        order_dataset = {}

        order_dataset["id"] = order_base_id
        order_dataset["order_status"] = order_status_q.id

        proceed_current_process_model, serializer_current_process_model = support_serializer_submit.validate_save_instance(Order, order_dataset)

        if proceed_current_process_model == False:
            print("error savin")
            print(serializer_current_process_model.errors)

        if proceed_current_process_model:
            # OrderRejectedByAgent
            proceed_client_approval_notification(order_base_id, api_lang)


        base_data = {"SUCCESS":True, "RESPONSE_MESSAGE":get_display_translated_value(value_constant.KEY_D_ORDER_MARKED_AS_REJECTED,api_lang)}
        return Response(base_data)

class OrderMarkedNoShowByAgent(APIView):

    def post(self,request):
        received_json_data=json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)


        print("reee")
        print(received_json_data)

        order_base_id = received_json_data["order_base_id"]



        order_status_q= db_operations_support.get_db_object_g(OrderStatus, {"code": GEN_Constants.ORDER_STATUS_NO_SHOW})

        order_dataset = {}

        order_dataset["id"] = order_base_id
        order_dataset["order_status"] = order_status_q.id

        proceed_current_process_model, serializer_current_process_model = support_serializer_submit.validate_save_instance(Order, order_dataset)

        if proceed_current_process_model == False:
            print("error savin")
            print(serializer_current_process_model.errors)

        if proceed_current_process_model:
            # OrderRejectedByAgent
            proceed_client_approval_notification(order_base_id, api_lang)


        base_data = {"SUCCESS":True, "RESPONSE_MESSAGE":get_display_translated_value(value_constant.KEY_D_ORDER_MARKED_AS_REJECTED,api_lang)}
        return Response(base_data)

def proceed_client_approval_notification(order_base_id,api_lang):



    data_set = {
        "app_user_type": GEN_Constants.APP_USER_TYPE_CUSTOMER,
        "push_type": "SCHEDULE_RESPONSE",
        "order_id": order_base_id
    }
    order_q = db_operations_support.get_db_object_g(Order, {"id": order_base_id})
    reg_id = order_q.user_customer.device_token

    title =get_display_translated_value(value_constant.KEY_D_BOOKING_NOT_CONFIRMED,api_lang)
    message = get_display_translated_value(value_constant.KEY_D_TAP_TO_VIEW_DETAILS,api_lang)

    if order_q.order_status.code == GEN_Constants.ORDER_STATUS_AGENT_APPROVED:
        title =get_display_translated_value(value_constant.KEY_D_BOOKING_CONFIRMED,api_lang)

    brand_id = order_q.brand.id


    proceedPush(brand_id, GEN_Constants.APP_USER_TYPE_CUSTOMER, reg_id, title, message, data_set)


class OrderMarkAsCompleted(APIView):

    def post(self, request):
        received_json_data=json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)

        print("reee")
        print(received_json_data)

        order_base_id = received_json_data["order_base_id"]



        order_status_q = db_operations_support.get_db_object_g(OrderStatus, {"code": GEN_Constants.ORDER_STATUS_COMPLETED})

        order_dataset = {}

        order_dataset["id"] = order_base_id
        order_dataset["order_status"] = order_status_q.id

        proceed_current_process_model, serializer_current_process_model = support_serializer_submit.validate_save_instance(Order, order_dataset)

        if proceed_current_process_model == False:
            print("error savin")
            print(serializer_current_process_model.errors)


        base_data = {"SUCCESS":True, "RESPONSE_MESSAGE":get_display_translated_value(value_constant.KEY_D_ORDER_MARKED_AS_COMPLETED,api_lang)}
        return Response(base_data)

class OrderMarkAsCheckedIn(APIView):

    def post(self,request):
        received_json_data=json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)


        print("reee")
        print(received_json_data)

        order_base_id = received_json_data["order_base_id"]
        order_status_q = db_operations_support.get_db_object_g(OrderStatus, {"code": GEN_Constants.ORDER_STATUS_ONGOING})

        order_dataset = {}

        order_dataset["id"] = order_base_id
        order_dataset["order_status"] = order_status_q.id
        order_dataset["checked_in_time"] = timezone.now()

        proceed_current_process_model, serializer_current_process_model = support_serializer_submit.validate_save_instance(Order, order_dataset)

        if proceed_current_process_model == False:
            print("error savin")
            print(serializer_current_process_model.errors)


        base_data = {"SUCCESS":True, "RESPONSE_MESSAGE":get_display_translated_value(value_constant.KEY_D_ORDER_MARKED_AS_CHECKEDIN,api_lang)}
        return Response(base_data)


class CustomerOrder(APIView):

    def post(self,request):
        received_json_data=json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)
        print("reee")
        print(received_json_data)

        phone = received_json_data["user_phone"]
        user_p = UserProfileInfo.objects.get(phone_primary=phone)



        order_list = Order.objects.filter(user_customer__id = user_p.id).order_by('-updated_at')
        order_list_s = CustomerAllOrderSerializer(order_list, many=True)


        base_data = {}
        base_data["order_list"] = order_list_s.data
        # base_data["delivery_text"] = "Order will bw delivered by 11 AM tomorrow"
        # base_data["status_text"] = "RECEIVED"

        return Response(base_data)


class AgentDetail_AD(APIView):

    def post(self,request):
        received_json_data=json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)
        print("reee")
        print(received_json_data)

        id = received_json_data["id"]
        user_p = UserProfileInfo.objects.get(id=id)

        user_p_s = BranchAgentDetailSerializer(user_p, many=False)


        base_data = {}
        base_data["agent_details"] = user_p_s.data
        # base_data["delivery_text"] = "Order will bw delivered by 11 AM tomorrow"
        # base_data["status_text"] = "RECEIVED"

        return Response(base_data)

class CustomerOrderUpcoming(APIView):

    def post(self,request):
        received_json_data=json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)
        print("reee")
        print(received_json_data)

        phone = received_json_data["user_phone"]
        user_p = UserProfileInfo.objects.get(phone_primary=phone)



        # order_list = Order.objects.filter(user_customer = user_p, order_status__code = GEN_Constants.ORDER_STATUS_AGENT_APPROVED).order_by('schedule_requested_time')
        order_list = Order.objects.filter(schedule_requested_time__gte = datetime.now()).order_by(
            'schedule_requested_time')
        order_list_s = CustomerAllOrderSerializer(order_list, many=True)


        base_data = {}
        base_data["order_list"] = order_list_s.data
        # base_data["delivery_text"] = "Order will bw delivered by 11 AM tomorrow"
        # base_data["status_text"] = "RECEIVED"

        return Response(base_data)

class CustomerOrderOthers(APIView):

    def post(self,request):
        received_json_data=json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)
        print("reee")
        print(received_json_data)

        phone = received_json_data["user_phone"]
        user_p = UserProfileInfo.objects.get(phone_primary=phone)
        # order_list = Order.objects.filter(user_customer = user_p).exclude(order_status__code = GEN_Constants.ORDER_STATUS_AGENT_APPROVED).order_by('-updated_at')
        order_list = Order.objects.filter(schedule_requested_time__lt = datetime.now()).order_by(
            'schedule_requested_time')

        order_list_s = CustomerAllOrderSerializer(order_list, many=True)


        base_data = {}
        base_data["order_list"] = order_list_s.data
        # base_data["delivery_text"] = "Order will bw delivered by 11 AM tomorrow"
        # base_data["status_text"] = "RECEIVED"

        return Response(base_data)



@csrf_exempt
def order_details(request):
    data = {"SUCCESS":True,"list":[{"card_type":"TITLE","data":{"title_text":"Recent Update"}},{"card_type":"PHONE","data":{"title":"Mr. Manigandan G","sub_title":"Dept Com of Police","phone":[9080349072,9020453454],"photo":"http://192.168.0.103:8000/media/profile_pics/user.png"}},{"card_type":"PHONE","data":{"title":"Mr. Manigandan G","sub_title":"Dept Com of Police","phone":[9080349072,9020453454],"photo":"http://192.168.0.103:8000/media/profile_pics/user.png"}},{"card_type":"SUB_TITLE","data":{"title_text":"Home Remidies"}},{"card_type":"Article","data":{"title":"Home Sanatizers","sub_title":"Steps to make sanatisers in home","URL":"https://www.healthline.com/health/how-to-make-hand-sanitizer","cover_photo":"http://192.168.0.103:8000/media/profile_pics/hand-sanitizer.jpg"}}]}

    return HttpResponse(json.dumps(data), content_type="application/json")

@csrf_exempt
def get_user_suggestion_list(request):
    phone = "908034"
    user_p = UserProfileInfo.objects.filter(phone_primary__startswith=phone)
    order_list_s =  UserProfileSuggestionSerializer(user_p, many=True)

    base_data = {}
    base_data["user_data"] = order_list_s.data

    # ORDER_STATUS[0]
    # base_data["status_text"] = "RECEIVED"
    return HttpResponse(json.dumps({"SUCCESS":False, "RESPONSE_DATA":base_data}),
        content_type="application/json")

@csrf_exempt
def validate_app(request):
        received_json_data=json.loads(request.body)

        print("resssa")
        print(received_json_data)
        # validate_app
        # return HttpResponse(json.dumps({"SUCCESS":False, "RESPONSE_DATA":{"partial":True, "url":"https://www.google.com/"}}),
        #     content_type="application/json")
        return HttpResponse(json.dumps({"SUCCESS":True, "RESPONSE_DATA":{"partial":False}}),
            content_type="application/json")



@csrf_exempt
def get_user_details(request):
    # phone = "9080349072"
    received_json_data=request.POST

    print("resssa")
    print(received_json_data)

    phone = received_json_data["phone"]
    user_p = UserProfileInfo.objects.get(phone_primary=phone)
    order_list_s =  UserProfileInfoSerializer(user_p, many=False)

    base_data = {}
    base_data["user_data"] = order_list_s.data

    # ORDER_STATUS[0]
    # base_data["status_text"] = "RECEIVED"
    return HttpResponse(json.dumps({"SUCCESS":False, "RESPONSE_DATA":base_data}),
        content_type="application/json")

@csrf_exempt
def product_list_suggestion(request):


    # received_json_data=json.loads(request.body)
    # #
    # phone = user["phone"]
    q = "ca"
    user_p = Product.objects.filter(name__contains=q)
# ProductSuggestionListSerializer
    order_list_s =  ProductSuggestionListSerializer(user_p, many=True)

    base_data = {}
    base_data["product_list"] = order_list_s.data

    # ORDER_STATUS[0]
    # base_data["status_text"] = "RECEIVED"
    return HttpResponse(json.dumps({"SUCCESS":False, "RESPONSE_DATA":base_data}),
        content_type="application/json")

def order_list_user(request):

    phone = user["phone"]
    # phone = "9080349072"
    user_p = UserProfileInfo.objects.get(phone_primary=phone)

    order_list = Order.objects.filter(user_customer = user_p).order_by('-updated_at')


    return HttpResponse(json.dumps(data_set), content_type="application/json")

    # return render(request, 'GEN/orders_list.html',  { 'orders': orders,  'measurements_list':measurements_list, 'state_list':state_list , 'order_status_list':order_status_list })


    # data = {"SUCCESS":True,"list":[{"card_type":"TITLE","data":{"title_text":"Recent Update"}},{"card_type":"PHONE","data":{"title":"Mr. Manigandan G","sub_title":"Dept Com of Police","phone":[9080349072,9020453454],"photo":"http://192.168.0.103:8000/media/profile_pics/user.png"}},{"card_type":"PHONE","data":{"title":"Mr. Manigandan G","sub_title":"Dept Com of Police","phone":[9080349072,9020453454],"photo":"http://192.168.0.103:8000/media/profile_pics/user.png"}},{"card_type":"SUB_TITLE","data":{"title_text":"Home Remidies"}},{"card_type":"Article","data":{"title":"Home Sanatizers","sub_title":"Steps to make sanatisers in home","URL":"https://www.healthline.com/health/how-to-make-hand-sanitizer","cover_photo":"http://192.168.0.103:8000/media/profile_pics/hand-sanitizer.jpg"}}]}
    #
    # return HttpResponse(json.dumps(data), content_type="application/json")




def getUser(phone):


    phone = user["phone"]
    user = UserProfileInfo.objects.get(phone_primary=phone)


    data = {"SUCCESS":True,"list":[{"card_type":"TITLE","data":{"title_text":"Recent Update"}},{"card_type":"PHONE","data":{"title":"Mr. Manigandan G","sub_title":"Dept Com of Police","phone":[9080349072,9020453454],"photo":"http://192.168.0.103:8000/media/profile_pics/user.png"}},{"card_type":"PHONE","data":{"title":"Mr. Manigandan G","sub_title":"Dept Com of Police","phone":[9080349072,9020453454],"photo":"http://192.168.0.106:8000/media/profile_pics/user.png"}},{"card_type":"SUB_TITLE","data":{"title_text":"Home Remidies"}},{"card_type":"Article","data":{"title":"Home Sanatizers","sub_title":"Steps to make sanatisers in home","URL":"https://www.healthline.com/health/how-to-make-hand-sanitizer","cover_photo":"http://192.168.0.103:8000/media/profile_pics/hand-sanitizer.jpg"}}]}

    return HttpResponse(json.dumps(data), content_type="application/json")

@csrf_exempt
def feed_news(request):
    data = {"SUCCESS": True, "list": [{"card_type": "INFO_NEUTRAL", "data":{"title_text": "Title", "details_text": "We are providing only the basic essentials because of the COVID19 situation. All the ondemand supplies will be provided up on order once the situation is over.", "bg_color": "#e58a8a"}}, {"card_type": "TITLE", "data": {"title_text": "Order From Home Details"}}, {"card_type": "PHONE", "data": {"title": "Mr. Manigandan G", "sub_title": "Delivery Agent", "phone": [9080349072, 9020453454], "photo": "http://192.168.0.103:8000/media/profile_pics/user.png"}}, {"card_type": "PHONE", "data": {"title": "Mr. Rahu G", "sub_title": "Business Agent", "phone": [9080349072, 9020453454], "photo": "http://192.168.0.106:8000/media/profile_pics/user.png"}}, {"card_type": "SUB_TITLE", "data": {"title_text": "COVID19 STATUS"}}, {"card_type": "ARTICLE", "data": {"title": "Coronavirus in Tamil", "sub_title": "Dr. V Ramasubramanian | Apollo Hospitals", "URL": "https://www.youtube.com/watch?v=ZezntM6IAvU", "cover_photo": "http://206.189.129.128:8000/media/profile_pics/maxresdefault.jpg"}}]}
    return HttpResponse(json.dumps(data), content_type="application/json")


@csrf_exempt
def feed_contact(request):

    received_json_data=json.loads(request.body)
    print(received_json_data)
    data = {"SUCCESS": True, "list": [{"card_type": "INFO_NEUTRAL", "data":{"title_text": "Notice", "details_text": "We are providing only the basic essentials because of the COVID19 situation. All the ondemand supplies will be provided up on order once the situation is over.", "bg_color": "#e58a8a"}}, {"card_type": "TITLE", "data": {"title_text": "Order From Home Details"}}, {"card_type": "PHONE", "data": {"title": "Ramesh", "sub_title": "Business Agent", "phone": [8144485556], "photo": "http://206.189.129.128:8000/media/profile_pics/user.png"}}]}
    # {"SUCCESS": True, "list": [{"card_type": "INFO_NEUTRAL", "data":{"title_text": "Notice", "details_text": "We are providing only the basic essentials because of the COVID19 situation. All the ondemand supplies will be provided up on order once the situation is over.", "bg_color": "#e58a8a"}}, {"card_type": "TITLE", "data": {"title_text": "Order From Home Details"}}, {"card_type": "PHONE", "data": {"title": "Mr. Manigandan G", "sub_title": "Delivery Agent", "phone": [9080349072, 9020453454], "photo": "http://206.189.129.128:8000/media/profile_pics/user.png"}}, {"card_type": "PHONE", "data": {"title": "Mr. Rahu G", "sub_title": "Business Agent", "phone": [9080349072, 9020453454], "photo": "http://192.168.0.106:8000/media/profile_pics/user.png"}}, {"card_type": "SUB_TITLE", "data": {"title_text": "COVID19 STATUS"}}, {"card_type": "ARTICLE", "data": {"title": "Coronavirus in Tamil", "sub_title": "Dr. V Ramasubramanian | Apollo Hospitals", "URL": "https://www.youtube.com/watch?v=ZezntM6IAvU", "cover_photo": "http://206.189.129.128:8000/media/profile_pics/maxresdefault.jpg"}}]}
    return HttpResponse(json.dumps(data), content_type="application/json")


@csrf_exempt
def submit_symptoms(request):

    received_json_data=json.loads(request.body)
    api_lang = get_api_language_preference(received_json_data)

    print(received_json_data)

    user =  received_json_data["user"]
    phone = user["phone"]

    symptom_list = received_json_data["symptom_list"]




    user = UserProfileInfo.objects.get(phone_primary=phone)

    symptom_total = 0

    for symptom_id in symptom_list:
        form_data = {}
        form_data["note"] = "Note"
        symptom = C19SymptomSet.objects.get(id=symptom_id)
        healh_form = UserHealthProfileForm(form_data)

        if healh_form.is_valid():

            symptom_total = symptom_total + int(symptom.seviarity)
            health = healh_form.save(commit=False)
            health.user = user
            health.symptom = symptom
            health.save()


    user.symptom_total = symptom_total
    user.save()

    # print("sypmtont");
    # print("sypmtont=="+str(symptom_total));

    return HttpResponse(json.dumps({"SUCCESS":True, "RESPONSE_MESSAGE":get_display_translated_value(value_constant.KEY_D_SAVED_SUCCESSFULLY,api_lang)}),
                        content_type="application/json")




@csrf_exempt
def change_user_status(request):


    print("came changestat")
    username = request.POST['username']
    user_status = request.POST['user_status']

    user_obj = User.objects.get(username=username)
    user_profile = UserProfileInfo.objects.get(user=user_obj)

    # user_profile = UserProfileInfo.objects.get(username=username)

    if user_status == "AT":
        print("useractive")
        user_status = dbconstants.USER_STATUS_DISABLED
    else:
        user_status = dbconstants.USER_STATUS_ACTIVE
        print("userinactive")
    user_profile.user_status = user_status
    user_profile.save()

    return HttpResponse(json.dumps({"SUCCESS":True, "RESPONSE_MESSAGE":"Status updated"}),
    content_type="application/json")



@csrf_exempt
def alter_order_item(request):
    if request.method == "GET":

         received_json_data = {"order_item_id" : "ODRHSXF1", "item_status":"CANCEL" }

         order_item = OrderItem.objects.get(order_item_id=received_json_data["order_item_id"])

         item_status = received_json_data["item_status"]

         item_status_to_update = order_item.status

         if item_status == "CANCEL":
             item_status_to_update =dbconstants.O_ITEM_REMOVED
         elif item_status == "REJECT":
             item_status_to_update =dbconstants.O_ITEM_REJECTED
         elif item_status == "NOT_AVAILABLE":
             item_status_to_update =dbconstants.O_ITEM_NOT_AVAILABLE


         order_item.status = item_status_to_update
         order_item.save()

    return HttpResponse(json.dumps({"SUCCESS":False, "RESPONSE_MESSAGE":"Status updated successfully"}),
        content_type="application/json")

# getSymptomSet
@csrf_exempt
def alter_order(request):

    if request.method == "GET":

         received_json_data = {"order_id" : "ODRHSXF1", "item_status":"CANCEL" }

         order_item = Order.objects.get(order_id=received_json_data["order_item_id"])

         item_status = received_json_data["item_status"]

         item_status_to_update = order_item.status

         if item_status == "CANCEL":
             item_status_to_update =dbconstants.ORDER_CANCELLED
         elif item_status == "PICKED":
             item_status_to_update =dbconstants.ORDER_PICKEDUP
         elif item_status == "CONFIRMED":
             item_status_to_update =dbconstants.ORDER_CONFIRMED_BY_CUSTOMER
         elif item_status == "DELIVERED":
             item_status_to_update =dbconstants.ORDER_DELIVERED

         order_item.status = item_status_to_update
         order_item.save()

    return HttpResponse(json.dumps({"SUCCESS":False, "RESPONSE_MESSAGE":"Status updated successfully"}),
        content_type="application/json")


# {
# "user":{"phone":9080349072,"location_lat":12.45345345,"location_long":12.98098098,"land_marr":"Near Ayyapan temple"},
# "item_list":[{"product_id":24, "uom_id":7,"quantity":5 },{"product_id":24, "uom_id":7,"quantity":5 }]
# }


class CreateOrder(APIView):


    def proceed_save(self, received_json_data):
        api_lang = get_api_language_preference(received_json_data)

        user_data_set = received_json_data["user"]
        order_data_set = received_json_data["order"]
        order_item_data_set_arr = received_json_data["order_item"]


        user_q = db_operations_support.get_db_object_g_last(UserProfileInfo,{"phone_primary" : user_data_set["phone"]})

        proceed_current_process_model = False
        order_base_id = -1
        if user_q is not None:
            user_customer_id = user_q.id
            order_data_set = received_json_data["order"]

            order_data_set_normalized = {}
            time_str = order_data_set["slot_time"]
            converted_date = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
            order_data_set_normalized["schedule_requested_time"] = converted_date
            order_data_set_normalized["user_customer"] = user_customer_id
            order_data_set_normalized["brand"] = order_data_set["brand_id"]
            order_data_set_normalized["branch"] = order_data_set["branch_id"]

            order_status_q = db_operations_support.get_db_object_g_last(OrderStatus, {"code": GEN_Constants.ORDER_STATUS_INITIATED})

            order_data_set_normalized["order_status"] = order_status_q.id

            order_data_set_normalized["order_id"] = support_db.unique_string_generator(Order, "order_id")

            proceed_current_process_model, serializer_current_process_model = support_serializer_submit.validate_save_instance(
                Order, order_data_set_normalized)
            order_base_id = serializer_current_process_model["id"]

            if proceed_current_process_model == False:
                print("order save error")
                print(serializer_current_process_model.errors)

        if proceed_current_process_model:

            for e_order_item_data_set in order_item_data_set_arr:

                item_breakdown_arr = e_order_item_data_set["item_breakdown"]

                servisable_product_q = db_operations_support.get_db_object_g_last(BranchServisableProduct, {
                    "id": e_order_item_data_set["servisable_product_id"]})

                for e_item_breakdown in item_breakdown_arr:

                    order_item_data_set_normalized = {}
                    order_item_data_set_normalized["order_item_id"] = support_db.unique_string_generator(OrderItem, "order_item_id")
                    order_item_data_set_normalized["order"] = order_base_id
                    order_item_data_set_normalized["status_note"] = "."
                    order_item_data_set_normalized["item_quantity"] = e_item_breakdown["qty"]

                    order_item_data_set_normalized["servisable_product"] = servisable_product_q.id
                    order_item_data_set_normalized["product"] = servisable_product_q.product.id
                    order_item_data_set_normalized["item_name"] = servisable_product_q.product.name
                    order_item_data_set_normalized["status_note"] = "."
                    order_item_data_set_normalized["brand_branch"] = servisable_product_q.branch.id
                    order_item_data_set_normalized["brand"] = servisable_product_q.branch.brand.id

                    print("reccbreakk")
                    print(e_item_breakdown)
                    order_item_data_set_normalized["measurement_unit"] = e_item_breakdown["uom_id"]

                    proceed_current_process_model, serializer_current_process_model = support_serializer_submit.validate_save_instance(
                        OrderItem, order_item_data_set_normalized)

                    if proceed_current_process_model == False:
                        print("item save error")


                        print(serializer_current_process_model.errors)

        if order_base_id != -1:
            update_order_request_to_branch_user(order_base_id)
        return proceed_current_process_model, {"title":get_display_translated_value(value_constant.KEY_D_BOOKING_FAILED,api_lang), "message":get_display_translated_value(value_constant.KEY_D_PLEASE_TRY_AFTER_SOME_TIME,api_lang)}

    def proceed_validation(self, received_json_data):

        api_lang = get_api_language_preference(received_json_data)

        proceed_current_process_model = True
        payload = {"title":get_display_translated_value(value_constant.KEY_D_SUCCESSFUL,api_lang), "message":get_display_translated_value(value_constant.KEY_D_BOOKING_REQUEST_CONFIRMATION,api_lang)}

        order_data_set = received_json_data["order"]
        time_str = order_data_set["slot_time"]
        brand_id = order_data_set["brand_id"]
        branch_id = order_data_set["branch_id"]


        schedule_requested_date_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")

        schedule_requested_day_of_week = schedule_requested_date_time.isoweekday()
        schedule_requested_time = schedule_requested_date_time.time()

        servicable_criteria_q = ServisableDaysCriteria.objects.filter(branch__id = branch_id, day_of_week = schedule_requested_day_of_week, is_online=True, is_available =True, service_start_time__lte=schedule_requested_time, service_end_time__gte=schedule_requested_time)

        if(servicable_criteria_q.count() == 0):
            proceed_current_process_model = False
            payload = {"title":get_display_translated_value(value_constant.KEY_D_BOOKING_FAILED,api_lang), "message":get_display_translated_value(value_constant.KEY_D_BRANCH_OPERATIONAL_SELECTE_TIME,api_lang)}


        if proceed_current_process_model:

            branch_q = BrandBranchBasicInfo.objects.get(id = branch_id)

            store_capacity = branch_q.store_capacity


            date_rec = schedule_requested_date_time.strftime("%Y-%m-%d ")
            date_time = schedule_requested_date_time.strftime("%m/%d/%Y, %H:%M:%S")
            schedule_requested_hour_str = schedule_requested_date_time.strftime("%H")

            filter_start_time_str = date_rec + schedule_requested_hour_str+":00:00"
            filter_end_time_str = date_rec + schedule_requested_hour_str+":59:59"

            filter_start_time = datetime.strptime(filter_start_time_str, "%Y-%m-%d %H:%M:%S")
            filter_end_time = datetime.strptime(filter_end_time_str, "%Y-%m-%d %H:%M:%S")
            Orders_q = Order.objects.filter(branch__id = branch_id,  order_accepted =True, schedule_requested_time__range=(filter_start_time, filter_end_time))
            Orders_q_data = Orders_q.values_list('id', flat=True)

            print(Orders_q_data)
            # Orders_q_data = [89, 92]

            filled_obj_data = OrderItem.objects.filter(order__id__in = Orders_q_data).aggregate(Sum('item_quantity'))
            print("filledcapacity")
            print(filled_obj_data)
            # {'item_quantity__sum': 6}

            filled_capacity = filled_obj_data["item_quantity__sum"]

            if(filled_capacity == None):
                filled_capacity = 0

            if(filled_capacity >= store_capacity):
                proceed_current_process_model = False
                payload = {"title":get_display_translated_value(value_constant.KEY_D_BOOKING_FAILED,api_lang),
                           "message":get_display_translated_value(value_constant.KEY_D_SELECTE_TIME_BOOKED,api_lang)}

        return proceed_current_process_model, payload

    def post(self,request):

        received_json_data=json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)
        print("rrrrrttttt")
        # print(received_json_data)
        # print("received_json_data")
        # print(received_json_dataa)

        proceed_current_process_model, payload  = self.proceed_validation(received_json_data)
        if proceed_current_process_model:
            proceed_current_process_model, payload  = self.proceed_save(received_json_data)

        if proceed_current_process_model:
            payload = {"title":get_display_translated_value(value_constant.KEY_D_SUCCESSFUL,api_lang), "message":get_display_translated_value(value_constant.KEY_D_BOOKING_REQUEST_CONFIRMATION,api_lang)}
            return HttpResponse(json.dumps({"SUCCESS":True, "RESPONSE_MESSAGE":payload}),
                content_type="application/json")
        else:
            return HttpResponse(
                json.dumps({"SUCCESS": False, "RESPONSE_MESSAGE": payload, "ERROR": payload}),
                content_type="application/json")




# @csrf_exempt
# def order_create_m(request):
#
#     if request.method == "POST":
#
#         print("camwww000000000000000000000001")
#
#         #
#         received_json_data = json.loads(request.body)
#         api_lang = get_api_language_preference(received_json_data)
#
#         user_data_set = received_json_data["user"]
#         order_data_set = received_json_data["order"]
#         order_item_data_set_arr = received_json_data["order_item"]
#
#
#         user_q = db_operations_support.get_db_object_g_last(UserProfileInfo,{"phone_primary" : user_data_set["phone"]})
#
#         proceed_current_process_model = False
#         order_base_id = -1
#         if user_q is not None:
#             user_customer_id = user_q.id
#             order_data_set = received_json_data["order"]
#
#             order_data_set_normalized = {}
#             time_str = order_data_set["slot_time"]
#             converted_date = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
#             order_data_set_normalized["schedule_requested_time"] = converted_date
#             order_data_set_normalized["user_customer"] = user_customer_id
#             order_data_set_normalized["brand"] = order_data_set["brand_id"]
#             order_data_set_normalized["branch"] = order_data_set["branch_id"]
#
#             order_status_q = db_operations_support.get_db_object_g_last(OrderStatus, {"code": GEN_Constants.ORDER_STATUS_INITIATED})
#
#             order_data_set_normalized["order_status"] = order_status_q.id
#
#             order_data_set_normalized["order_id"] = support_db.unique_string_generator(Order, "order_id")
#
#             proceed_current_process_model, serializer_current_process_model = support_serializer_submit.validate_save_instance(
#                 Order, order_data_set_normalized)
#             order_base_id = serializer_current_process_model["id"]
#
#             if proceed_current_process_model == False:
#                 print("order save error")
#                 print(serializer_current_process_model.errors)
#
#         if proceed_current_process_model:
#
#             for e_order_item_data_set in order_item_data_set_arr:
#
#                 order_item_data_set_normalized = {}
#                 order_item_data_set_normalized["order_item_id"] = support_db.unique_string_generator(OrderItem, "order_item_id")
#                 order_item_data_set_normalized["order"] = order_base_id
#                 order_item_data_set_normalized["status_note"] = "."
#                 order_item_data_set_normalized["item_quantity"] = e_order_item_data_set["quantity"]
#
#                 servisable_product_q = db_operations_support.get_db_object_g_last(BranchServisableProduct, {
#                     "id": e_order_item_data_set["servisable_product_id"]})
#
#                 order_item_data_set_normalized["servisable_product"] = servisable_product_q.id
#                 order_item_data_set_normalized["product"] = servisable_product_q.product.id
#                 order_item_data_set_normalized["item_name"] = servisable_product_q.product.name
#                 order_item_data_set_normalized["status_note"] = "."
#                 order_item_data_set_normalized["brand_branch"] = servisable_product_q.branch.id
#                 order_item_data_set_normalized["brand"] = servisable_product_q.branch.brand.id
#
#                 measurementunit_q = db_operations_support.get_db_object_g_last(ItemMeasuementUnit, {
#                     "name": e_order_item_data_set["uom"]})
#
#                 order_item_data_set_normalized["measurement_unit"] = measurementunit_q.id
#
#                 proceed_current_process_model, serializer_current_process_model = support_serializer_submit.validate_save_instance(
#                     OrderItem, order_item_data_set_normalized)
#
#                 if proceed_current_process_model == False:
#                     print("item save error")
#
#
#                     print(serializer_current_process_model.errors)
#
#         print("camwww000000000000000000000002")
#         if order_base_id != -1:
#             update_order_request_to_branch_user(order_base_id)
#         if proceed_current_process_model:
#             print("camwww000000000000000000000003")
#             return HttpResponse(json.dumps({"SUCCESS":True, "RESPONSE_MESSAGE":get_display_translated_value(value_constant.KEY_D_ORDER_PLACED_SUCCESSFULLY,api_lang)}),
#                 content_type="application/json")
#         else:
#             print("camwww000000000000000000000004")
#             return HttpResponse(
#                 json.dumps({"SUCCESS": False, "RESPONSE_MESSAGE": "Error", "ERROR": order_item_form.errors}),
#                 content_type="application/json")


# @csrf_exempt
# def order_create_m(request):
#
#     if request.method == "POST":
#
#         #
#         received_json_data = json.loads(request.body)
#
#         user_data_set = received_json_data["user"]
#         order_data_set = received_json_data["order"]
#         order_item_data_set_arr = received_json_data["order_item"]
#
#
#         user_q = db_operations_support.get_db_object_g_last(UserProfileInfo,{"phone_primary" : user_data_set["phone"]})
#
#         proceed_current_process_model = False
#         order_base_id = -1
#         if user_q is not None:
#             user_customer_id = user_q.id
#             order_data_set = received_json_data["order"]
#
#             order_data_set_normalized = {}
#             time_str = order_data_set["slot_time"]
#             converted_date = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
#             order_data_set_normalized["schedule_requested_time"] = converted_date
#             order_data_set_normalized["user_customer"] = user_customer_id
#             order_data_set_normalized["brand"] = order_data_set["brand_id"]
#             order_data_set_normalized["branch"] = order_data_set["branch_id"]
#
#             order_status_q = db_operations_support.get_db_object_g_last(OrderStatus, {"code": GEN_Constants.ORDER_STATUS_INITIATED})
#
#             order_data_set_normalized["order_status"] = order_status_q.id
#
#             order_data_set_normalized["order_id"] = support_db.unique_string_generator(Order, "order_id")
#
#             proceed_current_process_model, serializer_current_process_model = support_serializer_submit.validate_save_instance(
#                 Order, order_data_set_normalized)
#             order_base_id = serializer_current_process_model["id"]
#
#             if proceed_current_process_model == False:
#                 print("order save error")
#                 print(serializer_current_process_model.errors)
#
#         if proceed_current_process_model:
#
#             for e_order_item_data_set in order_item_data_set_arr:
#
#                 order_item_data_set_normalized = {}
#                 order_item_data_set_normalized["order_item_id"] = support_db.unique_string_generator(OrderItem, "order_item_id")
#                 order_item_data_set_normalized["order"] = order_base_id
#                 order_item_data_set_normalized["status_note"] = "."
#                 order_item_data_set_normalized["item_quantity"] = e_order_item_data_set["quantity"]
#
#                 servisable_product_q = db_operations_support.get_db_object_g_last(BranchServisableProduct, {
#                     "id": e_order_item_data_set["servisable_product_id"]})
#
#                 order_item_data_set_normalized["servisable_product"] = servisable_product_q.id
#                 order_item_data_set_normalized["product"] = servisable_product_q.product.id
#                 order_item_data_set_normalized["item_name"] = servisable_product_q.product.name
#                 order_item_data_set_normalized["status_note"] = "."
#                 order_item_data_set_normalized["brand_branch"] = servisable_product_q.branch.id
#                 order_item_data_set_normalized["brand"] = servisable_product_q.branch.brand.id
#
#                 measurementunit_q = db_operations_support.get_db_object_g_last(ItemMeasuementUnit, {
#                     "name": e_order_item_data_set["uom"]})
#
#                 order_item_data_set_normalized["measurement_unit"] = measurementunit_q.id
#
#                 proceed_current_process_model, serializer_current_process_model = support_serializer_submit.validate_save_instance(
#                     OrderItem, order_item_data_set_normalized)
#
#                 if proceed_current_process_model == False:
#                     print("item save error")
#
#
#                     print(serializer_current_process_model.errors)
#
#         if order_base_id != -1:
#             update_order_request_to_branch_user(order_base_id)
#         if proceed_current_process_model:
#             return HttpResponse(json.dumps({"SUCCESS":True, "RESPONSE_MESSAGE":"Order Placed Successfully"}),
#                 content_type="application/json")
#         else:
#             return HttpResponse(
#                 json.dumps({"SUCCESS": False, "RESPONSE_MESSAGE": "Error", "ERROR": order_item_form.errors}),
#                 content_type="application/json")

def update_order_request_to_branch_user(order_base_id):
    # received_json_data = json.loads(request.body)
    # api_lang = get_api_language_preference(received_json_data)
    print("recc-id")
    print(order_base_id)

    order_q = db_operations_support.get_db_object_g_last(Order, {"id": order_base_id})

    if order_q is not None:
        brand_id = order_q.brand.id
        branch_id = order_q.branch.id
        order_id = order_q.id
        print("order exist")
        print(branch_id)
        branch_agents_q = db_operations_support.get_db_object_g_list(UserProfileInfo, {"brandbranch__id": branch_id, "app_user_type__code":GEN_Constants.APP_USER_TYPE_BRANCH_AGENT, "is_available":True})
        # branch_agents_q = db_operations_support.get_db_object_g_list(UserProfileInfo, {"brandbranch__id": branch_id, "app_user_type__code":GEN_Constants.APP_USER_TYPE_BRANCH_AGENT})
        data_payload =  {"app_user_type" : GEN_Constants.APP_USER_TYPE_BRANCH_AGENT, "push_type" : "SCHEDULE_REQUEST", "order_id" : order_id}
        for e_branch_agent in branch_agents_q:
            print("eachua")
            print(e_branch_agent.phone_primary)
            proceedPush(brand_id, GEN_Constants.APP_USER_TYPE_BRANCH_AGENT, e_branch_agent.device_token,get_display_translated_value(value_constant.KEY_D_NEW_REQUEST), get_display_translated_value(value_constant.KEY_D_NEW_BOOKING_REQUEST_VIEW_DETAILS), data_payload)



@csrf_exempt
def order_create_m1(request):

    if request.method == "POST":

        #
        received_json_data=json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)
        print("resssa")
        print(received_json_data)
        # print(eeeesss)
        # received_json_data={"user":{"phone":9629283679,"location_lat":12.45345345,"location_long":12.98098098,"land_mark":"Near Ayyapan temple"},"item_list":[{"product_id":15, "uom_id":2,"quantity":5 },{"product_id":2, "uom_id":1,"quantity":5 }]}

        user = received_json_data["user"]
        item_list = received_json_data["item_list"]

        user_brand = user["brand_id"]
        user_brand_branch = user["branch_id"]

        # print(user)
        # print(user["land_mark"])

        user_profile = UserProfileInfo.objects.get(phone_primary=user["phone"])

        # order_form = IOrderForm(request.POST, request.FILES, instance=user)
                # fields = ('order_id', 'user_customer', 'delivery_charges')
        order_data = {}
        # order_data["order_id"] = "3343322"
        # order_form.user_customer = user
        order_data["delivery_charges"] = 0
        time_str = user["slot_time"]
        converted_date = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        order_data["schedule_requested_time"] = converted_date
        order_data["brand"] = converted_date
        # order_data["user_customer"] = user

        order_form = IOrderForm(order_data)
        # order_form.order_id = "3343322"

        brand_q = BrandBasicInfo.objects.get(id = user_brand)
        brand_branch_q = BrandBranchBasicInfo.objects.get(id = user_brand_branch)

        # order_form.delivery_charges = 20

        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.user_customer = user_profile
            order.brand = brand_q
            order.branch = brand_branch_q
            order.order_id = unique_order_id_generator(order)
            order.save()


            for item in item_list:

                # "product_id":24, "uom_id":7,"quantity":5
                        # fields = ('order_item_id', 'product' 'item_name', 'item_quantity', 'order', 'measurement_unit')
                order_item_data = {}

                print("cameotem")
                print(item)
                order_item_data["item_name"] = item['name']
                order_item_data["item_quantity"] = item['quantity']

                order_item_form = IOrderItemForm(order_item_data)

                if order_item_form.is_valid():


                    order_item = order_item_form.save(commit=False)
                    order_item.order = order
                    order_item.order_item_id = unique_order_item_id_generator(order_item)

                    if item['product_id']:
                        order_item.product = Product.objects.get(id = item['product_id'])
                    # print("eachit")
                    # print(order_item.product.measurement_unit[0])
                    # print(order_item.product.measurement_unit)
                    # order_item.measurement_unit = ItemMeasuementUnit.objects.get(id = item['uom_id'])
                    order_item.measurement_unit = ItemMeasuementUnit.objects.get(name = item['uom'])
                    # order_item.measurement_unit = order_item.product.measurement_unit[0]
                    order_item.save()

                    # fields = ('status', 'order_item')
                    order_item_log_data = {}
                    order_item_log_data["status"] = dbconstants.O_ITEM_PLACED

                    order_item_log_form = OrderItemLogForm(order_item_log_data)

                    if order_item_log_form.is_valid():
                        order_item_log = order_item_log_form.save(commit=False)
                        order_item_log.order_item = order_item
                        order_item_log.save()
                    #
                    return HttpResponse(json.dumps({"SUCCESS":True, "RESPONSE_MESSAGE":get_display_translated_value(value_constant.KEY_D_ORDER_PLACED_SUCCESSFULLY,api_lang)}),
                        content_type="application/json")
                    #     return HttpResponse(json.dumps({"SUCCESS":True, "RESPONSE_MESSAGE":"Order Placed Successfully"}),
                    #         content_type="application/json")
                    # else:
                    #
                    #     return HttpResponse(json.dumps({"SUCCESS":True, "RESPONSE_MESSAGE":"Order Placed Successfully2"}),
                    #         content_type="application/json")




                else:
                    return HttpResponse(json.dumps({"SUCCESS":False, "RESPONSE_MESSAGE":"Error", "ERROR":order_item_form.errors}),
                        content_type="application/json")


            order_log_data = {}
            order_log_data["status"] = dbconstants.ORDER_PLACED

            order_log_form = OrderLogForm(order_log_data)

            if order_log_form.is_valid():
                order_log = order_log_form.save(commit=False)
                order_log.order = order
                order_log.save()

                return HttpResponse(json.dumps({"SUCCESS":True, "RESPONSE_MESSAGE":get_display_translated_value(value_constant.KEY_D_ORDER_PLACED_SUCCESSFULLY,api_lang)}),
                    content_type="application/json")

                # print(item)

        else:
            return HttpResponse(json.dumps({"SUCCESS":False, "RESPONSE_MESSAGE":"Error", "ERROR":order_form.errors}),
                content_type="application/json")


    # return Response(base_data)


@csrf_exempt
def order_create(request):
        # received_json_data=json.loads(request.body)

        # print(request.POST)
        # if request.method == "POST":
        #     data = request.POST
        #
        #
        #
        #     return HttpResponse(json.dumps({"SUCCESS":False, "RESPONSE_MESSAGE":"Error", "ERROR":{"Name":"Error"}}),content_type="application/json")
        # else:
        #     return HttpResponse(json.dumps({"SUCCESS":False, "RESPONSE_MESSAGE":"Go F*uck yourself", "ERROR":{"Name":"Error"}}),content_type="application/json")


    if request.method == "POST":

        # json.loads(request.body)
        received_json_data=request.POST
        api_lang = get_api_language_preference(received_json_data)
        print("resssa")
        print(received_json_data)

        user = received_json_data["user"]
        item_list = received_json_data["item_list"]

        # print(user)
        # print(user["land_mark"])

        user_profile = UserProfileInfo.objects.get(phone_primary=user["phone"])

        # order_form = IOrderForm(request.POST, request.FILES, instance=user)
                # fields = ('order_id', 'user_customer', 'delivery_charges')
        order_data = {}
        # order_data["order_id"] = "3343322"
        # order_form.user_customer = user
        order_data["delivery_charges"] = 20
        # order_data["user_customer"] = user

        order_form = IOrderForm(order_data)
        # order_form.order_id = "3343322"

        # order_form.delivery_charges = 20

        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.user_customer = user_profile
            order.order_id = unique_order_id_generator(order)
            order.save()


            for item in item_list:

                # "product_id":24, "uom_id":7,"quantity":5
                        # fields = ('order_item_id', 'product' 'item_name', 'item_quantity', 'order', 'measurement_unit')
                order_item_data = {}

                print("cameotem")
                print(item)
                order_item_data["item_name"] = "test"
                order_item_data["item_quantity"] = item['quantity']

                order_item_form = IOrderItemForm(order_item_data)

                if order_item_form.is_valid():


                    order_item = order_item_form.save(commit=False)
                    order_item.order = order
                    order_item.order_item_id = unique_order_item_id_generator(order_item)
                    order_item.product = Product.objects.get(id = item['product_id'])
                    print("eachit")
                    # print(item['uom_id'])
                    print(order_item.product.measurement_unit)
                    # order_item.measurement_unit = ItemMeasuementUnit.objects.get(id = item['uom_id'])
                    order_item.measurement_unit = order_item.product.measurement_unit
                    order_item.save()

                    # fields = ('status', 'order_item')
                    order_item_log_data = {}
                    order_item_log_data["status"] = dbconstants.O_ITEM_PLACED

                    order_item_log_form = OrderItemLogForm(order_item_log_data)

                    if order_item_log_form.is_valid():
                        order_item_log = order_item_log_form.save(commit=False)
                        order_item_log.order_item = order_item
                        order_item_log.save()






                else:
                    return HttpResponse(json.dumps({"SUCCESS":False, "RESPONSE_MESSAGE":"Error", "ERROR":order_item_form.errors}),
                        content_type="application/json")


            order_log_data = {}
            order_log_data["status"] = dbconstants.ORDER_PLACED

            order_log_form = OrderLogForm(order_log_data)

            if order_log_form.is_valid():
                order_log = order_log_form.save(commit=False)
                order_log.order = order
                order_log.save()


                # print(item)

        else:
            return HttpResponse(json.dumps({"SUCCESS":False, "RESPONSE_MESSAGE":"Error", "ERROR":order_form.errors}),
                content_type="application/json")



# unique_order_id_generator

            # order = CMN_CommunicationPhysicalModel.objects.get(slug=CMN_CommunicationPhysicalModel_data["slug"])
            # serializer_communication_physical = CMN_CommunicationPhysicalModelSerializer(instance = order_obj, data=CMN_CommunicationPhysicalModel_data, partial=True)






    # return HttpResponse(json.dumps({"SUCCESS":True, "RESPONSE_MESSAGE":"Status updated"}),
    #     content_type="application/json")


@csrf_exempt
def change_product_status(request):

    print(request.POST)

    product_id = request.POST['product_id']
    status = request.POST['status']
    product = Product.objects.get(id=product_id)

    print("camerr")

    user_status = True

    if status == "ENABLE":
        print("useractive")
        user_status = True
    else:
        user_status = False
        print("userinactive")
    product.is_available = user_status
    product.save()

    return HttpResponse(json.dumps({"SUCCESS":True, "RESPONSE_MESSAGE":"Status updated"}),
    content_type="application/json")



@csrf_exempt
def authenticate_app_user(request):

    if request.method == "POST":

        received_json_data=json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)

        print("recdd")
        print(received_json_data)
        user_name = received_json_data["user_name"]
        password = received_json_data["password"]
        device_token = received_json_data["device_token"]


        user_profile1 = UserProfileInfo.objects.filter(app_user_name=user_name, password = password)

        print("came23332")
        if not user_profile1:
            print("came2333")
            return HttpResponse(json.dumps({"SUCCESS":False, "RESPONSE_MESSAGE":"Invalid User Name/Password"}), content_type="application/json")
        else:
            user_profile = UserProfileInfo.objects.get(app_user_name=user_name, password = password)
            # lang = received_json_data["user_lang"]
            # user_profile.user_language = lang
            # user_profile.save()
            #
            # print("rec_un")
            user_name = str(user_profile.user)
            # print(user_name)
            user = User.objects.get(username = user_name)



            user_data = {}
            user_data["name"] = user.first_name
            user_data["user_type"] = user_profile.app_user_type.code
            user_data["brand_id"] = user_profile.brand.id
            user_data["user_id"] = user_profile.id
            if user_profile.brandbranch is not None:
                user_data["brand_branch_id"] = user_profile.brandbranch.id
            else:
                user_data["brand_branch_id"] = -1
            user_profile.device_token = device_token
            user_profile.save()
            return HttpResponse(json.dumps({"SUCCESS":True, "RESPONSE_DATA": user_data, "RESPONSE_MESSAGE":get_display_translated_value(value_constant.KEY_D_LOGIN_SUCCESSFUL,api_lang)}), content_type="application/json")

@csrf_exempt
def validate_user(request):

    if request.method == "POST":

        received_json_data=json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)

        print("recdd")
        print(received_json_data)
        phone = received_json_data["phone"]
        brand_code = received_json_data["brand_code"]


        user_profile1 = UserProfileInfo.objects.filter(phone_primary=phone)
        brand_c = BrandBasicInfo.objects.get(code=brand_code)


        if not user_profile1:

            response_data = {}
            response_data["brand_id"] = brand_c.id

            return HttpResponse(json.dumps({"SUCCESS":False, "RESPONSE_DATA": response_data,  "RESPONSE_MESSAGE":"User Not Exist"}), content_type="application/json")
        else:
            user_profile = UserProfileInfo.objects.get(phone_primary=phone)
            lang = received_json_data["user_lang"]
            user_profile.user_language = lang
            user_profile.save()

            print("rec_un")
            user_name = str(user_profile.user)
            print(user_name)
            user = User.objects.get(username = user_name)
            user_data = {}
            user_data["name"] = user.first_name
            user_data["location_latitude"] = user_profile.location_latitude
            user_data["location_longitude"] = user_profile.location_latitude
            user_data["user_id"] = user_profile.id
            user_data["brand_id"] = brand_c.id

            brand_details = {}
            brand_details["brand_name"] = brand_c.name
            brand_details["contact"] = ""
            brand_details["code"] = brand_c.id
            user_data["brand_details"] = brand_details


            return HttpResponse(json.dumps({"SUCCESS":True, "RESPONSE_DATA": user_data, "RESPONSE_MESSAGE":"User Exist"}), content_type="application/json")


@csrf_exempt
def change_order_status(request):

    print("camemee")

    orderid = request.POST['order_id']
    orderstatus = request.POST['order_status']

    order_obj = Order.objects.get(order_id=orderid)
    updated_order_sataus=""
    for key, value in dbconstants.ORDER_STATUS:
        if value == orderstatus:
            updated_order_sataus= key
    order_obj.status = updated_order_sataus
    order_obj.save()

    return HttpResponse(json.dumps({"SUCCESS":True, "RESPONSE_MESSAGE":"Order status updated"}),
    content_type="application/json")






@csrf_exempt
def register_business_agent(request):

    if request.method == "POST":

        received_json_data=json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)

        phone = received_json_data["phone"]
        name = received_json_data["name"]


        user = UserProfileInfo.objects.filter(phone_primary=phone)

        if not user:
            user_name_t = name.replace(" ", "_")
            user_name = createUserName(user_name_t)

            print("user_name")
            print(received_json_data)

            user_data = {}
            user_data["first_name"] = name
            user_data["username"] = user_name
            user_data["email"] = user_data["username"]+"@mycity.com"
            user_data["password"] = user_data["username"]+"@123"

            user_profile_data = {}
            user_profile_data["phone_primary"] = phone


            user_profile_data["age"] = 25
            user_profile_data["gender"] = received_json_data["gender"][0]


            # user_profile_data["phone_secondary"] = received_json_data["whatsapp"]

            # if "user_language" in received_json_data:
            #     user_data["user_language"] = received_json_data["user_language"]

            # user_data["location_area"] = received_json_data["location_area"]

            #
            # if "location_sublocality" in received_json_data:
            #     if received_json_data["location_sublocality"] != "":
            #         user_data["location_sublocality"] = received_json_data["location_sublocality"]
            #     else:
            #         user_data["location_sublocality"] = "NOT AVAILABLE"
            #
            # else:
            #     user_data["location_sublocality"] = "NOT AVAILABLE"

            #
            # if "location_locality" in received_json_data:
            #     if received_json_data["location_sublocality"] != "":
            #         user_data["location_locality"] = received_json_data["location_locality"]
            #     else:
            #         user_data["location_locality"] = "NOT AVAILABLE"
            # else:
            #     user_data["location_locality"] = "NONE"
            #
            #
            # if "location_city" in received_json_data:
            #     user_data["location_city"] = received_json_data["location_city"]
            # else:
            #     user_data["location_city"] = "NONE"
            #
            # user_data["location_state"] = received_json_data["location_state"]
            #
            # user_data["location_pincode"] = received_json_data["pincode"]
            #
            # user_data["location_latitude"] = received_json_data["location_latitude"]
            # user_data["location_longitude"] = received_json_data["location_longitude"]
            #


            # print("serrrddaa")
            # print(user_data)

            # user_form = UserFormCustomer(user_data)
            # profile_form = UserProfileInfoForm(data=user_data)
            #
            # if user_form.is_valid() and profile_form.is_valid() :
            #
            #     user = user_form.save()
            #     user.set_password(user.password)
            #     user = user_form.save()
            #     user.save()
            #
            #     profile = profile_form.save(commit=False)
            #     # profile.ref_id = unique_ref_id_generator(profile)
            #     profile.user = user
            #
            #     profile.save()
            # else:
            #     print("errorsa")
            #     print(user_form.errors)
            #     print(profile_form.errors)
            #     return HttpResponse(json.dumps({"SUCCESS":False, "RESPONSE_MESSAGE":"Error", "ERROR":profile_form.errors} ), content_type="application/json")

            return HttpResponse(json.dumps({"SUCCESS":True, "RESPONSE_MESSAGE":get_display_translated_value(value_constant.KEY_D_USER_CREATED_SUCCESSFULLY,api_lang)}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"SUCCESS":False, "RESPONSE_MESSAGE":"User2 already Exist"}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"SUCCESS":False, "RESPONSE_MESSAGE":"User3 already Exist"}), content_type="application/json")





@csrf_exempt
def RegisterAgent(request):

    if request.method == "POST":

        received_json_data=json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)

        phone = received_json_data["phone"]
        name = received_json_data["name"]
        brandbranch_id = received_json_data["brand_branch_id"]
        brand_id = received_json_data["brand_id"]


        user = UserProfileInfo.objects.filter(phone_primary=phone)

        if not user:
            user_name_t = name.replace(" ", "_")
            user_name = createUserName(user_name_t)

            print("user_name")
            print(received_json_data)

            user_data = {}
            user_data["first_name"] = name
            user_data["username"] = received_json_data["username"]
            user_data["email"] = user_data["username"]+"_agent@safez.com"
            user_data["password"] = received_json_data["password"]
            user_data["phone_primary"] = phone
            user_data["phone_secondary"] = received_json_data["whatsapp"]

            if "user_language" in received_json_data:
                user_data["user_language"] = received_json_data["user_language"]

            user_data["location_area"] = received_json_data["location_area"]


            if "location_sublocality" in received_json_data:
                if received_json_data["location_sublocality"] != "":
                    user_data["location_sublocality"] = received_json_data["location_sublocality"]
                else:
                    user_data["location_sublocality"] = "NOT AVAILABLE"

            else:
                user_data["location_sublocality"] = "NOT AVAILABLE"


            if "location_locality" in received_json_data:
                if received_json_data["location_sublocality"] != "":
                    user_data["location_locality"] = received_json_data["location_locality"]
                else:
                    user_data["location_locality"] = "NOT AVAILABLE"
            else:
                user_data["location_locality"] = "NONE"


            if "location_city" in received_json_data:
                user_data["location_city"] = received_json_data["location_city"]
            else:
                user_data["location_city"] = "NONE"

            user_data["location_state"] = received_json_data["location_state"]

            user_data["location_pincode"] = received_json_data["pincode"]

            user_data["location_latitude"] = received_json_data["location_latitude"]
            user_data["location_longitude"] = received_json_data["location_longitude"]


            user_data["age"] = received_json_data["age"]
            user_data["gender"] = received_json_data["gender"][0]

            print("serrrddaa")
            print(user_data)

            # user_data
            user_form = UserFormCustomer(user_data)
            profile_form = UserProfileInfoForm(data=user_data)

            if user_form.is_valid() and profile_form.is_valid() :

                user = user_form.save()
                user.set_password(user.password)
                user = user_form.save()
                user.save()

                profile = profile_form.save(commit=False)
                # profile.ref_id = unique_ref_id_generator(profile)
                profile.password = received_json_data["password"]
                profile.app_user_name = received_json_data["username"]
                profile.user = user
                user_type_q = db_operations_support.get_db_object_g(AppUserType, {"code" : GEN_Constants.APP_USER_TYPE_BRANCH_AGENT})
                profile.app_user_type = user_type_q
                brand_q = db_operations_support.get_db_object_g(BrandBasicInfo, {"id" : brand_id})
                profile.brand = brand_q
                brandbranch_q = db_operations_support.get_db_object_g(BrandBranchBasicInfo, {"id" : brandbranch_id})
                profile.brandbranch = brandbranch_q

                profile.save()
            else:
                print("errorsa")
                print(user_form.errors)
                print(profile_form.errors)
                return HttpResponse(json.dumps({"SUCCESS": False, "RESPONSE_MESSAGE": "User with this 'UserName' or 'Login UserName' already exist. Please try some other Name"}), content_type="application/json")
                # return HttpResponse(json.dumps({"SUCCESS":False, "RESPONSE_MESSAGE":"Error", "ERROR":profile_form.errors} ), content_type="application/json")

            return HttpResponse(json.dumps({"SUCCESS":True, "RESPONSE_MESSAGE":get_display_translated_value(value_constant.KEY_D_USER_CREATED_SUCCESSFULLY,api_lang)}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"SUCCESS":False, "RESPONSE_MESSAGE":"User with this Mobile number already Exist"}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"SUCCESS":False, "RESPONSE_MESSAGE":"Error Occured"}), content_type="application/json")

@csrf_exempt
def register_user(request):

    if request.method == "POST":

        received_json_data=json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)

        phone = received_json_data["phone"]
        name = received_json_data["name"]
        device_token = received_json_data["device_token"]


        user = UserProfileInfo.objects.filter(phone_primary=phone)

        if not user:

            response_data = {}
            user_name_t = name.replace(" ", "_")
            user_name = createUserName(user_name_t)
            password = user_name + "@123"
            print("user_name")
            print(received_json_data)



            user_data = {}
            user_data["first_name"] = name
            user_data["username"] = user_name
            user_data["email"] = user_data["username"]+"@mycity.com"
            user_data["password"] = password
            user_data["phone_primary"] = phone
            user_data["device_token"] = device_token
            user_data["phone_secondary"] = phone
                # received_json_data["whatsapp"]
            brand_id = received_json_data["brand_id"]

            if "user_language" in received_json_data:
                user_data["user_language"] = received_json_data["user_language"]



            if "location_area" in received_json_data:
                if received_json_data["location_area"] != "":
                    user_data["location_area"] = received_json_data["location_area"]
                else:
                    user_data["location_area"] = "NOT AVAILABLE"

            else:
                user_data["location_area"] = "NOT AVAILABLE"

            if "location_sublocality" in received_json_data:
                if received_json_data["location_sublocality"] != "":
                    user_data["location_sublocality"] = received_json_data["location_sublocality"]
                else:
                    user_data["location_sublocality"] = "NOT AVAILABLE"

            else:
                user_data["location_sublocality"] = "NOT AVAILABLE"


            if "location_locality" in received_json_data:
                if received_json_data["location_sublocality"] != "":
                    user_data["location_locality"] = received_json_data["location_locality"]
                else:
                    user_data["location_locality"] = "NOT AVAILABLE"
            else:
                user_data["location_locality"] = "NONE"


            if "location_city" in received_json_data:
                user_data["location_city"] = received_json_data["location_city"]
            else:
                user_data["location_city"] = "NONE"

            # user_data["location_state"] = received_json_data["location_state"]
            user_data["location_state"] = "NONE"

            user_data["location_pincode"] = received_json_data["pincode"]

            user_data["location_latitude"] = 0.0
            user_data["location_longitude"] = 0.0
            # user_data["location_latitude"] = received_json_data["location_latitude"]
            # user_data["location_longitude"] = received_json_data["location_longitude"]


            user_data["age"] = received_json_data["age"]
            user_data["gender"] = received_json_data["gender"][0]

            # print("serrrddaa")
            # print(user_data)

            user_form = UserFormCustomer(user_data)
            profile_form = UserProfileInfoForm(data=user_data)
            profile = None
            if user_form.is_valid() and profile_form.is_valid() :

                user = user_form.save()
                user.set_password(user.password)
                user = user_form.save()
                user.save()

                profile = profile_form.save(commit=False)
                # profile.ref_id = unique_ref_id_generator(profile)
                profile.user = user


                profile.password = password
                profile.app_user_name = user_name
                profile.user = user
                user_type_q = db_operations_support.get_db_object_g(AppUserType, {"code" : GEN_Constants.APP_USER_TYPE_CUSTOMER})
                profile.app_user_type = user_type_q
                brand_q = db_operations_support.get_db_object_g(BrandBasicInfo, {"id" : brand_id})
                profile.brand = brand_q



                profile.save()
                #
                # user_data["user_id"] = user_profile.id
                # user_data["brand_id"] = brand_c.id

                # user = User.objects.get(username=user_name)

                # user_data = {}
                response_data["name"] = user.first_name
                response_data["user_type"] = profile.app_user_type.code
                response_data["brand_id"] = profile.brand.id
                response_data["user_id"] = profile.id
                response_data["brand_branch_id"] = -1

            else:
                print("errorsa")
                print(profile_form.errors)
                print(user_form.errors)
                return HttpResponse(json.dumps({"SUCCESS":False, "RESPONSE_DATA":user_data, "RESPONSE_MESSAGE":"Error", "ERROR":profile_form.errors} ), content_type="application/json")

            # print(profile_form.errors)
            response_data["id"] = profile.id

            return HttpResponse(json.dumps({"SUCCESS":True, "RESPONSE_DATA":response_data, "RESPONSE_MESSAGE":get_display_translated_value(value_constant.KEY_D_USER_CREATED_SUCCESSFULLY,api_lang)}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"SUCCESS":False, "RESPONSE_MESSAGE":"User2 already Exist"}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"SUCCESS":False, "RESPONSE_MESSAGE":"User3 already Exist"}), content_type="application/json")


def unique_order_item_id_generator(instance, new_ref_id=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    if new_ref_id is not None:
        ref_id = new_ref_id
    else:
        ref_id = random_string_generator(size=11)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(order_item_id=ref_id).exists()
    if qs_exists:
        new_ref_id = random_string_generator(size=11)
        # "{ref_id}-{randstr}".format(
        #             ref_id=ref_id,
        #             randstr=random_string_generator(size=8, chars=string.ascii_uppercase)
        #         )
        return unique_order_item_id_generator(instance, order_item_id=new_ref_id)
    return ref_id


def unique_order_id_generator(instance, new_ref_id=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    if new_ref_id is not None:
        ref_id = new_ref_id
    else:
        ref_id = random_string_generator(size=11)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(order_id=ref_id).exists()
    if qs_exists:
        new_ref_id = random_string_generator(size=11)
        # "{ref_id}-{randstr}".format(
        #             ref_id=ref_id,
        #             randstr=random_string_generator(size=8, chars=string.ascii_uppercase)
        #         )
        return unique_order_id_generator(instance, order_id=new_ref_id)
    return ref_id


def unique_ref_id_generator(instance, new_ref_id=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    if new_ref_id is not None:
        ref_id = new_ref_id
    else:
        ref_id = "USER_"+random_string_generator(size=5)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(ref_id=ref_id).exists()
    if qs_exists:
        new_ref_id = constants.REF_ID_PREF_DELIVERY_AGENT+random_string_generator(size=5)
        # "{ref_id}-{randstr}".format(
        #             ref_id=ref_id,
        #             randstr=random_string_generator(size=8, chars=string.ascii_uppercase)
        #         )
        return unique_ref_id_generator(instance, new_ref_id=new_ref_id)
    return ref_id


def createUserName(username):
    username_f = username
    user_check = User.objects.filter(username=username)
    count = 1

    while user_check.count() != 0:
        username_f = username+str(count)
        user_check = User.objects.filter(username=username_f)
        count = count+1
    return username_f



class SymptomSet(APIView):

    # def get(self,request):


    def get(self,request):

        category =  C19SymptomSet.objects.filter(is_available=True)
        serializer_cat = C19SymptomSetSerializer(category, many=True)

        base_data = {}


        base_data["symptomset"] = serializer_cat.data

        return Response(base_data)



# @csrf_exempt
# def getSymptomSet(request):
#
#     symptoms = C19SymptomSet.objects.filter(is_available=True)
#     #
#     # serializer = C19SymptomSetSerializer(symptoms, many=True)
#     #
#     # # return Response(serializer)
#     # # serialized_obj = serializers.serialize('json', [ serializer])
#
#     return HttpResponse(json.dumps({"SUCCESS":True, "Data":symptoms}),
#         content_type="application/json")
#

class StoreBranchListAdmin(APIView):

    def post(self,request):
        received_json_data = request.POST
        api_lang = get_api_language_preference(received_json_data)
        print(":cameggg");

        category = BrandBranchBasicInfo.objects.all()
        serializer_cat = BrandBranchBasicInfoSerializerAD(category, many=True)

        base_data = {}
        base_data["branchlist"] = serializer_cat.data

        return Response(base_data)


class StoreBranchList(APIView):

    def get(self,request):
        print(":cameggg");
        #
        category = BrandBranchBasicInfo.objects.filter(is_available=True)
        serializer_cat = BrandBranchBasicInfoSerializer(category, many=True)

        base_data = {}
        base_data["branchlist"] = serializer_cat.data

        return Response(base_data)

    def post(self,request):
        print(":cameggg");

        category = BrandBranchBasicInfo.objects.filter(is_available=True)
        serializer_cat = BrandBranchBasicInfoSerializer(category, many=True)

        base_data = {}
        base_data["branchlist"] = serializer_cat.data

        return Response(base_data)

class BranchAgentList(APIView):
# class ProductList(APIView):

    def post(self,request):
        received_json_data = json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)
        #
        brand_id = received_json_data["brand_id"]
        brand_branch_id = received_json_data["brand_branch_id"]
        print(":cameggg");

        print(received_json_data);
        # branch_id = "1"


        brand_agent_list = UserProfileInfo.objects.filter(brand__id = brand_id, brandbranch__id = brand_branch_id, app_user_type__code = GEN_Constants.APP_USER_TYPE_BRANCH_AGENT).order_by('-created_at')
        serializer_brand_agent_list = BranchAgentListSerializer(brand_agent_list, context={"language":"en"}, many=True)

        base_data = {}
        base_data["agent_list"] = serializer_brand_agent_list.data

        return Response(base_data)


class BranchProductListCustomer1(APIView):
# class ProductList(APIView):

    def post(self,request):
        received_json_data = json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)
        #
        branch_id = received_json_data["branch_id"]
        print(":cameggg");

        print(received_json_data);
        # branch_id = "1"


        category_servisable = BranchServisableCategory.objects.filter(branch__id = branch_id).values_list('product_category__id', flat=True)
        product_base_servisable = BranchServisableProductBase.objects.filter(branch__id = branch_id, product_base__product_category__in=category_servisable).values_list('product_base__id', flat=True)
        product_servisable = BranchServisableProduct.objects.filter(branch__id = branch_id, product__product_base__product_category__in=category_servisable).values_list('product__id', flat=True)

        print("recc aa")
        print(category_servisable)

        category = ProductCategory.objects.filter(id__in=category_servisable)
        # category_ids = ProductCategory.objects.filter(id__in=category_servisable).values_list('id', flat=True)
        # category = ProductCategory.objects.filter(is_available=True)
        serializer_cat = ProductCategorySerializer(category, many=True)

        product = Product.objects.filter(id__in = product_servisable).order_by('-priority')

        # user = UserProfileInfo.objects.get(phone_primary=phone)

        serializer_pro = ProductSerializer(product, context={"language":"en"},   many=True)

        product_base = ProductBase.objects.filter(id__in = product_base_servisable)
        serializer_pro_base = ProductBaseSerializer(product_base, many=True)

        itemMeasuementUnit_base = ItemMeasuementUnit.objects.filter(is_available=True)
        serialiser_itemMeasuementUnit_base = ItemMeasuementUnitSerializer(itemMeasuementUnit_base, many=True)

        base_data = {}

        base_data["uom"] = serialiser_itemMeasuementUnit_base.data
        base_data["category"] = serializer_cat.data
        base_data["product"] = serializer_pro.data
        base_data["product_base"] = serializer_pro_base.data

        return Response(base_data)

class BranchProductSupportDataCustomer(APIView):
    def post(self,request):
        received_json_data = json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)
        #
        brand_id = received_json_data["brand_id"]
        branch_id = received_json_data["branch_id"]
        print(":cameggg");

        print(received_json_data);
        # branch_id = "1"

        category_servisable = BranchServisableCategory.objects.filter(is_available=True, product_category__is_available=True, is_online=True, branch__id = branch_id).values_list('product_category__id', flat=True)
        product_base_servisable = BranchServisableProductBase.objects.filter(is_available = True, is_online=True, branch__id = branch_id, product_base__product_category__in=category_servisable).values_list('product_base__id', flat=True)


        category = ProductCategory.objects.filter(id__in=category_servisable)
        # category_ids = ProductCategory.objects.filter(id__in=category_servisable).values_list('id', flat=True)
        # category = ProductCategory.objects.filter(is_available=True)
        serializer_cat = ProductCategorySerializer(category, many=True)
        product_base = ProductBase.objects.filter(id__in = product_base_servisable)


        itemMeasuementUnit_base = ItemMeasuementUnit.objects.filter(is_available=True, brand__id = brand_id)
        serialiser_itemMeasuementUnit_base = ItemMeasuementUnitSerializer(itemMeasuementUnit_base, many=True)

        serializer_pro_base = ProductBaseSerializer(product_base, many=True)

        base_data = {}

        base_data["uom"] = serialiser_itemMeasuementUnit_base.data
        base_data["category"] = serializer_cat.data
        base_data["product_base"] = serializer_pro_base.data

        return Response(base_data)

class BranchProductListCustomer(APIView):

    def post(self,request):

        received_json_data = json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)
        brand_id = received_json_data["brand_id"]
        branch_id = received_json_data["branch_id"]
        category_id = received_json_data["category_id"]

        if "page_no" in received_json_data:
            page_no = received_json_data["page_no"]
        else:
            page_no = 1


        if category_id == -1:
            category_servisable = BranchServisableCategory.objects.filter(is_available=True, product_category__is_available=True, is_online=True, branch__id = branch_id).values_list('product_category__id', flat=True)
            # product_base_servisable = BranchServisableProductBase.objects.filter(is_available = True, is_online=True, branch__id = branch_id, product_base__product_category__in=category_servisable).values_list('product_base__id', flat=True)
            product_servisable = BranchServisableProduct.objects.filter(is_available=True,product__is_available=True, is_online=True, branch__id = branch_id, product__product_base__product_category__in=category_servisable)
        else:
            print("came categvvv")
            product_servisable = BranchServisableProduct.objects.filter(is_available=True,product__is_available=True, is_online=True, branch__id = branch_id, product__product_base__product_category__id=category_id)

        product_servisable = get_paginated_data(product_servisable, page_no)
        serializer_pro = ServisableProductSerializerCustomer(product_servisable, context={"language":"en"},   many=True)
        base_data = {}
        base_data["product"] = serializer_pro.data

        return Response(base_data)

class BranchProductListAdmin2(APIView):

    def post(self,request):

        received_json_data = json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)
        brand_id = received_json_data["brand_id"]

        category_id = received_json_data["category_id"]

        if "page_no" in received_json_data:
            page_no = received_json_data["page_no"]
        else:
            page_no = 1


        if category_id == -1:
            product_servisable = Product.objects.all()
        else:
            product_servisable = Product.objects.filter(product_base__product_category=category_id)

        product_servisable = get_paginated_data(product_servisable, page_no)
        serializer_pro = ProductADFeedSerializer(product_servisable, context={"language":"en"},   many=True)
        base_data = {}
        base_data["product"] = serializer_pro.data

        return Response(base_data)

def get_paginated_data(queyset, page_no, page_size = GEN_Constants.ORDERS_LIST_COUNT_BUSINESS):
    # size = queyset.count()
    end = page_no * page_size+1
    start = end-page_size
    queryset = queyset[start-1:end]
    return queryset






# class BranchProductListCustomer(APIView):
#
#     def post(self,request):
#         received_json_data = json.loads(request.body)
#         #
#         branch_id = received_json_data["branch_id"]
#         print(":cameggg");
#
#         print(received_json_data);
#         # branch_id = "1"
#
#
#         category_servisable = BranchServisableCategory.objects.filter(is_available=True, product_category__is_available=True, is_online=True, branch__id = branch_id).values_list('product_category__id', flat=True)
#         product_base_servisable = BranchServisableProductBase.objects.filter(is_available = True, is_online=True, branch__id = branch_id, product_base__product_category__in=category_servisable).values_list('product_base__id', flat=True)
#         product_servisable = BranchServisableProduct.objects.filter(is_available=True,product__is_available=True, is_online=True, branch__id = branch_id, product__product_base__product_category__in=category_servisable)
#             # .values_list('product__id', flat=True)
#
#         print("recc aa")
#         print(category_servisable)
#
#         category = ProductCategory.objects.filter(id__in=category_servisable)
#         # category_ids = ProductCategory.objects.filter(id__in=category_servisable).values_list('id', flat=True)
#         # category = ProductCategory.objects.filter(is_available=True)
#         serializer_cat = ProductCategorySerializer(category, many=True)
#
#         # product = Product.objects.filter(id__in = product_servisable).order_by('-priority')
#
#         # user = UserProfileInfo.objects.get(phone_primary=phone)
#
#         serializer_pro = ServisableProductSerializerCustomer(product_servisable, context={"language":"en"},   many=True)
#
#         product_base = ProductBase.objects.filter(id__in = product_base_servisable)
#         serializer_pro_base = ProductBaseSerializer(product_base, many=True)
#
#         itemMeasuementUnit_base = ItemMeasuementUnit.objects.filter(is_available=True)
#         serialiser_itemMeasuementUnit_base = ItemMeasuementUnitSerializer(itemMeasuementUnit_base, many=True)
#
#         base_data = {}
#
#         base_data["uom"] = serialiser_itemMeasuementUnit_base.data
#         base_data["category"] = serializer_cat.data
#         base_data["product"] = serializer_pro.data
#         base_data["product_base"] = serializer_pro_base.data
#
#         return Response(base_data)


class BranchProductListAdmin(APIView):

    def post(self,request):
        received_json_data = json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)
        #
        branch_id = received_json_data["branch_id"]
        print(":cameggg");

        print(received_json_data);
        # branch_id = "1"


        category_servisable = BranchServisableCategory.objects.filter(branch__id = branch_id).values_list('product_category__id', flat=True)
        product_base_servisable = BranchServisableProductBase.objects.filter(branch__id = branch_id, product_base__product_category__in=category_servisable).values_list('product_base__id', flat=True)
        # product_servisable = BranchServisableProduct.objects.filter(branch__id = branch_id, product__product_base__product_category__in=category_servisable).values_list('product__id', flat=True)

        print("recc aa")
        print(category_servisable)

        category = ProductCategory.objects.filter(id__in=category_servisable)
        # category_ids = ProductCategory.objects.filter(id__in=category_servisable).values_list('id', flat=True)
        # category = ProductCategory.objects.filter(is_available=True)
        serializer_cat = ProductCategorySerializer(category, many=True)

        print("start1000")
        # product_servisable = BranchServisableProduct.objects.filter(branch__id = branch_id, product__product_base__product_category__in=category_servisable).values_list('product__id', flat=True)
        product_servisable = BranchServisableProduct.objects.filter(branch__id = branch_id, product__product_base__product_category__in=category_servisable).order_by('-product__priority')
        # product = Product.objects.filter(id__in = product_servisable).order_by('-priority')

        # user = UserProfileInfo.objects.get(phone_primary=phone)
        print("start10002")
        serializer_pro = BranchServisableProductSerializerAd(product_servisable, context={"language":"en"}, many=True)
        print(serializer_pro.data)
        print("start1003")
        product_base = ProductBase.objects.filter(id__in = product_base_servisable)
        serializer_pro_base = ProductBaseSerializer(product_base, many=True)

        itemMeasuementUnit_base = ItemMeasuementUnit.objects.filter(is_available=True)
        serialiser_itemMeasuementUnit_base = ItemMeasuementUnitSerializer(itemMeasuementUnit_base, many=True)

        base_data = {}

        base_data["uom"] = serialiser_itemMeasuementUnit_base.data
        base_data["category"] = serializer_cat.data
        base_data["product"] = []
        base_data["product"] = serializer_pro.data
        base_data["product_base"] = serializer_pro_base.data
        # base_data["product_base"] = []
        return Response(base_data)

class BrandProductListAdmin(APIView):

    def post(self,request):
        received_json_data = json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)
        #
        brand_id = received_json_data["brand_id"]
        print(":cameggg");

        print(received_json_data);
        # branch_id = "1"


        category_servisable = BranchServisableCategory.objects.filter(branch__brand__id = brand_id).values_list('product_category__id', flat=True)
        product_base_servisable = BranchServisableProductBase.objects.filter(branch__brand__id = brand_id, product_base__product_category__in=category_servisable).values_list('product_base__id', flat=True)
        product_servisable = BranchServisableProduct.objects.filter(branch__brand__id = brand_id, product__product_base__product_category__in=category_servisable).values_list('product__id', flat=True)

        print("recc aa")
        print(category_servisable)

        category = ProductCategory.objects.filter(id__in=category_servisable)
        # category_ids = ProductCategory.objects.filter(id__in=category_servisable).values_list('id', flat=True)
        # category = ProductCategory.objects.filter(is_available=True)
        serializer_cat = ProductCategorySerializer(category, many=True)

        product = Product.objects.filter(id__in = product_servisable).order_by('-priority')

        # user = UserProfileInfo.objects.get(phone_primary=phone)

        serializer_pro = ProductSerializer(product, context={"language":"en"},   many=True)

        product_base = ProductBase.objects.filter(id__in = product_base_servisable)
        serializer_pro_base = ProductBaseSerializer(product_base, many=True)

        itemMeasuementUnit_base = ItemMeasuementUnit.objects.filter(is_available=True)
        serialiser_itemMeasuementUnit_base = ItemMeasuementUnitSerializer(itemMeasuementUnit_base, many=True)

        base_data = {}

        base_data["uom"] = serialiser_itemMeasuementUnit_base.data
        base_data["category"] = serializer_cat.data
        base_data["product"] = serializer_pro.data
        base_data["product_base"] = serializer_pro_base.data

        return Response(base_data)

class BranchProductListServisableCategorySpecific(APIView):

    def post(self,request):
        received_json_data = json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)
        #
        servisable_category_id = received_json_data["servisable_category_id"]
        branch_id = received_json_data["branch_id"]
        print(":cameggg");

        print(received_json_data);
        # branch_id = "1"


        category_servisable_q = BranchServisableCategory.objects.get(id = servisable_category_id, branch__id = branch_id)
        category_id = category_servisable_q.product_category.id


        # product_base_servisable = BranchServisableProduct.objects.filter(product__product_base__product_category=category_id)
        product_servisable = BranchServisableProduct.objects.filter(product__product_base__product_category=category_id, branch__id = branch_id)
            # .values_list('product_base__id', flat=True)
        # product_servisable = BranchServisableProduct.objects.filter(product__product_base__product_category=category_id).values_list('product__id', flat=True)

        # product = Product.objects.filter(id__in = product_servisable).order_by('-priority')

        # user = UserProfileInfo.objects.get(phone_primary=phone)

        serializer_pro = ServisableProductSerializerBranchUser(product_servisable, many=True)

        # product_base = ProductBase.objects.filter(id__in = product_base_servisable)
        # serializer_pro_base = ProductBaseSerializer(product_base, many=True)

        itemMeasuementUnit_base = ItemMeasuementUnit.objects.filter(is_available=True)
        serialiser_itemMeasuementUnit_base = ItemMeasuementUnitSerializer(itemMeasuementUnit_base, many=True)

        base_data = {}

        print("rpodd data============00000009")
        print(serializer_pro.data)
        base_data["uom"] = serialiser_itemMeasuementUnit_base.data
        # base_data["category"] = serializer_cat.data
        base_data["product"] = serializer_pro.data
        # base_data["product_base"] = serializer_pro_base.data

        return Response(base_data)

class BranchProductListServisableCategorySpecificDisabled(APIView):

    def post(self,request):
        received_json_data = json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)
        #
        servisable_category_id = received_json_data["servisable_category_id"]
        branch_id = received_json_data["branch_id"]
        print(":cameggg");

        print(received_json_data);
        # branch_id = "1"


        category_servisable_q = BranchServisableCategory.objects.get(id = servisable_category_id, branch__id = branch_id)
        category_id = category_servisable_q.product_category.id


        # product_base_servisable = BranchServisableProduct.objects.filter(product__product_base__product_category=category_id)
        product_servisable = BranchServisableProduct.objects.filter(is_available = False, product__product_base__product_category=category_id, branch__id = branch_id)
            # .values_list('product_base__id', flat=True)
        # product_servisable = BranchServisableProduct.objects.filter(product__product_base__product_category=category_id).values_list('product__id', flat=True)

        # product = Product.objects.filter(id__in = product_servisable).order_by('-priority')

        # user = UserProfileInfo.objects.get(phone_primary=phone)

        serializer_pro = ServisableProductSerializerBranchUser(product_servisable, many=True)

        # product_base = ProductBase.objects.filter(id__in = product_base_servisable)
        # serializer_pro_base = ProductBaseSerializer(product_base, many=True)

        itemMeasuementUnit_base = ItemMeasuementUnit.objects.filter(is_available=True)
        serialiser_itemMeasuementUnit_base = ItemMeasuementUnitSerializer(itemMeasuementUnit_base, many=True)

        base_data = {}

        print("rpodd data============00000009")
        print(serializer_pro.data)
        base_data["uom"] = serialiser_itemMeasuementUnit_base.data
        # base_data["category"] = serializer_cat.data
        base_data["product"] = serializer_pro.data
        # base_data["product_base"] = serializer_pro_base.data

        return Response(base_data)


class StoreCategoryListAd(APIView):

    def post(self,request):
        received_json_data = json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)

        print("recc sss")
        print(received_json_data)
        #
        brand_id = received_json_data["brand_id"]
        # branch_id = received_json_data["branch_id"]
        # print(":cameggg");

        # print(received_json_data);
        # branch_id = "1"


        category_servisable = ProductCategory.objects.filter(brand__id = brand_id)

        serializer_cat = ProductCategorySerializerAd(category_servisable, many=True)

        base_data = {}

        base_data["categorylist"] = serializer_cat.data

        print("ressponsee ddd")
        print(base_data)

        return Response(base_data)

class StoreUomList(APIView):

    def post(self,request):
        received_json_data = json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)

        print("recc sss")
        print(received_json_data)
        #
        brand_id = received_json_data["brand_id"]
        # branch_id = received_json_data["branch_id"]
        # print(":cameggg");

        # print(received_json_data);
        # branch_id = "1"


        category_servisable = ItemMeasuementUnit.objects.filter(brand__id = brand_id)

        serializer_uom = StoreUomSerializer(category_servisable, many=True)

        base_data = {}

        base_data["uom_list"] = serializer_uom.data

        print("ressponsee ddd")
        print(base_data)

        return Response(base_data)

class StoreCategoryList(APIView):

    def post(self,request):
        received_json_data = json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)

        print("recc sss")
        print(received_json_data)
        #
        branch_id = received_json_data["brand_branch_id"]
        # branch_id = received_json_data["branch_id"]
        print(":cameggg");

        print(received_json_data);
        # branch_id = "1"


        category_servisable = BranchServisableCategory.objects.filter(branch__id = branch_id)

        serializer_cat = ProductCategorySerializerBranchUser(category_servisable, many=True)

        base_data = {}

        base_data["category_list"] = serializer_cat.data

        print("ressponsee ddd")
        print(base_data)

        return Response(base_data)

class ProductList(APIView):

    def get(self,request):
        print(":cameggg");

        category = ProductCategory.objects.filter(is_available=True)
        serializer_cat = ProductCategorySerializer(category, many=True)

        product = Product.objects.filter(is_available=True).order_by('-priority')



        serializer_pro = ProductSerializer(product, context={"language":"ta"},  many=True)

        product_base = ProductBase.objects.filter(is_available=True)
        serializer_pro_base = ProductBaseSerializer(product_base, many=True)


        itemMeasuementUnit_base = ItemMeasuementUnit.objects.filter(is_available=True)
        serialiser_itemMeasuementUnit_base = ItemMeasuementUnitSerializer(itemMeasuementUnit_base, many=True)

        base_data = {}

        base_data["uom"] = serialiser_itemMeasuementUnit_base.data
        base_data["category"] = serializer_cat.data
        base_data["product"] = serializer_pro.data
        base_data["product_base"] = serializer_pro_base.data

        return Response(base_data)


        #
        # # product = Product.objects.filter(is_available=True)
        #
        # serializer = ProductCategorySerializer(category, many=True)
        # # serializer = ProductSerializer(product, many=True)
        # # return Response(serializer.data)
        # return serializer

        # orders = ProductCategory.objects.filter(is_available=True)
        #
        # serializer = ProductCategorySerializer(orders, many=True)
        # return Response(serializer.data)

    def post(self,request):
        received_json_data = json.loads(request.body)
        api_lang = get_api_language_preference(received_json_data)
        #
        phone = received_json_data["user_phone"]
        print(":cameggg");

        print(received_json_data);

        category = ProductCategory.objects.filter(is_available=True)
        serializer_cat = ProductCategorySerializer(category, many=True)

        product = Product.objects.filter(is_available=True).order_by('-priority')

        user = UserProfileInfo.objects.get(phone_primary=phone)

        serializer_pro = ProductSerializer(product, context={"language":user.user_language},   many=True)

        product_base = ProductBase.objects.filter(is_available=True)
        serializer_pro_base = ProductBaseSerializer(product_base, many=True)


        itemMeasuementUnit_base = ItemMeasuementUnit.objects.filter(is_available=True)
        serialiser_itemMeasuementUnit_base = ItemMeasuementUnitSerializer(itemMeasuementUnit_base, many=True)

        base_data = {}

        base_data["uom"] = serialiser_itemMeasuementUnit_base.data
        base_data["category"] = serializer_cat.data
        base_data["product"] = serializer_pro.data
        base_data["product_base"] = serializer_pro_base.data

        return Response(base_data)


# # {"category_filter":"All"}
#         received_json_data=json.loads(request.body)
#         #
#         category_filter = received_json_data["category_filter"]
#
#         # category_filter = "All"
#
#         if category_filter == "All":
#              product = Product.objects.filter(is_available=True).order_by('-priority')
#              serializer_pro = ProductSerializer(product, many=True)
#
#
#              category = ProductCategory.objects.filter(is_available=True)
#              serializer_cat = ProductCategorySerializer(category, many=True)
#
#
#              product_base = ProductBase.objects.filter(is_available=True)
#              serializer_pro_base = ProductBaseSerializer(product_base, many=True)
#
#
#              itemMeasuementUnit_base = ItemMeasuementUnit.objects.filter(is_available=True)
#              serialiser_itemMeasuementUnit_base = ItemMeasuementUnitSerializer(itemMeasuementUnit_base, many=True)
#
#         else:
#
#             product = Product.objects.filter(is_available=True).order_by('-priority')
#             serializer_pro = ProductSerializer(product, many=True)
#
#             category = ProductCategory.objects.filter(is_available=True, id= category_filter)
#             serializer_cat = ProductCategorySerializer(category, many=True)
#
#             product_base = ProductBase.objects.filter(is_available=True, product_category = category)
#             serializer_pro_base = ProductBaseSerializer(product_base, many=True)
#
#             itemMeasuementUnit_base = ItemMeasuementUnit.objects.filter(is_available=True)
#             serialiser_itemMeasuementUnit_base = ItemMeasuementUnitSerializer(itemMeasuementUnit_base, many=True)
#
#         base_data = {}
#
#         base_data["uom"] = serialiser_itemMeasuementUnit_base.data
#         base_data["category"] = serializer_cat.data
#         base_data["product"] = serializer_pro.data
#         base_data["product_base"] = serializer_pro_base.data
#
#         return Response(base_data)

        #
        # serializer = CMN_CommunicationPhysicalModelSerializer(data=request.data)
        #
        # data={}
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_200_OK)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# def get_products(request):

def customer_heatmap(request):
# data =     [
# {
# position: new google.maps.LatLng(-33.91721, 151.22630),
# type: 'info'
# }]


    user_list = UserProfileInfo.objects.prefetch_related('user').filter(user_m_status = dbconstants.M_STATUS_POSITIVE).order_by('-created_at')


    user_l_positive = []
    for user_p in user_list:
        arr = {}
        arr["lat"] = user_p.location_latitude
        arr["lon"] = user_p.location_longitude
        user_l_positive.append(arr)
            # user_l_positive.append(user_p.location_latitude+", "+user_p.location_longitude)

    print("tesssss")
    print(user_l_positive)

    return render(request, 'GEN/heatmaps.html',  {"user_positive":user_l_positive})


def customer_list(request):


    user_list = UserProfileInfo.objects.prefetch_related('user').filter(user_type = dbconstants.USER_TYPE_CONSUMER).order_by('-created_at')
    # user_list = User.objects.all().select_related('user_profile_info')

    # user_profile_list.

    user_list_final = []



    c_status = {}


# M_STATUS_POSITIVE = 'PTV'
# M_STATUS_NEGATIVE = 'NTV'
# M_STATUS_TEST_IN_PROGRESS = 'TIP'
# M_STATUS_NOT_TESTED = "NTD"
#
# M_STATUS_TYPES = [
#         (M_STATUS_POSITIVE, 'M_STATUS_POSITIVE'),
#         (M_STATUS_NEGATIVE, 'M_STATUS_NEGATIVE'),
#         (M_STATUS_TEST_IN_PROGRESS, 'M_STATUS_TEST_IN_PROGRESS'),
#         (M_STATUS_NOT_TESTED, 'M_STATUS_NOT_TESTED'),
#      ]

    c_status["PTV"] = "TESTED_POSITIVE"
    c_status["NTV"] = "TESTED_NEGATIVE"
    c_status["TIP"] = "TEST_IN_PROGRESS"
    c_status["NTD"] = "NOT_TESTED"





    for user_temp in user_list:
        # print("caddd")
        user_meta_raw = User.objects.get(username=user_temp.user)
        # print(user_meta_raw.username)
        user_meta = {}
        user_meta['username'] = user_meta_raw.username
        user_meta['fullname'] = user_meta_raw.first_name
        user_meta['c_status'] =c_status[user_temp.user_m_status]

        #
        #
        # user_temp['profile_pic_absolute'] =  appendServerPath(user_temp['profile_pic'])
        # user_temp.profile_pic("aa","aa")
        # pic = user_temp.profile_pic
        # print(pic)
        user_parent_set = {}
        # user_parent_set['profile_pic'] = appendServerPath(user_temp.profile_pic)
        user_parent_set['user_meta'] = user_meta
        user_parent_set['user_profile'] = user_temp
        #
        user_list_final.append(user_parent_set)

    serialized_obj = serializers.serialize('json', user_list)

    print("sizeb:"+ str(user_list.count()))

    page = request.GET.get('page', 1)

    paginator = Paginator(user_list_final, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'GEN/customers.html',  {'state_list':dbconstants.STATE_LIST_DICT, 'users': users})



# @login_required
def orders_list(request):



    # order_list = Order.objects.prefetch_related('user_customer').prefetch_related('user_delivery_agent').all().order_by('-updated_at')
    order_list = Order.objects.prefetch_related('user_customer').all().order_by('-updated_at')
    order_list_final = []

    for order_temp in order_list:
        # print("caddd")
        # print("cadddw"+str(order_temp.user_customer))
        user_customer_m =User.objects.get(username = order_temp.user_customer)
        user_customer = UserProfileInfo.objects.get(user = user_customer_m)
        #
        # user_delivery_agent_m =User.objects.get(username = order_temp.user_delivery_agent)
        # user_delivery_agent = UserProfileInfo.objects.get(user=user_delivery_agent_m)

        user_customer.user_location_display = user_customer.location_area +','+user_customer.location_sublocality+","+user_customer.location_city+","+user_customer.location_pincode


        # getting order item

        order_items = OrderItem.objects.filter(order = order_temp)
        # print("sizeaaa:"+ str(order_items.count()))

        item_name =""

        for order_item in order_items:

            if item_name != '':
                item_name += ", "+str(order_item.item_name)+" : " +str(order_item.item_quantity) + " " +str(order_item.measurement_unit)
            else:
                item_name += str(order_item.item_name) +" : " +str(order_item.item_quantity) + " " +str(order_item.measurement_unit) 

        order_temp.order_items = item_name

        # getting status text
        order_temp.status = dbconstants.ORDER_STATUS_DIC[order_temp.status]




        # print(user_meta_raw.username)
        order_foreign = {}
        order_foreign['user_customer'] = user_customer
        # order_foreign['user_delivery_agent'] = user_delivery_agent

        #
        #
        order_parent_set = {}
        order_parent_set['order_meta'] = order_temp
        order_parent_set['order_foreign'] = order_foreign
        #
        order_list_final.append(order_parent_set)
        # print("sizeb:"+ JsonResponse(json.loads(order_list_final)))
        # serialized_obja = serializers.serialize('json', order_parent_set)
        # # # filter(user__username ='azr')
        # # # user_list = User.objects.filter(username ='azr')
        # dataa = {"aSomeModel_json": serialized_obja}
        # ("atitaa")
        # print(dataa)
        #
        #




    # fetching prerequistis data for screen

    state_list  = dbconstants.STATE_LIST_DICT
    measurements_list = ItemMeasuementUnit.objects.all()
    # delivery_agents_list = UserProfileInfo.objects.prefetch_related('user').filter(user_type = dbconstants.USER_TYPE_DELIVERY_AGENT)
    order_status_list = dbconstants.ORDER_STATUS_DIC
    # for meas in measurements_list:
    #     print("came print m"+meas.name)
    #

    page = request.GET.get('page', 1)

    paginator = Paginator(order_list_final, 9)
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)
    # print("test1")
    return render(request, 'GEN/orders_list.html',  { 'orders': orders,  'measurements_list':measurements_list, 'state_list':state_list , 'order_status_list':order_status_list })


# @login_required
def product_list(request):


    product_list = Product.objects.all()

    product_list_final = []

    for product_i in product_list:

        each_obj = {}
        each_obj["id"] = str(product_i.id)+""
        each_obj["name"] = product_i.name+""
        each_obj["is_available"] = product_i.is_available

        each_obj["pic"] = appendServerPath(product_i.pic)
        each_obj["measurement_unit"] = str(product_i.measurement_unit)+""

        product_list_final.append(each_obj)

        # print(product_i.measurement_unit)

    # field_dic = dict_01()

    uom = ItemMeasuementUnit.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(product_list, 9)
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)
    # print("test1")
    return render(request, 'GEN/product_list.html',  { 'products': product_list_final, "uoms": uom })


@login_required
def place_order(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('GEN:index'))

@login_required
def user_logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('GEN:index'))

def appendServerPath(relative_path):
    a = str(relative_path)
    return GEN_Constants.SERVER_PREFIX+"media/"+a

def user_login(request):


    return HttpResponse(json.dumps({"SUCCESS":False, "RESPONSE_MESSAGE":get_display_translated_value(value_constant.KEY_D_INVALID_DATA), "ERRORS": {}}),
    content_type="application/json")

def get_html_privacy_policy(request):
    return render(request, 'GEN/privacy_policy.html', {})

def get_html_index(request):
    return render(request, 'GEN/index.html', {})

def get_html_terms_and_conditions(request):
    return render(request, 'GEN/terms_and_conditions.html', {})
def get_html_safez(request):
    return render(request, 'GEN/safez_index.html', {})
def user_login(request):
    # return HttpResponse("Hi came view")

    if request.method == "POST":

        dataset = request.POST
        api_lang = get_api_language_preference(dataset)

        username = request.POST['username']
        password = request.POST['password']

        print(username+"+==="+password)

        user = authenticate(request, username = username, password = password)

        if user:
            if user.is_active:
                print('active')
                auth_login(request,user)
                return HttpResponse(json.dumps({"SUCCESS":True, "RESPONSE_MESSAGE":get_display_translated_value(value_constant.KEY_D_LOGIN_SUCCESSFUL,api_lang)}),
                content_type="application/json")


                # return HttpResponseRedirect(reverse('base_app:index'))
            else:
                errors_dict = {"DATA":get_display_translated_value(value_constant.KEY_D_NOT_INVALID_DATA,api_lang)}
                return HttpResponse(json.dumps({"SUCCESS":False, "RESPONSE_MESSAGE":"2INVALID DATA", "ERRORS": errors_dict}),
                content_type="application/json")

        else:
            errors_dict = {"DATA":get_display_translated_value(value_constant.KEY_D_NOT_INVALID_DATA,api_lang)}
            return HttpResponse(json.dumps({"SUCCESS":False, "RESPONSE_MESSAGE":get_display_translated_value(value_constant.KEY_D_INVALID_DATA,api_lang), "ERRORS": errors_dict}),
            content_type="application/json")

    else:
        print('jdkada')
        return render(request, 'GEN/index.html', {})

    # return render(request, 'GEN/login2.html', {})
#
#
# class EnterPriseForm(APIView):
#
#     def get(self,request):
#         orders = CMN_CommunicationPhysicalModel.objects.all()
#         serializer = CMN_CommunicationPhysicalModelSerializer(orders, many=True)
#         return Response(serializer.data)
#
#     def post(self,request):
#          # "CMN_CommunicationPhysicalModel__slug":"ssssaaee",
#         # CMN_CommunicationPhysicalModel__
#         # "CMN_CommunicationVirtualModel__slug":"TEST",
#         # "CMN_CommunicationVirtualModel__id":"TEST",
#         # "CMN_CommunicationPhysicalModel__slug": "Y6OVJRZ3",
#         form_data = { "CMN_CommunicationVirtualModel__communication_channel_value": '["Channel v"]', "CMN_CommunicationPhysicalModel__address_line_01": "address_line_01", "CMN_CommunicationPhysicalModel__address_line_02":"address_line_02", "CMN_CommunicationPhysicalModel__city":"city", "CMN_CommunicationPhysicalModel__district":"district", "CMN_CommunicationPhysicalModel__country":"country", "CMN_CommunicationPhysicalModel__pincode":"008877", "CMN_CommunicationPhysicalModel__state":"state"}
#         # "CMN_CommunicationPhysicalModel__state":"state",
#         # "CMN_CommunicationPhysicalModel__country":"country",
#         # serializer = CMN_CommunicationPhysicalModelSerializer(data=request.data)
#         clean_serializer_data = getSerializerCleanData(form_data)
#
#
#         CMN_CommunicationPhysicalModel_data = clean_serializer_data["CMN_CommunicationPhysicalModel"]
#         CMN_CommunicationVirtualModel_data = clean_serializer_data["CMN_CommunicationVirtualModel"]
#         #
#         # print("came tesss")
#         # print(CMN_CommunicationPhysicalModel_data)
#         data={}
#
#         if 'slug' in CMN_CommunicationPhysicalModel_data:
#             order_obj = CMN_CommunicationPhysicalModel.objects.get(slug=CMN_CommunicationPhysicalModel_data["slug"])
#             serializer_communication_physical = CMN_CommunicationPhysicalModelSerializer(instance = order_obj, data=CMN_CommunicationPhysicalModel_data, partial=True)
#         else:
#             slug = unique_slug_generator(CMN_CommunicationPhysicalModel)
#             CMN_CommunicationPhysicalModel_data.add("slug",slug)
#             serializer_communication_physical = CMN_CommunicationPhysicalModelSerializer(data=CMN_CommunicationPhysicalModel_data, partial=True)
#
#         if 'slug' in CMN_CommunicationVirtualModel_data:
#             order_obj = CMN_CommunicationVirtualModel.objects.get(slug=CMN_CommunicationVirtualModel_data["slug"])
#             serializer_communication_virtual = CMN_CommunicationVirtualModelSerializer(instance = order_obj, data=CMN_CommunicationVirtualModel_data, partial=True)
#         else:
#             slug = unique_slug_generator(CMN_CommunicationVirtualModel)
#             CMN_CommunicationVirtualModel_data.add("slug",slug)
#             serializer_communication_virtual = CMN_CommunicationVirtualModelSerializer(data=CMN_CommunicationVirtualModel_data, partial=True)
#
#         # return Response(CMN_CommunicationPhysicalModel_data, status=status.HTTP_400_BAD_REQUEST)
#         # serializer = CMN_CommunicationPhysicalModelSerializer(data=request.data)
#
#         # CMN_CommunicationPhysicalModel_data.add("id",8)
#
#         if serializer_communication_physical.is_valid():
#             # serializer_communication_physical.save()
#             if serializer_communication_virtual.is_valid():
#                 cm_p = serializer_communication_physical.save()
#                 cm_v = serializer_communication_virtual.save()
#
#                 print("vm success")
#
#             else:
#                 return Response(serializer_communication_virtual.errors, status=status.HTTP_400_BAD_REQUEST)
#             return Response(serializer_communication_physical.data, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer_communication_physical.errors, status=status.HTTP_400_BAD_REQUEST)
#             # return Response(serializer_communication_physical.data, status=status.HTTP_200_OK)
#
#
#             # return Response(serializer_communication_virtual.data, status=status.HTTP_200_OK)
#
#         return Response(serializer_communication_physical.errors, status=status.HTTP_400_BAD_REQUEST)
#
#


def MergeDict(dict1, dict2):
    (dict2.update(dict1))
    return dict2


# @csrf_exempt
def add_enterprise_s(request):

    usera = authenticate(request, username = "azr", password = "q1w2e3r41")
    # form_data  = dict_01()
    # # form_data = {"CMN_CommunicationVirtualModel__slug":"TEST","CMN_CommunicationVirtualModel__id":"TEST",  "CMN_CommunicationPhysicalModel__pincode":"601201", "CMN_CommunicationPhysicalModel__slug":"601201"}
    # if request.method == "POST":
    #     for key, value in request.POST.items():
    #         print(key,value)
    #         form_data.add(key,value)
    #     print("aaat")
    #     print(form_data)
    # else:
    #     print("GET")
    #
    # # print request.POST
    #
    # print(form_data)


    # od = collections.OrderedDict(sorted(form_data.items()))
    # clean_serializer_data = getSerializerCleanData(form_data)
    # slug - unique_slug_generator
    # CMN_CommunicationPhysicalModel__
    # data_m = {"CMN_CommunicationPhysicalModel__slug":"ssssaaee", "CMN_CommunicationPhysicalModel__address_line_01": "address_line_01", "CMN_CommunicationPhysicalModel__address_line_02":"address_line_02", "CMN_CommunicationPhysicalModel__city":"city", "CMN_CommunicationPhysicalModel__district":"district","CMN_CommunicationPhysicalModel__state":"state","CMN_CommunicationPhysicalModel__country":"country", "CMN_CommunicationPhysicalModel__pincode":"pincod"}
    data_m = {"slug":"ssssaaee", "address_line_01": "address_line_01", "address_line_02":"address_line_02", "city":"city", "district":"district","state":"state","country":"country", "pincode":"pincod"}
# , 'city':'city', 'country':'country', 'address_line_02': 'DSDW', 'address_line_01': 'WEWRSD','state': 'SDSD', 'district': 'FSDFDSF', 'pincode': '000000'}
    serializer = CMN_CommunicationPhysicalModelSerializer(data=data_m)

    # CMN_CommunicationPhysicalModel

    if serializer.is_valid():
        # serializer.save(user=usera, date=timezone.now(), status='sent')
        serializer.save(user=usera)

    # field_arr = ["HAHAH"]
    return JsonResponse({'sucees':serializer.errors}, safe=False)

# def posta(request):
#         serializer = CMN_CommunicationPhysicalModelSerializer(data=request.data)
#         data={}
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def user_logind(request):

    user = authenticate(request, username = "azr", password = "q1w2e3r41")

    # # return HttpResponse("Hi came view")
    #
    # if request.method == "POST":
    #
    #     username = request.POST['username']
    #     password = request.POST['password']
    #
    #     print(username+"+==="+password)
    #
    #     user = authenticate(request, username = username, password = password)
    #
    #     if user:
    #         if user.is_active:
    #             print('active')
    #             auth_login(request,user)
    #             return HttpResponse(json.dumps({"SUCCESS":True, "RESPONSE_MESSAGE":"Login successful"}),
    #             content_type="application/json")
    #
    #
    #             # return HttpResponseRedirect(reverse('GEN:index'))
    #         else:
    #             errors_dict = {"DATA":"Not a valid data"}
    #             return HttpResponse(json.dumps({"SUCCESS":False, "RESPONSE_MESSAGE":"2INVALID DATA", "ERRORS": errors_dict}),
    #             content_type="application/json")
    #
    #     else:
    #         errors_dict = {"DATA":"Not a valid data"}
    #         return HttpResponse(json.dumps({"SUCCESS":False, "RESPONSE_MESSAGE":"INVALID DATA", "ERRORS": errors_dict}),
    #         content_type="application/json")
    #
    # else:
    #     print('jdkada')
    #     return render(request, 'GEN/login2.html', {})
    #     orders = Order.objects.all()
    #     serializer = OrderSerializer(orders, many=True)
    #     return JsonResponse(serializer.data, safe=False)
    #
    # elif request.method == 'POST':
    #     data = JSONParser.parse(request)


def index(request):

    # enterpriseform_s
    # print("came changestat")

    # if request.method == 'GET':
    #     serializer =OrderSerializer(data=data)
    #
    #     if(serializer.is_valid()):
    #         serializer.save()
    #         return JsonResponse(serializer.data, status=201)[
    #     return JsonResponse(serializer.errors, status=400)

    # username = request.POST['username']
    # user_status = request.POST['user_status']
    #
    # user_obj = User.objects.get(username=username)
    # user_profile = UserProfileInfo.objects.get(user=user_obj)
    #
    # # user_profile = UserProfileInfo.objects.get(username=username)
    #
    # if user_status == "AT":
    #     print("useractive")
    #     user_status = dbconstants.USER_STATUS_DISABLED
    # else:
    #     user_status = dbconstants.USER_STATUS_ACTIVE
    #     print("userinactive")
    # user_profile.user_status = user_status
    # user_profile.save()
    # return render(request, 'GEN/base.html',  {})
    # return HttpResponse(json.dumps({"SUCCESS":True, "RESPONSE_MESSAGE":"Status updated"}),
    # content_type="application/json")
    # form_f = [{"fn": "company_name", "dt": "Text_100", "rq": true, "ph": "Enterprise Name"},{"fn": "company_mail", "dt": "Email", "rq": true, "ph": "Enterprise Email"}]
     # return HttpResponse(json.dumps({"SUCCESS":True, "RESPONSE_MESSAGE":"Status updated"})


     # CMN_CommunicationVirtualModelSerializer

     # [{"fn": "company_name", "dt": "Text_100", "rq": true, "ph": "Enterprise Name"},{"fn": "company_mail", "dt": "Email", "rq": true, "ph": "Enterprise Email"}]

    # return render(request, 'GEN/base.html',  {})
    # orders = CMN_CommunicationVirtualModel.objects.all()
    # serializer = CMN_CommunicationVirtualModelSerializer(orders, many=True)
    # return JsonResponse(serializer.data, safe=False)

    field_arr = []

    form_fields = ["CMN_CommunicationVirtualModel__slug", "CMN_CommunicationVirtualModel__communication_type", "CMN_CommunicationVirtualModel__communication_channel_key", "CMN_CommunicationVirtualModel__communication_channel_value", "CMN_CommunicationPhysicalModel__communication_type", "CMN_CommunicationPhysicalModel__address_line_01", "CMN_CommunicationPhysicalModel__address_line_02", "CMN_CommunicationPhysicalModel__city", "CMN_CommunicationPhysicalModel__district", "CMN_CommunicationPhysicalModel__state", "CMN_CommunicationPhysicalModel__pincode"]
    serializer = EnterPriseForm()

    field_arr =getSerilalierField(serializer,field_arr, "Parent", form_fields)
    return JsonResponse(field_arr, safe=False)

def add_enterprise(request):

    field_arr = []

    form_fields = ["CMN_CommunicationVirtualModel__slug", "CMN_CommunicationVirtualModel__communication_type", "CMN_CommunicationVirtualModel__communication_channel_key", "CMN_CommunicationVirtualModel__communication_channel_value", "CMN_CommunicationPhysicalModel__communication_type", "CMN_CommunicationPhysicalModel__address_line_01", "CMN_CommunicationPhysicalModel__address_line_02", "CMN_CommunicationPhysicalModel__city", "CMN_CommunicationPhysicalModel__district", "CMN_CommunicationPhysicalModel__state", "CMN_CommunicationPhysicalModel__pincode"]

    serializer = EnterPriseForm()

    field_arr =getSerilalierField(serializer,field_arr, "Parent", form_fields)
    return JsonResponse(field_arr, safe=False)



class dict_01(dict):

    # __init__ function
    def __init__(self):
        self = dict()

    # Function to add key:value
    def add(self, key, value):
        self[key] = value

def getSerializerCleanData(form_data):

    model_dic = dict_01()

    model_name = "NONE"
    field_dic = dict_01()
    field_set = []

    for key in form_data:

        print(key)
        split = key.split("__");
        model_name_c = split[0]

        if model_name != model_name_c:
            if model_name != "NONE":
                model_dic.add(model_name, field_dic)
            model_name = model_name_c
            field_dic = dict_01()


        field_name = split[1]
        field_dic.add(field_name, form_data[key])

    model_dic.add(model_name, field_dic)
    print(model_dic)
        # if(last)
        # model_dic.add(model_name, field_dic)

    return model_dic;

def getSerilalierField(serializer_obj,field_arr, model ,form_fields ):
    for field_name, field_obj in serializer_obj.get_fields().items():

        if 'Serializer' in field_obj.__class__.__name__ and field_obj.__class__.__name__ != 'SerializerMethodField':
            field_arr=getSerilalierField(field_obj, field_arr, field_obj.__class__.__name__, form_fields)
        else:
            name_final = model.replace("ModelSerializer", "Model")+"__"+field_name
            # name_final = name_final.replace("SerializerModel__", "Model__")
            if name_final in form_fields:
                each_obj ={}
                # each_obj['model'] = model
                each_obj['cn'] = name_final
                each_obj['dt'] = field_obj.help_text
                each_obj['dt_r'] = field_obj.__class__.__name__
                each_obj['required'] = field_obj.required
                if hasattr(field_obj, 'verbose_name'):
                    each_obj['lb'] = field_obj.verbose_name
                else:
                    v_name = field_name.replace("_"," ")
                    each_obj['lb'] = v_name

                if hasattr(field_obj, 'choices'):
                   each_obj['choices'] = field_obj.choices
                   # each_obj['dt'] = 'MOD_DT_CHOICES'
                # if hasattr(field_obj, 'label'):
                #    each_obj['lb'] = field_obj.label
                field_arr.append(each_obj)
    return field_arr;



def unique_slug_generator(Klass, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = random_string_generator(size=8)

    # Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug= slug).exists()
    if qs_exists:
        new_slug = random_string_generator(size=8)
        return unique_slug_generator(Klass, new_slug= new_slug)
    return slug;

def unique_slug_generator_i(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = random_string_generator(size=8)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug= slug).exists()
    if qs_exists:
        new_slug = random_string_generator(size=8)
        return unique_slug_generator(instance, new_slug= new_slug)
    return slug;


def random_string_generator(size=8, chars=string.ascii_uppercase +string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
