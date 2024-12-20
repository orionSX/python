from django.urls import path
from . import views

urlpatterns = [
    # Главная страница
    path('', views.index, name='index'),

    # CRUD для Dancer
    path('dancer/add/', views.add_or_edit_dancer, name='add_dancer'),
    path('dancer/edit/<int:id>/', views.add_or_edit_dancer, name='edit_dancer'),
    path('dancer/delete/<int:id>/', views.delete_dancer, name='delete_dancer'),
    path('dancer/<int:id>/', views.dancer_detail, name='dancer_detail'),

    # CRUD для DanceGroup
    path('groups/', views.list_groups, name='list_groups'),
    path('group/add/', views.add_or_edit_group, name='add_group'),
    path('group/edit/<int:id>/', views.add_or_edit_group, name='edit_group'),
    path('group/delete/<int:id>/', views.delete_group, name='delete_group'),

    # CRUD для DanceStyle
    path('styles/', views.list_styles, name='list_styles'),
    path('style/add/', views.add_or_edit_style, name='add_style'),
    path('style/edit/<int:id>/', views.add_or_edit_style, name='edit_style'),
    path('style/delete/<int:id>/', views.delete_style, name='delete_style'),

    # CRUD для Performance
    path('performances/', views.list_performances, name='list_performances'),
    path('performance/add/', views.add_or_edit_performance, name='add_performance'),
    path('performance/edit/<int:id>/', views.add_or_edit_performance, name='edit_performance'),
    path('performance/delete/<int:id>/', views.delete_performance, name='delete_performance'),
]
