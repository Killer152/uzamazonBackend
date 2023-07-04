"""e_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from e_shop import settings

schema_view = get_schema_view(
   openapi.Info(title="UzAmazon API", default_version='v0.1'),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', include(('shop.urls', 'shop'), namespace='shop')),
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0)),

    path('account/', include(('account.urls', 'account'), namespace='account')),
    path('cart/', include(('cart.urls', 'cart'), namespace='cart')),
    path('order/', include(('orders.urls', 'orders'), namespace='order')),
    path('review/', include(('reviews.urls', 'reviews'), namespace='review')),
    path('vendors/', include(('vendors.urls', 'vendors'), namespace='vendor')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
