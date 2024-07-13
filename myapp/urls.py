from django.urls import path
from . import views


urlpatterns=[
    path('store/', views.store_data, name='store_data'),
    path('fetch/', views.fetch_data, name='fetch_data')
]