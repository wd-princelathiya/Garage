from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.log_in, name='log_in'),
    path('logout/', views.log_out, name='log_out'),
    path('buy/', views.buy, name='buy'),
    path('sell/', views.sell, name='sell'),
    path('buy/<int:product_id>/', views.profile, name='profile')
]
