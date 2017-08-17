# coding=utf-8
from django.conf.urls import include, url
from app.schedule import views as schedule


# 总的URL设置,新版本按下面的来不会有warning.
urlpatterns = [
    url(r'^api/common/', include('app.common.urls')),
    url(r'^api/schedules/', schedule.get_list),
    url(r'^api/schedule/', include('app.schedule.urls')),
    url(r'^api/codememo/', include('app.codememo.urls')),
]
