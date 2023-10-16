from django.urls import path
from . import views

urlpatterns = [
    path('', views.select_option, name='select'),
    path('verify/', views.verify, name='verify'),
    path('exist/<str:certificate_slug>/', views.exist, name='exist'),
    path('inexistent/', views.inexistent, name='inexistent'),
    path('qr-scan-redirect/<str:qr_slug>/', views.qr_scan_redirect, name='qr-scan-redirect'),
    path('qr-scan/', views.qr_scan_view, name='qr-scan'),
    path('enter-email/', views.request_email, name='enter-email'),
    path('enter-otp/', views.verify_otp, name='enter-otp'),
    path('store-harshcode/', views.store_harshcode, name='store-harshcode'),
    path('test/', views.test, name='test'),
    path('existqr/<str:hashcode>/', views.qr_scan_redirect, name='qr-scan-redirect'),

]


