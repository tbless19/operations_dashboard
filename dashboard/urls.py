from django.urls import path,include
from .import views

urlpatterns = [
    path('',views.dashboard, name='base'),
    path('data/', views.get_data),
    #path('reset/',views.line_swap, name= 'reset'),
]