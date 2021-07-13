from django import forms
from django.contrib.auth.models import User
from GEN.models import UserProfileInfo, Order, OrderItem, OrderLog, OrderItemLog, UserHealthProfile
from GEN import dbconstants


class UserHealthProfileForm(forms.ModelForm):

    class Meta():
        model = UserHealthProfile
        fields = ('user', 'symptom', 'note')
        exclude = ['user', 'symptom']


class OrderLogForm(forms.ModelForm):

    class Meta():
        model = OrderLog
        fields = ('status', 'order')
        exclude = ['order']


class OrderItemLogForm(forms.ModelForm):

    class Meta():
        model = OrderItemLog
        fields = ('status', 'order_item')
        exclude = ['order_item']


class IOrderForm(forms.ModelForm):

    class Meta():
        model = Order
        fields = ('order_id', 'user_customer', 'delivery_charges', 'schedule_requested_time')
        exclude = ['user_customer', 'order_id']

class IOrderItemForm(forms.ModelForm):

    class Meta():
        model = OrderItem
        fields = ('order_item_id', 'product', 'item_name', 'item_quantity', 'order', 'measurement_unit')
        exclude = ['order_item_id', 'measurement_unit', 'product', 'order']

class UserParentForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'email', 'password')
        # exclude = ['username']
class UserFormCustomer(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'email', 'password', 'first_name')
        # exclude = ['username']

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'email', 'password', 'first_name')
        # exclude = ['username']


class UserProfileInfoForm(forms.ModelForm):

    class Meta():
        model = UserProfileInfo
        fields = ('phone_primary', 'user_language', 'phone_secondary', 'age', 'gender', 'location_latitude','location_longitude', 'phone_secondary', 'location_area','location_sublocality','location_locality','location_city','location_pincode')
        #


class OrderForm(forms.ModelForm):
    class Meta():
        model = Order
        fields = ( 'delivery_charges', 'status_note')
        exclude = ['delivery_charges', 'status_note']
    # def __init__(self, *args, **kwargs):
    #     super(OrderForm, self).__init__(*args, **kwargs)
    #     self.fields['user_delivery_agent'].required = False


    # customer_name = forms.CharField(label='Customer Name', max_length=50)
    # phone_primary = forms.CharField(max_length=10, label='Phone Number' )
    # location_sublocality = forms.CharField(max_length=80, label='Address' )
    # location_locality = forms.CharField(max_length=80, label='Locality')
    # location_city = forms.CharField(max_length=80,  label='City')
    # location_state = models.CharField(max_length=80, unique=False, default="KERALA")
    # location_pincode = forms.CharField(max_length=6, label='Pincode')
    # delivery_agent = forms.ModelChoiceField(queryset=UserProfileInfo.objects.prefetch_related('user').filter(user_type = dbconstants.USER_TYPE_DELIVERY_AGENT))
    # UserProfileInfo.objects.prefetch_related('user').filter(user_type = dbconstants.USER_TYPE_DELIVERY_AGENT)
    # forms.ModelChoiceField(queryset=User.objects.all().order_by('username'))
    # forms.CharField(max_length=80,  label='Delivery Agent')


class OrderItemForm(forms.ModelForm):

    class Meta():
        model = OrderItem
        fields = ('measurement_unit', 'item_name', 'item_quantity')
        exclude = ['measurement_unit','item_name','item_quantity']
