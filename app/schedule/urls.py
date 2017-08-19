from django.conf.urls import url
import views
urlpatterns = [
    url(r'^test/$', views.test),
    url(r'^new/$', views.add_schedule),
    url(r'^(\d+)/$', views.get_schedule),
    url(r'^(\d+)/update/$', views.update_schedule),
    url(r'^(\d+)/delete/$', views.delete_schedule),

    url(r'^(\d+)/configs/$', views.schedule_configs),
    url(r'^(\d+)/config/new/$', views.add_schedule_config),
    url(r'^(\d+)/config/(\d+)/update/$', views.update_schedule_config),
    url(r'^(\d+)/config/(\d+)/delete/$', views.delete_schedule_config),
]
