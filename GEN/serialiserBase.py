from rest_framework import serializers
from GEN import dbconstants, GEN_Constants,value_constant
from .value_constant import get_display_translated_value
from .models import UserProfileInfo, CMN_CommunicationVirtualModel, CMN_CommunicationPhysicalModel, ProductCategory,\
    Product, ProductBase, ItemMeasuementUnit, OrderItem, C19SymptomSet, UserHealthProfile, Order, BrandBranchBasicInfo,\
    BranchServisableCategory, BranchServisableProductBase, BranchServisableProduct, ServisableDaysCriteria


# def get_language_preferrence(self, obj):
#     try:
#         if "language" in get_display_translated_value:
#             if self.context["language"] == value_constant.KEY_LANGUAGE_TA:
#                 return value_constant.KEY_LANGUAGE_TA
#             else:
#                 return value_constant.KEY_LANGUAGE_EN
#         return value_constant.KEY_LANGUAGE_EN
#     except:
#         return value_constant.KEY_LANGUAGE_EN
# 


class ProductSuggestionListSerializer(serializers.ModelSerializer):
    # first_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('name', 'name_tamil', 'slug')
        # exclude = ['user']
    # def get_first_name(self, obj):
    #     return obj.user.first_name


class UserProfileSuggestionSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()

    class Meta:
        model = UserProfileInfo
        fields = ('first_name', 'phone_primary')
        # exclude = ['user']
    def get_first_name(self, obj):
        return obj.user.first_name

class UserProfileInfoSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()

    class Meta:
        model = UserProfileInfo
        fields = ('first_name', 'phone_primary', 'location_area', 'location_sublocality', 'location_locality', 'location_city', 'location_pincode')
        # exclude = ['user']
    def get_first_name(self, obj):
        return obj.user.first_name


class UserHealthProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserHealthProfile
        fields = ('user', 'symptom')
        exclude = ['user']



class C19SymptomSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = C19SymptomSet
        fields = ['id', 'name', 'name_tamil', 'seviarity']
        depth = 0


class OrderItemSerializer(serializers.ModelSerializer):

    measurement_unit = serializers.SerializerMethodField()
    item_name = serializers.SerializerMethodField()
    item_img = serializers.SerializerMethodField()

    def get_measurement_unit(self, obj):

        # measurement_un = ItemMeasuementUnit.objects.get(pk=obj.measurement_unit)
        return str(obj.measurement_unit)
        # order_items_s = OrderItemSerializer(order_items, many=True).data
        # return order_items_s
        #
        # return "Kg"

    def get_item_img(self, obj):
        if(obj.product):
            return "/media/"+str(obj.product.pic)
        else:
            return ""

    def get_item_name(self, obj):
        return str(obj.item_name)

    class Meta:
        model = OrderItem
        fields = ['item_name', 'item_quantity', 'measurement_unit', 'item_img']



class OrderSerializer(serializers.ModelSerializer):
    order_item = serializers.SerializerMethodField()
    delivery_status = serializers.SerializerMethodField()
    status_text = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'order_id', 'delivery_charges', 'status_text', 'delivery_status', 'order_item']
        depth = 0


    def get_delivery_status(self, obj):
            return "None"

class CustomerAllOrderSerializer(serializers.ModelSerializer):
    order_item = serializers.SerializerMethodField()
    order_status = serializers.SerializerMethodField()
    status_title = serializers.SerializerMethodField()
    status_text = serializers.SerializerMethodField()

    branch_lat = serializers.SerializerMethodField()
    branch_long = serializers.SerializerMethodField()
    branch_name = serializers.SerializerMethodField()
    branch_address = serializers.SerializerMethodField()
    g_map_query = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    phone_secondary = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'g_map_query', 'phone', 'phone_secondary', 'order_id', 'delivery_charges', 'schedule_requested_time', 'checked_in_time', 'order_status', 'order_item', 'status_title', 'status_text', 'branch_address', 'branch_name', 'branch_lat', 'branch_long']


    def get_branch_name(self, obj):
        return obj.branch.name

    def get_branch_address(self, obj):
        return obj.branch.address_text

    def get_branch_lat(self, obj):
        return obj.branch.location_latitude

    def get_branch_long(self, obj):
        return obj.branch.location_langitude

    def get_g_map_query(self, obj):
        return "geo:0,0?q="+obj.branch.g_address_dump
        # return "geo:0,0?q=Naturals Salon and Spa, Landons Road, Kilpauk, Chennai, Tamil Nadu, India"

    def get_phone(self, obj):
        return obj.branch.phone_primary

    def get_phone_secondary(self, obj):
        return obj.branch.phone_secondary

    def get_status_title(self, obj):
        return obj.get_status_title()

    def get_status_text(self, obj):
        return obj.get_status_text()

    def get_order_status(self, obj):
        if obj.order_status is not None:
            return obj.order_status.code
        else:
            return None

    def get_order_item(self, obj):

        order_items = OrderItem.objects.filter(order=obj).order_by('-created_at')

        order_items_s = OrderItemSerializer(order_items, many=True).data
        return order_items_s


