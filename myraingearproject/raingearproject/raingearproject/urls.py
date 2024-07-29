"""
URL configuration for raingearproject project.

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
from myraingearapp import views
from django.conf import settings
from django.conf.urls.static import static
from myraingearapp.views import Productlist, Sellerproductlist, Addproduct, Updateproduct, Deleteproduct, Productdetail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('search/', views.search, name='search'),
    path('addtocart/', views.addtocart, name='addtocart'),
    path('viewcart/', views.viewcart, name='viewcart'),
    path('summary/', views.summary, name='summary'),
    path('payment/', views.payment, name='payment'),
    path('paymentsuccess/', views.paymentsuccess, name='paymentsuccess'),
    path('productlist/', Productlist.as_view(), name="productlist"),
    path('sellerproductlist/', Sellerproductlist.as_view(), name="sellerproductlist"),
    path('addproduct/', Addproduct.as_view(),name="addproduct"),
    path('updateproduct/<int:pk>/', Updateproduct.as_view(),name="updateproduct"),
    path('productdetail/<int:pk>/', Productdetail.as_view(),name='productdetail'),
    path('deleteproduct/<int:pk>/', Deleteproduct.as_view(),name='deleteproduct'),
    path('logout', views.logout, name='logout'),    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
