from django.urls import path
from . import views


urlpatterns = [
    path('', views.starttest, name = 'starttest'),
    path('test_first/<int:user_id>/<int:vibor_test_id>/', views.test_first),
    path('test/<int:user_id>/<int:vibor_test_id>/<int:question_id>/', views.test),






    ]