class OrderDetail01SerializerWithActions(serializers.ModelSerializer):
    order_item = serializers.SerializerMethodField()
    delivery_status = serializers.SerializerMethodField()
    status_text = serializers.SerializerMethodField()
    status_code = serializers.SerializerMethodField()
    requested_time = serializers.SerializerMethodField()
    can_accept = serializers.SerializerMethodField()
    can_checkin = serializers.SerializerMethodField()
    can_complete_service = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()
    slot_details = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user_details', 'slot_details', 'can_accept', 'can_checkin', 'can_complete_service', 'requested_time', 'order_id', 'status_code', 'delivery_charges', 'status_text', 'delivery_status', 'order_item']
        depth = 0


    def get_slot_details(self, obj):
        # received_data_str = str(obj.schedule_requested_time)

        received_data_str = obj.schedule_requested_time.strftime("%Y-%m-%d %H:%M:%S")
        print("received_data_str")

        print(received_data_str)
        # received_data_str
        return obj.branch.get_slot_details(received_data_str)
            # {"slot_display_text":"5 open slots available at selected time block (2 PM to 3PM)", "slot_status_type":1, "slot_total":100, 'slot_filled':95, 'slot_open':5, "slot_block":"2 PM to 3PM"}

    def get_user_details(self, obj):
        return {"name":obj.user_customer.user.first_name, 'age':obj.user_customer.age, "gender":obj.user_customer.gender}
        # return {"name":"Test Name", 'age':25, "gender":"Male"}

    def get_can_accept(self, obj):
        return {"STATUS":True, "MESSAGE":"Can Accept Request", "SHOW_MESSAGE":False}

    def get_can_complete_service(self, obj):
        return {"STATUS":True, "MESSAGE":"Can Complete Request", "SHOW_MESSAGE":False}

    def get_can_complete_service(self, obj):

        return {"STATUS":True, "MESSAGE":"Can Accept Request", "SHOW_MESSAGE":False}

    def get_can_checkin(self, obj):
        return {"STATUS":True, "MESSAGE":"Can Checkin", "SHOW_MESSAGE":False}
        # return {"STATUS":False, "MESSAGE":"Checkin Timeout", "SHOW_MESSAGE":True}

    def get_requested_time(self, obj):
        return str(obj.schedule_requested_time)

    def get_status_code(self, obj):
        if obj.order_status is not None:
            return obj.order_status.code
        else:
            return "NO_STATUS"

    def get_delivery_status(self, obj):
        return "None"



    def get_status_text(self, obj):
        if obj.branch is not None:
            return obj.branch.name
        else:
            return ""

    def get_order_item(self, obj):

        order_items = OrderItem.objects.filter(order=obj).order_by('-created_at')

        order_items_s = OrderItemSerializer(order_items, many=True).data
        return order_items_s

