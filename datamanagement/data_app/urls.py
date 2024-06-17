from django.urls import path
from . import views

urlpatterns = [
    path('', views.base_view, name='base'),
    path('checker_register/', views.checker_register, name='checker_register'),
    path('maker_register/', views.maker_register, name='maker_register'),
    path('login/', views.user_login, name='loginpage'),
    path('logout/', views.logout_view, name='logout'),
    path('create_customer/', views.create_customer, name='create_customer'),
    path('success/', views.success_page, name='success_page'),
    path('view_customer/<int:customer_id>/', views.view_customer, name='view_customer'),
    path('update_customer/<int:customer_id>/', views.update_customer, name='update_customer'),
    path('delete_customer/<int:customer_id>/', views.delete_customer, name='delete_customer'),
    path('maker_home/',views.maker_home,name='maker_home'),
    path('checker_home/', views.checker_home, name='checker_home'),
    path('maker_list/<int:maker_id>/', views.maker_list, name='maker_list'),
    path('maker/<int:maker_id>/', views.maker_detail, name='maker_detail'),
    path('view_customers/', views.view_customers, name='view_customers'),
    path('update_customer_status/<int:customer_id>/', views.update_customer_status, name='update_customer_status'),
    path('maker_list/<int:maker_id>/', views.maker_list, name='maker_list'),
    path('maker_detail/<int:maker_id>/', views.maker_detail, name='maker_detail'),
    path('delete_maker/<int:maker_id>/', views.delete_maker, name='delete_maker'),
]