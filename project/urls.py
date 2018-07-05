"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from django.conf.urls import url
from ProjectMy import views
from project import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.shops_all ),
    url(r'^insert_data/$', views.insert_data),
    url(r'^url_params/$', views.params),
    url(r'^res/$', views.index),
    url(r'^select_data/$', views.select_data),
    url(r'^update_data/$', views.update_data),
    url(r'^delete_data/$', views.delete_data),
    url(r'^my_view/$', views.MyView.as_view()),
    url(r'^shops/', include([
        url(r'^$', views.shops, name = 'index'),
        url(r'^add/$', views.AddShop.as_view()),
        url(r'^(\d)/', include([
            url(r'^$',views.shop_id),
            url(r'^add/$', views.DepAdd.as_view(), name = 'add_dep' )
            ]))
        ])),
    url(r'^items/(?P<item_id>\d+)/',
        include([url(r'^update/$', views.EditItem.as_view(), name='update'),
                 url(r'^delete/$', views.delete_object, name='delete')])),
    url(r'^templates/$', views.template),
    url(r'^simple_form/$', views.SimpleFormView.as_view()),
    url(r'^item_create/$', views.ItemCreateView.as_view()),
#    url(r'^simple_form_result/$', views.SimpleFormView.as_view())
    url(r'^search/$', views.Search.as_view()),
#    url(r'^result/$', views.Search.as_view()),
     url(r'^update_item/(?P<pk>\d+)/$', views.UpdateItemView.as_view()),
    url(r'^delete_item/(?P<pk>\d+)/$', views.ItemDeleteView.as_view()),
]
# (?p<pk>\d+) для updateview
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)