class OrderAgentResponseSerializer(serializers.ModelSerializer):
    order_item = serializers.SerializerMethodField()
    delivery_status = serializers.SerializerMethodField()
    status_text = serializers.SerializerMethodField()
    status_code = serializers.SerializerMethodField()
    requested_time = serializers.SerializerMethodField()
    agent_response_details = serializers.SerializerMethodField()
    branch_details = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'branch_details', 'agent_response_details',  'requested_time', 'order_id', 'status_code', 'delivery_charges', 'status_text', 'delivery_status', 'order_item']
        depth = 0

    def get_agent_response_details(self, obj):

        response = {"status": False, "status_title":"Booking Not Confirmed", "status_text":"Booking has not been confirmed on requested time. Please try scheduling on some other time" }
        if obj.order_status is not None:
            if obj.order_status.code == GEN_Constants.ORDER_STATUS_AGENT_APPROVED:
                response = {"status": True, "status_title":get_display_translated_value(value_constant.KEY_D_BOOKING_CONFIRMED),
                            "status_text":get_display_translated_value(value_constant.KEY_D_BOOKING_SCHEDULED_REQUEST_TIME)}
        return  response


    def get_branch_details(self, obj):
        return obj.branch.get_branch_display_details()

    def get_requested_time(self, obj):
        return str(obj.schedule_requested_time)

    def get_status_code(self, obj):
        if obj.order_status is not None:
            return obj.order_status.code
        else:
            return "NO_STATUS"

    def get_delivery_status(self, obj):
        return "None"



    def get_status_text(self, obj):
        if obj.branch is not None:
            return obj.branch.name
        else:
            return ""

    def get_order_item(self, obj):

        order_items = OrderItem.objects.filter(order=obj).order_by('-created_at')

        order_items_s = OrderItemSerializer(order_items, many=True).data
        return order_items_s

class OrderDetail01Serializer(serializers.ModelSerializer):
    order_item = serializers.SerializerMethodField()
    delivery_status = serializers.SerializerMethodField()
    status_text = serializers.SerializerMethodField()
    status_code = serializers.SerializerMethodField()
    requested_time = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'requested_time', 'order_id', 'status_code', 'delivery_charges', 'status_text', 'delivery_status', 'order_item']
        depth = 0


    def get_requested_time(self, obj):
        return str(obj.schedule_requested_time)

    def get_status_code(self, obj):
        if obj.order_status is not None:
            return obj.order_status.code
        else:
            return "NO_STATUS"

    def get_delivery_status(self, obj):
        return "None"



    def get_status_text(self, obj):
        if obj.branch is not None:
            return obj.branch.name
        else:
            return ""

    def get_order_item(self, obj):

        order_items = OrderItem.objects.filter(order=obj).order_by('-created_at')

        order_items_s = OrderItemSerializer(order_items, many=True).data
        return order_items_s

class ServisableDaysCriteriaSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServisableDaysCriteria
        fields = ['id', 'brand', 'branch', 'service_start_time', 'service_end_time', 'day_of_week', 'is_available', 'is_online']


class BranchDetailAdminSerializer(serializers.ModelSerializer):

    servisable_days_criteria = serializers.SerializerMethodField()

    class Meta:
        model = BrandBranchBasicInfo
        fields = ['id', 'brand', 'name', 'phone_primary', 'phone_secondary', 'g_address_dump', 'place_google_id', 'description', 'address_text', 'branch_base_image', 'store_capacity', 'location_latitude', 'location_langitude', 'status', 'is_available', 'is_online', 'servisable_days_criteria']

    def get_brand(self, obj):
        return obj.brand.id

    def get_servisable_days_criteria(self, obj):
        ServisableDaysCriteria_q = ServisableDaysCriteria.objects.filter(branch__id = obj.id)
        ServisableDaysCriteria_data = ServisableDaysCriteriaSerializer(ServisableDaysCriteria_q, many=True).data
        return ServisableDaysCriteria_data


class BrandOrderListSerializer(serializers.ModelSerializer):

    order_item = serializers.SerializerMethodField()

    order_status = serializers.SerializerMethodField()
    status_title = serializers.SerializerMethodField()
    status_text = serializers.SerializerMethodField()
    customer = serializers.SerializerMethodField()
    branch_name = serializers.SerializerMethodField()
    branch_address = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'order_id', 'schedule_requested_time', 'order_status', 'status_title', 'status_text', 'customer', 'order_item', 'branch_name', 'branch_address']
        depth = 0


    def get_branch_name(self, obj):
        return obj.branch.name

    def get_branch_address(self, obj):
        return obj.branch.address_text


    def get_customer(self, obj):
        return {"name":(obj.user_customer.getUserDisplayName()), "phone":obj.user_customer.phone_primary}

    def get_order_status(self, obj):
        print("order idd")
        print(obj.order_id)
        return str(obj.order_status.code)

    def get_status_title(self, obj):
        return obj.get_status_title()

    def get_status_text(self, obj):
        return obj.get_status_text()

    def get_order_item(self, obj):

        order_items = OrderItem.objects.filter(order=obj).order_by('-created_at')

        order_items_s = OrderItemSerializer(order_items, many=True).data
        return order_items_s

