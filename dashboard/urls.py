from django.urls import path

from . import views

urlpatterns = [
    path('', views.SelectSession.as_view(), name='select_session'),
    path('dashboard', views.Dashboard.as_view(), name='dashboard'),
    path('voucher', views.CreateVoucher.as_view(), name='create_voucher'),
    path('test_voucher', views.test_voucher, name='test_voucher'),
    path('create_session', views.CreateSession.as_view(), name='create_session'),
]
