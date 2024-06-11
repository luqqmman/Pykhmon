from django.urls import path

from . import views

urlpatterns = [
    path('', views.SelectSession.as_view(), name='select_session'),
    path('dashboard', views.Dashboard.as_view(), name='dashboard'),
    path('session/create', views.CreateSession.as_view(), name='create_session'),
    path('profile/create', views.CreateProfile.as_view(), name='create_profile'),
    path('profile/list', views.ListProfile.as_view(), name='list_profile'),
    path('voucher/create', views.CreateVoucher.as_view(), name='create_voucher'),
    path('voucher/list', views.ListVoucher.as_view(), name='list_voucher'),
    path('pdf/list', views.ListVoucherPdf.as_view(), name='list_voucher_pdf'),
    path('pdf/<int:pk>', views.DetailVoucherPdf.as_view(), name='detail_voucher_pdf'),
    path('income/', views.Income.as_view(), name='income'),


]
