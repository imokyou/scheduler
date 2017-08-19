from django.conf.urls import url
import views
urlpatterns = [
    url(r'^test/$', views.test),
    url(r'^codes/$', views.get_codes),
    url(r'^new/$', views.add_codememo),
    url(r'^(\d+)/update/$', views.update_codememo),
    url(r'^(\d+)/delete/$', views.delete_codememo)
]