class BranchOrderListSerializer(serializers.ModelSerializer):
    order_item = serializers.SerializerMethodField()
    delivery_status = serializers.SerializerMethodField()
    status_text = serializers.SerializerMethodField()
    status_code = serializers.SerializerMethodField()
    scheduled_at = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'order_id', 'delivery_charges', 'status_code', 'status_text', 'user_name', 'delivery_status', 'order_item', 'scheduled_at']
        depth = 0


    def get_user_name(self, obj):
        return str(obj.user_customer.getUserDisplayName())

    def get_status_code(self, obj):
        print("order idd")
        print(obj.order_id)
        return str(obj.order_status.code)

    def get_scheduled_at(self, obj):
        return str(obj.schedule_requested_time)

    def get_delivery_status(self, obj):
        #
        # if obj.status == dbconstants.ORDER_PLACED:
        #     return "Order has been placed successfully. Customer Executive will call in some time"
        # elif obj.status == dbconstants.ORDER_CONFIRMED_BY_CUSTOMER:
        #     return "Order will be delivered by the 11 Am tomorrow"
        # elif obj.status == dbconstants.ORDER_PICKEDUP:
        #     return "Order pickedup and the delivery executive is on his way"
        # elif obj.status == dbconstants.ORDER_CANCELLED:
        return str(obj.schedule_requested_time)



    def get_status_text(self, obj):
        if obj.branch is not None:
            return obj.branch.name
        else:
            return ""
        # return obj.order_status.name
        # return dbconstants.ORDER_STATUS_DISPLAY[obj.status]

    def get_order_item(self, obj):

        order_items = OrderItem.objects.filter(order=obj).order_by('-created_at')

        order_items_s = OrderItemSerializer(order_items, many=True).data
        return order_items_s

class ItemMeasuementUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemMeasuementUnit
        fields = ['id', 'name', 'note']
        depth = 0


class BrandBranchBasicInfoSerializerAD(serializers.ModelSerializer):

    phone = serializers.SerializerMethodField()

    class Meta:
        model = BrandBranchBasicInfo
        fields = ['id', 'name', 'description', 'address_text', 'branch_base_image', 'status', 'is_available', 'is_online', 'location_latitude', 'location_langitude' , 'phone', 'place_google_id', 'landmark_place_google_id', 'store_capacity']
        depth = 0

    def get_phone(self, obj):
        return "9999999999"


class BrandBranchBasicInfoSerializer(serializers.ModelSerializer):
    phone = serializers.SerializerMethodField()
    phone_secondary = serializers.SerializerMethodField()
    g_map_query = serializers.SerializerMethodField()

    class Meta:
        model = BrandBranchBasicInfo
        fields = ['id', 'name', 'place_google_id', "g_map_query", 'description', 'address_text', 'branch_base_image', 'status', 'is_available', 'is_online', 'location_latitude', 'location_langitude' , 'phone', 'phone_secondary']
        depth = 0

    def get_g_map_query(self, obj):
        return "geo:0,0?q="+obj.g_address_dump
        # return "geo:0,0?q=Naturals Salon and Spa, Landons Road, Kilpauk, Chennai, Tamil Nadu, India"

    def get_phone(self, obj):
        return obj.phone_primary

    def get_phone_secondary(self, obj):
        return obj.phone_secondary

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'pic', 'name', 'name_tamil', 'sub_text', 'description', 'status_note']
        depth = 0

