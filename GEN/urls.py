from django.urls import path
from GEN import views
# from .views import EnterPriseForm

app_name = 'GEN'

urlpatterns =[
path('',views.get_html_index, name = "index"),
path('safez/',views.get_html_safez, name = ""),
path('safez/privacy-policy/',views.get_html_privacy_policy, name = ""),
path('safez/terms-of-use/',views.get_html_terms_and_conditions, name = ""),
path('user_login/',views.user_login, name = "user_login"),

path('StoreBranchList/',views.StoreBranchList.as_view(), name = "StoreBranchList"),
path('StoreBranchListAdmin/',views.StoreBranchListAdmin.as_view(), name = "StoreBranchListAdmin"),
path('StoreCategoryListAd/',views.StoreCategoryListAd.as_view(), name = "StoreCategoryListAd"),
path('StoreUomList/',views.StoreUomList.as_view(), name = "StoreUomList"),
path('StoreCategoryList/',views.StoreCategoryList.as_view(), name = "StoreCategoryList"),
path('BranchAgentList/',views.BranchAgentList.as_view(), name = "BranchAgentList"),
path('index/',views.index, name = "index"),
path('orders_list/', views.orders_list, name = "orders_list"),
path('change_product_status/', views.change_product_status, name = "change_product_status"),
# path('EnterPriseForm/', views.EnterPriseForm.as_view(), name = "EnterPriseForm"),
path('orders_list/',views.orders_list, name = "orders_list1"),
path('order_create/',views.order_create, name = "order_create"),

path('GetBrandBranchDetailAdmin/',views.GetBrandBranchDetailAdmin.as_view(), name = "GetBrandBranchDetailAdmin"),
path('CreateBrandBranch/',views.CreateBrandBranch.as_view(), name = "CreateBrandBranch"),
path('CreateUpdateDataset/',views.CreateUpdateDataset.as_view(), name = "CreateUpdateDataset"),
path('CreateProductCategory/',views.CreateProductCategory.as_view(), name = "CreateProductCategory"),
path('CreateProduct/',views.CreateProduct.as_view(), name = "CreateProduct"),

path('login/',views.user_login, name = "login"),
path('logout/',views.user_logout, name = "logout"),
path('validate_user/',views.validate_user, name = "validate_user"),
path('authenticate_app_user/',views.authenticate_app_user, name = "authenticate_app_user"),
path('register_user/',views.register_user, name = "register_user"),
path('RegisterAgent/',views.RegisterAgent, name = "RegisterAgent"),
path('ProductList/', views.ProductList.as_view(), name = "ProductList"),
path('UpdateUserDetails/', views.UpdateUserDetails.as_view(), name = "UpdateUserDetails"),
path('UpdateServisableCategoryDetails/', views.UpdateServisableCategoryDetails.as_view(), name = "UpdateServisableCategoryDetails"),
path('UpdateServisableProduct/', views.UpdateServisableProduct.as_view(), name = "UpdateServisableProduct"),
path('UpdateCategoryDetails/', views.UpdateCategoryDetails.as_view(), name = "UpdateCategoryDetails"),
path('BranchProductListAdmin/', views.BranchProductListAdmin.as_view(), name = "BranchProductListAdmin"),
path('BrandProductListAdmin/', views.BrandProductListAdmin.as_view(), name = "BrandProductListAdmin"),
path('BranchProductListServisableCategorySpecific/', views.BranchProductListServisableCategorySpecific.as_view(), name = "BranchProductListServisableCategorySpecific"),
path('BranchProductListServisableCategorySpecificDisabled/', views.BranchProductListServisableCategorySpecificDisabled.as_view(), name = "BranchProductListServisableCategorySpecificDisabled"),
path('BranchProductListCustomer/', views.BranchProductListCustomer.as_view(), name = "BranchProductListCustomer"),
path('BranchProductListAdmin2/', views.BranchProductListAdmin2.as_view(), name = "BranchProductListAdmin2"),
path('BranchProductSupportDataCustomer/', views.BranchProductSupportDataCustomer.as_view(), name = "BranchProductSupportDataCustomer"),

path('SymptomSet/', views.SymptomSet.as_view(), name = "SymptomSet"),
path('CustomerOrder/', views.CustomerOrder.as_view(), name = "CustomerOrder"),
path('AgentDetail_AD/', views.AgentDetail_AD.as_view(), name = "AgentDetail_AD"),
path('CustomerOrderUpcoming/', views.CustomerOrderUpcoming.as_view(), name = "CustomerOrderUpcoming"),
path('CustomerOrderOthers/', views.CustomerOrderOthers.as_view(), name = "CustomerOrderOthers"),
path('OrderAcceptedByAgent/', views.OrderAcceptedByAgent.as_view(), name = "OrderAcceptedByAgent"),
path('OrderRejectedByAgent/', views.OrderRejectedByAgent.as_view(), name = "OrderRejectedByAgent"),
path('OrderCancelledByAgent/', views.OrderCancelledByAgent.as_view(), name = "OrderCancelledByAgent"),
path('OrderMarkedNoShowByAgent/', views.OrderMarkedNoShowByAgent.as_view(), name = "OrderMarkedNoShowByAgent"),
path('OrderMarkAsCompleted/', views.OrderMarkAsCompleted.as_view(), name = "OrderMarkAsCompleted"),
path('OrderMarkAsCheckedIn/', views.OrderMarkAsCheckedIn.as_view(), name = "OrderMarkAsCheckedIn"),

path('SamplePush/', views.SamplePush.as_view(), name = "SamplePush"),
path('BrandOrders/', views.BrandOrders.as_view(), name = "BrandOrders"),
path('BrandBranchOrders/', views.BrandBranchOrders.as_view(), name = "BrandBranchOrders"),
path('BrandBranchOrdersOngoing/', views.BrandBranchOrdersOngoing.as_view(), name = "BrandBranchOrdersOngoing"),
path('BrandBranchOrdersPendingApproval/', views.BrandBranchOrdersPendingApproval.as_view(), name = "BrandBranchOrdersPendingApproval"),
path('BrandBranchOrdersUpcoming/', views.BrandBranchOrdersUpcoming.as_view(), name = "BrandBranchOrdersUpcoming"),
path('GetOrderDetails01/', views.GetOrderDetails01.as_view(), name = "GetOrderDetails01"),
path('GetOrderAgentResponse/', views.GetOrderAgentResponse.as_view(), name = "GetOrderAgentResponse"),
path('BaGetOrderDetailswithActions/', views.BaGetOrderDetailswithActions.as_view(), name = "BaGetOrderDetailswithActions"),

path('product_list/', views.product_list, name = "product_list"),
path('change_order_status/', views.change_order_status, name = "change_order_status"),
path('alter_order_item/', views.alter_order_item, name = "alter_order_item"),
path('alter_order/', views.alter_order_item, name = "alter_order"),
path('order_details/', views.order_details, name = "order_details"),
path('order_list_user/', views.order_list_user, name = "order_list_user"),
path('order_create_m/', views.CreateOrder.as_view(), name = "order_create_m"),

path('customer_heatmap/', views.customer_heatmap, name = "customer_heatmap"),

path('validate_app/',views.validate_app, name = "validate_app"),
path('product_list_suggestion/',views.product_list_suggestion, name = "product_list_suggestion"),
path('get_user_suggestion_list/',views.get_user_suggestion_list, name = "get_user_suggestion_list"),
path('get_user_details/',views.get_user_details, name = "get_user_details"),
path('feed_contact/',views.feed_contact, name = "feed_contact"),
path('feed_news/',views.feed_news, name = "feed_news"),
path('submit_symptoms/',views.submit_symptoms, name = "submit_symptoms"),
path('customer_list/',views.customer_list, name = "customer_list"),
path('change_user_status/',views.change_user_status, name = "change_user_status"),
path('change_order_status_auto/',views.change_order_status_auto, name = "change_order_status_auto"),


# path('posta/',views.posta, name = "posta"),
# posta
 ]
