from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import custom_logout_view,goodbye_view


urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html'), name='login'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('goodbye/', views.goodbye_view, name='goodbye'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),

    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),
]