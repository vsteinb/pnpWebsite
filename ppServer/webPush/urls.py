from django.urls import path

from . import views

app_name = 'web_push'

urlpatterns = [
    path('settings', views.SettingView.as_view(), name='settings'),
    path('test', views.TestView.as_view(), name='test'),

    # POST only
    path('push_settings', views.save_push_settings, name='push_settings'),
    path('subscribe_user', views.register_webpush, name='subscribe_user'),
    path('send_testmessage', views.send_testmessage, name='send_testmessage'),
]
