from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/create/', views.post_create, name='post_create'),
    path('post/<int:pk>/update/', views.post_update, name='post_update'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('post/<int:pk>/like/', views.post_like, name='post_like'),
    path('post/<int:pk>/comment/', views.comment_create, name='comment_create'),
    path('comment/<int:pk>/delete/', views.comment_delete, name='comment_delete'),
    path('story/create/', views.story_create, name='story_create'),
    path('follow/<int:user_id>/', views.follow_toggle, name='follow_toggle'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('search/', views.user_search, name='user_search'),
]