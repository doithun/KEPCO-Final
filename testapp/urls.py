
from django.contrib import admin
from django.urls import path
from django.contrib import admin
from . import views
from testapp import views as ts


urlpatterns = [
     path('',views.index),
     path('index/',views.index),
     path('mem_insert/',views.MemberInsert),
     path('mem_plus/',views.memcreate),
     path('mem_delete/',views.MemberDelete),
     path('mem_minus/',views.getdelete),
     path('mem_update/',views.MemberUpdate),
     path('login_logout/',views.login_logout),
     path('login/',views.login),
     path('logout/',views.logout),
     path('update/',views.MemberUpdate),
     path('mypage/',views.mypage),
     ##################################
     
     path('photo/',views.getPhoto),  
     path('photo_save/',views.getPhoto_save),
     path('photo_create/',views.getcreate),
     path('photo_output',views.getoutput),
] 

