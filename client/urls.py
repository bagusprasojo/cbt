from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('ujian/', views.ujian, name='ujian'),
    path('hasil/', views.hasil, name='hasil_ujian'),
    path('', auth_views.LoginView.as_view(template_name='client/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('tinjau/', views.tinjau_soal, name='tinjau_soal'),
]
