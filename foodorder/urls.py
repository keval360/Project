"""
URL configuration for food_order_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .import views as v

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',v.home),
    path('reg',v.adduser),
    path('log',v.login_view),
    path('out',v.logout_view),
    path('product',v.product_list),
    path('addtocart/<int:pid>',v.add_to_cart),
    path('clist',v.cart_list),
    path('about',v.about),
    path('delete/<int:pid>',v.remove_from_cart),
    path('order',v.order),
    path('success',v.success_view),
]