class ProductCategorySerializerAd(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()

    class Meta:
        model = ProductCategory
        fields = ['id', 'pic', 'name', 'sub_text', 'description',  'is_available']

    def get_name(self, obj):
        return obj.name

class StoreUomSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()

    class Meta:
        model = ItemMeasuementUnit
        fields = ['id', 'name', 'brand', 'note',  'is_available']

    def get_name(self, obj):
        return obj.name

class ProductCategorySerializerBranchUser(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()
    category_id = serializers.SerializerMethodField()
    pic = serializers.SerializerMethodField()
    sub_text = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = BranchServisableCategory
        fields = ['id', 'category_id', 'pic', 'name', 'sub_text', 'description',  'is_available']

    def get_name(self, obj):
        return obj.product_category.name

    def get_category_id(self, obj):
        return obj.product_category.id

    def get_pic(self, obj):
        # if obj.product_category is not None:
        if obj.product_category.pic and hasattr(obj.product_category.pic, 'url'):
            return obj.product_category.pic.url
        else:
            return None

    def get_sub_text(self, obj):
        return obj.product_category.sub_text

    def get_description(self, obj):
        return obj.product_category.description


class ProductBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBase
        fields = ['id','name', 'name_tamil','sub_text', 'description', 'status_note', 'product_category']
        depth = 0



class BranchServisableProductSerializerAd(serializers.ModelSerializer):

    product_id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    pic = serializers.SerializerMethodField()
    sub_text = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    base_measurement_unit = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    show_price = serializers.SerializerMethodField()
    status_note = serializers.SerializerMethodField()
    product_base = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()



    class Meta:
        model = BranchServisableProduct
        fields = ['id', 'product_id', 'category', 'name', 'pic', 'sub_text', 'description', 'base_measurement_unit', 'price', 'show_price', 'status_note', 'product_base', 'measurement_unit', 'is_available', 'is_online']


    def get_measurement_unit(self, obj):
        m_units = []
        for e_m_unit in obj.product.measurement_unit.all():
            m_units.append(e_m_unit.id)
        return m_units

        # return obj.product.measurement_unit
        # return[]

    def get_product_base(self, obj):
        return obj.product.product_base.id

    def get_status_note(self, obj):
        return obj.product.status_note

    def get_show_price(self, obj):
        return obj.product.show_price

    def get_base_measurement_unit(self, obj):
        return obj.product.base_measurement_unit.id

    def get_description(self, obj):
        return obj.product.description

    def get_sub_text(self, obj):
        return obj.product.sub_text

    def get_pic(self, obj):
        # if obj.product.pic is not None:
        if obj.product.pic and hasattr(obj.product.pic, 'url'):
            return str(obj.product.pic.url)
        else:
            return None

    def get_product_id(self, obj):
        return obj.product.id

    def get_category(self, obj):
        return obj.product.product_base.product_category.id

    def get_name(self, obj):
        return str(obj.product.name)


class ProductADFeedSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()
    product_id = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', "product_id", 'pic', 'category', 'category_name', 'name', 'name_tamil', 'sub_text', 'description', 'base_measurement_unit', 'price', 'show_price', 'status_note', 'slug', 'priority', 'product_base', 'measurement_unit', 'is_available']
        # fields = '__all__'
        depth = 0

    def get_product_id(self, obj):
        return obj.id

    def get_category(self, obj):
        return obj.product_base.product_category.id

    def get_category_name(self, obj):
        return obj.product_base.product_category.name

    def get_name(self, obj):
        # if self.context["language"] == "ta":
        #     return str(obj.name_tamil)
        # else:
        return str(obj.name)
    def get_pic(self,obj):
        if obj.product.pic and hasattr(obj.product.pic,'url'):
            return obj.product.pic.url
        else:
            return None

class ProductSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'pic', 'category', 'name', 'name_tamil', 'sub_text', 'description', 'base_measurement_unit', 'price', 'show_price', 'status_note', 'slug', 'priority', 'product_base', 'measurement_unit', 'is_available']
        # fields = '__all__'
        depth = 0

    def get_category(self, obj):
        return obj.product_base.product_category.id

    def get_name(self, obj):
        # if self.context["language"] == "ta":
        #     return str(obj.name_tamil)
        # else:
        return str(obj.name)
    def get_pic(self,obj):
        if obj.product.pic and hasattr(obj.product.pic,'url'):
            return obj.product.pic.url
        else:
            return None




class ServisableProductSerializerCustomer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()
    show_price = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    base_measurement_unit = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    sub_text = serializers.SerializerMethodField()
    pic = serializers.SerializerMethodField()
    priority = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()
    product_base = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField()
    is_available = serializers.SerializerMethodField()
    status_note = serializers.SerializerMethodField()
    product_id = serializers.SerializerMethodField()


    class Meta:
        model = BranchServisableProduct
        fields = ['id', 'product_id', "slug", "is_available", 'pic', 'name', 'sub_text', 'description', 'base_measurement_unit', 'price', 'show_price', 'status_note', 'slug', 'priority', 'product_base', 'measurement_unit']

    def get_product_id(self, obj):
        return obj.product.id

    def get_is_available(self, obj):
        return obj.is_available

    def get_name(self, obj):
        return str(obj.product.name)

    def get_slug(self, obj):
        return str(obj.product.slug)

    def get_status_note(self, obj):
        return str(obj.product.status_note)

    def get_measurement_unit(self, obj):
        m_units = []
        for e_m_unit in obj.product.measurement_unit.all():
            m_units.append(e_m_unit.id)
        return m_units

    def get_priority(self, obj):
        return str(obj.product.priority)

    def get_pic(self, obj):
        # if obj.product.pic is not None:
        if obj.product.pic and hasattr(obj.product.pic, 'url'):
            return str(obj.product.pic.url)
        else:
            return None

    def get_sub_text(self, obj):
        return str(obj.product.sub_text)

    def get_description(self, obj):
        return str(obj.product.description)

    def get_base_measurement_unit(self, obj):
        return str(obj.product.base_measurement_unit.id)

    def get_price(self, obj):
        return str(obj.product.price)

    def get_show_price(self, obj):
        return str(obj.product.show_price)

    def get_product_base(self, obj):
        return str(obj.product.id)

class ServisableProductSerializerCustomer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()
    show_price = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    base_measurement_unit = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    sub_text = serializers.SerializerMethodField()
    pic = serializers.SerializerMethodField()
    priority = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()
    product_base = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField()
    is_available = serializers.SerializerMethodField()
    status_note = serializers.SerializerMethodField()
    product_id = serializers.SerializerMethodField()


    class Meta:
        model = BranchServisableProduct
        fields = ['id', 'product_id', "slug", "is_available", 'pic', 'name', 'sub_text', 'description', 'base_measurement_unit', 'price', 'show_price', 'status_note', 'slug', 'priority', 'product_base', 'measurement_unit']

    def get_product_id(self, obj):
        return obj.product.id

    def get_is_available(self, obj):
        return obj.is_available

    def get_name(self, obj):
        return str(obj.product.name)

    def get_slug(self, obj):
        return str(obj.product.slug)

    def get_status_note(self, obj):
        return str(obj.product.status_note)

    def get_measurement_unit(self, obj):
        m_units = []
        for e_m_unit in obj.product.measurement_unit.all():
            m_units.append(e_m_unit.id)
        return m_units

    def get_priority(self, obj):
        return str(obj.product.priority)

    def get_pic(self, obj):
        # if obj.product.pic is not None:
        if obj.product.pic and hasattr(obj.product.pic, 'url'):
            return str(obj.product.pic.url)
        else:
            return None

    def get_sub_text(self, obj):
        return str(obj.product.sub_text)

    def get_description(self, obj):
        return str(obj.product.description)

    def get_base_measurement_unit(self, obj):
        return str(obj.product.base_measurement_unit.id)

    def get_price(self, obj):
        return str(obj.product.price)

    def get_show_price(self, obj):
        return str(obj.product.show_price)

    def get_product_base(self, obj):
        return str(obj.product.id)


class ServisableProductSerializerBranchUser(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()
    show_price = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    base_measurement_unit = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    sub_text = serializers.SerializerMethodField()
    pic = serializers.SerializerMethodField()
    priority = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()
    product_base = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField()
    is_available = serializers.SerializerMethodField()
    status_note = serializers.SerializerMethodField()


    class Meta:
        model = BranchServisableProduct
        fields = ['id', "slug", "is_available", 'pic', 'name', 'sub_text', 'description', 'base_measurement_unit', 'price', 'show_price', 'status_note', 'slug', 'priority', 'product_base', 'measurement_unit']

    def get_is_available(self, obj):
        return obj.is_available

    def get_name(self, obj):
        return str(obj.product.name)

    def get_slug(self, obj):
        return str(obj.product.slug)

    def get_status_note(self, obj):
        return str(obj.product.status_note)

    def get_measurement_unit(self, obj):
        return str(obj.product.name)

    def get_priority(self, obj):
        return str(obj.product.priority)

    def get_pic(self, obj):
        # if obj.product.pic is not None:
        if obj.product.pic and hasattr(obj.product.pic, 'url'):
            return str(obj.product.pic.url)
        else:
            return None

    def get_sub_text(self, obj):
        return str(obj.product.sub_text)

    def get_description(self, obj):
        return str(obj.product.description)

    def get_base_measurement_unit(self, obj):
        return str(obj.product.base_measurement_unit)

    def get_price(self, obj):
        return str(obj.price)

    def get_show_price(self, obj):
        return str(obj.product.show_price)

    def get_product_base(self, obj):
        return str(obj.product.id)

class BranchAgentListSerializer(serializers.ModelSerializer):

    first_name = serializers.SerializerMethodField()

    class Meta:
        model = UserProfileInfo
        fields = ('id', 'first_name', 'phone_primary', 'location_area', 'location_sublocality', 'location_locality', 'location_city', 'location_pincode', 'is_active')
        # exclude = ['user']
    def get_first_name(self, obj):
        return obj.user.first_name


class BranchAgentDetailSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = UserProfileInfo
        fields = ('id', 'name', 'app_user_name', 'gender', 'phone_primary', 'location_city', 'location_pincode', 'is_active')

    def get_name(self, obj):
        return obj.user.first_name



# name": "Jercey Millk",
#             "name_tamil": "Jercey Millk",
#             "status_note": "Milk",
#             "is_available": true,
#             "slug": "jercey-millk"
#
# class DynamicFieldsModelSerializer(serializers.ModelSerializer):
#     """
#     A ModelSerializer that takes an additional `fields` argument that
#     controls which fields should be displayed.
#     """
#
#     def __init__(self, *args, **kwargs):
#         # Instantiate the superclass normally
#         super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)
#
#         # fields = self.context['request'].query_params.get('fields')
#         fields = kwargs.get("fields")
#         if fields:
#             fields = fields.split(',')
#             # Drop any fields that are not specified in the `fields` argument.
#             allowed = set(fields)
#             existing = set(self.fields.keys())
#             for field_name in existing - allowed:
#                 self.fields.pop(field_name)


class CMN_CommunicationVirtualModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CMN_CommunicationVirtualModel
        fields = '__all__'


class CMN_CommunicationPhysicalModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CMN_CommunicationPhysicalModel
        fields = '__all__'
        # , 'communication_type'
        # fields = ['address_line_01']
    def create(self, validated_data):
        print("testta")
        cMN_CommunicationPhysicalModel = CMN_CommunicationPhysicalModel.objects.create(**validated_data)
        return cMN_CommunicationPhysicalModel

    def update(self, instance, validated_data):
        print("testtau")
        # cMN_CommunicationPhysicalModel = CMN_CommunicationPhysicalModel.objects.create(**validated_data)
        # cMN_CommunicationPhysicalModel.save()
        # instance.

        field_arr = []
        #
        # form_fields = ["CMN_CommunicationVirtualModel__slug", "CMN_CommunicationVirtualModel__communication_type", "CMN_CommunicationVirtualModel__communication_channel_key", "CMN_CommunicationVirtualModel__communication_channel_value", "CMN_CommunicationPhysicalModel__communication_type", "CMN_CommunicationPhysicalModel__address_line_01", "CMN_CommunicationPhysicalModel__address_line_02", "CMN_CommunicationPhysicalModel__city", "CMN_CommunicationPhysicalModel__district", "CMN_CommunicationPhysicalModel__state", "CMN_CommunicationPhysicalModel__pincode"]
        # serializer = EnterPriseForm()
        # form_fields = []
        # field_arr =getSerilalierField(serializer,field_arr, "Parent", form_fields)
        #
        # for i in field_arr:
        #     print(i["cn"])
        #     name = i["cn"]
        #     # instance.name = validated_data.get(name, instance.name)
        #
        #
        # print(field_arr)

        instance.slug = validated_data.get("slug", instance.slug)
        instance.communication_type = validated_data.get("communication_type", instance.communication_type)
        instance.is_person = validated_data.get("is_person", instance.is_person)
        instance.address_line_01 = validated_data.get("address_line_01", instance.address_line_01)
        instance.address_line_02 = validated_data.get("address_line_02", instance.address_line_02)
        instance.city = validated_data.get("city", instance.city)
        instance.district = validated_data.get("district", instance.district)
        instance.state = validated_data.get("state", instance.state)
        instance.country = validated_data.get("country", instance.country)
        instance.pincode = validated_data.get("pincode", instance.pincode)

        instance.save()


        return instance

class CMN_CommunicationVirtualModelSerializer(serializers.ModelSerializer):

    # full_name = serializers.SerializerMethodField()
    # full_name = serializers.IntegerField(required=True)

    class Meta:
        model = CMN_CommunicationVirtualModel
        fields = '__all__'
        # fields = ['slug', 'communication_type']
        # extra_kwargs = {'slug': {'required': False}}

    def create(self, validated_data):
        print("testta")
        cMN_CommunicationVirtualModel = CMN_CommunicationVirtualModel.objects.create(**validated_data)
        return cMN_CommunicationVirtualModel





def getSerilalierField(serializer_obj,field_arr, model ,form_fields ):
    for field_name, field_obj in serializer_obj.get_fields().items():

        if 'Serializer' in field_obj.__class__.__name__ and field_obj.__class__.__name__ != 'SerializerMethodField':
            field_arr=getSerilalierField(field_obj, field_arr, field_obj.__class__.__name__, form_fields)
        else:
            # print(field_name)
            # name_final = model.replace("ModelSerializer", "Model")+"__"+field_name
            # name_final = name_final.replace("SerializerModel__", "Model__")
            # if name_final in form_fields:
            each_obj ={}
            # each_obj['model'] = model
            each_obj['cn'] = field_name
            each_obj['dt'] = field_obj.help_text
            each_obj['dt_r'] = field_obj.__class__.__name__
            each_obj['required'] = field_obj.required


            # if hasattr(field_obj, 'verbose_name'):
            #     each_obj['lb'] = field_obj.verbose_name
            # else:
            #     v_name = field_name.replace("_"," ")
            #     each_obj['lb'] = v_name
            #
            # if hasattr(field_obj, 'choices'):
            #    each_obj['choices'] = field_obj.choices
               # each_obj['dt'] = 'MOD_DT_CHOICES'
            # if hasattr(field_obj, 'label'):
            #    each_obj['lb'] = field_obj.label
            field_arr.append(each_obj)
    return field_arr;



class EnterPriseForm(serializers.Serializer):

    # fields =  ['slug']
    # fields=['slug']


    communication_virtual = CMN_CommunicationVirtualModelSerializer()
    communication_physical = CMN_CommunicationPhysicalModelSerializer()

# class GenericSerializer():

# class frm_enterprise(serializers.ModelSerializer):

# class GeneralViewSet(viewsets.ModelViewSet):
#
#      def get_queryset(self):
#          model = self.kwargs.get('model')
#          return model.objects.all()
#
#      def get_serializer_class(self):
#          GeneralSerializer.Meta.model = self.kwargs.get('model')
#          return GeneralSerializer

def serializer_factory(model, base=serializers.ModelSerializer,
                       fields=None, exclude=None):
    attrs = {'model': model}
    if fields is not None:
        attrs['fields'] = fields
    if exclude is not None:
        attrs['exclude'] = exclude

    parent = (object,)
    if hasattr(base, 'Meta'):
        parent = (base.Meta, object)
    Meta = type(str('Meta'), parent, attrs)
    if model:
        class_name = model.__name__ + 'Serializer'
    else:
        class_name = 'Serializer'
    return type(base)(class_name, (base,), {'Meta': Meta, })







# class DynamicFieldsSerializerMixin(object):
#
#     def __init__(self, *args, **kwargs):
#         # Don't pass the 'fields' arg up to the superclass
#         fields = kwargs.pop('fields', None)
#
#         # Instantiate the superclass normally
#         super(DynamicFieldsSerializerMixin, self).__init__(*args, **kwargs)
#
#         if fields is not None:
#             # Drop any fields that are not specified in the `fields` argument.
#             allowed = set(fields)
#             existing = set(self.fields.keys())
#             for field_name in existing - allowed:
#                 self.fields.pop(field_name)


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
