from django.urls import path
from . import views

urlpatterns = [
    path('', views.idea_list, name='idea_list'),
    path('<int:pk>/', views.idea_detail, name='idea_detail'),
    path('create/', views.idea_create, name='idea_create'),
    path('<int:pk>/update/', views.idea_update, name='idea_update'),
    path('<int:pk>/delete/', views.idea_delete, name='idea_delete'),
    path('<int:pk>/star/', views.idea_star, name='idea_star'),
    path('<int:pk>/interest/<str:action>/', views.idea_interest, name='idea_interest'),

    # 개발툴
    path('devtool/', views.devtool_list, name='devtool_list'),
    path('devtool/<int:pk>/', views.devtool_detail, name='devtool_detail'),
    path('devtool/create/', views.devtool_create, name='devtool_create'),
    path('devtool/<int:pk>/update/', views.devtool_update, name='devtool_update'),
    path('devtool/<int:pk>/delete/', views.devtool_delete, name='devtool_delete'),
]