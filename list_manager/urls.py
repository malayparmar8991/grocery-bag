from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('listview/', views.listView, name="listview"),
    path('item_form/', views.itemForm, name="item_form"),
    path('add_item/', views.addItem, name="add_item"),
    path('update_form/<str:pk>/', views.updateForm, name="update_form"),
    path('update_item/', views.updateItem, name="update_item"),
    path('delete_item/', views.deleteItem, name="delete_item"),
    path('logout/', views.logoutUser, name="logout"),
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
]