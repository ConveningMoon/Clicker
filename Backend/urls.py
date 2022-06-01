from django.urls import path
from . import views

boosts = views.BoostViewSet.as_view({   
    'get': 'list',
    'post': 'create',
})

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('call_click/', views.call_click),
    path('logout/', views.user_logout, name='logout'),
    path('', views.index, name='index'),
    path('boosts/', boosts, name='boosts'),
]