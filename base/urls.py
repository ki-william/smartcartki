from django.urls import path,include
from rest_framework.authtoken import views as v
from . import views

urlpatterns = [
    path('api/login', views.CustomAuthToken.as_view() , name="login"),
    path('api/register', views.register_user , name="register"),
    path('api/user-profile', views.user_profile , name="user-profile"),

    path('api/create_order', views.create_order , name="create-order"),
    path('api/add_orderItems', views.adding_orderItem , name="add-orderItems"),

    path('api/orders/logged-in-user/', views.user_orders, name='logged-in-user'),
    path('api/orders/logged-in-user/<int:id>', views.get_order_details, name="get_order_detail"),


    path('api/products', views.products_list , name="product-list"),

    path('api/orders', views.orders_list , name="orders-list"),

    path('api/all-users', views.get_all_users, name="all-users"),
    path('api/all-rates', views.get_all_rates, name="all-rates"),
    

    path('api/ml-ratings', views.mlmodel, name="mlmodel"),
    path('api/product', views.specificproduct, name="specificproduct"),

    path('api/carts', views.carts, name="carts"),

    path('api/cart', views.cart, name="cart"),

    path('api/reservercart', views.reservercart, name="reservercart"),

    path('api/unreservercart', views.unreservecart, name="unreservecart"),



    ##Nanil latest update for URLs
    path('api/login-cart', views.send_and_receive, name="login-cart"),
    path('api/confirm-login-cart', views.send_and_receive, name="confirm-login-cart"),
    path('api/logout-cart', views.send_and_receive, name="logout-cart"), 
    path('api/confirm-logout-cart', views.send_and_receive, name="confirm-logout-cart"),

    path('api/recommendations', views.recommendations, name="recommendations"),

    path('api/recharge', views.recharge, name="recharge"),

    path('__debug__/', include('debug_toolbar.urls')),

]