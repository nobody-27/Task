from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from task import views

urlpatterns = [
    path('user-list/',views.UserList.as_view(),name="user_list"),
    path('',views.UploadFile.as_view(),name="api_chunked_upload"),
    path('completed/',csrf_exempt(views.upload_complated),name="completed"),
    path('search/',views.Searh.as_view(),name="search"),
    path('query_builder/',views.query_builder,name="query_builder"),
    path('add-user/',views.addUser,name="add_user"),
    path('edit-user/<int:id>/',views.editUser,name="edit_user")

]
