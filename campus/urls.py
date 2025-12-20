from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_material, name='upload'),
    path('register/', views.register_course, name='register'),
    path('subject/<int:subject_id>/', views.subject_courses, name='subject_courses'),
    path('level/<str:level>/', views.level_courses, name='level_courses'),
    path('course/<int:course_id>/', views.course_details, name='course_details'),
    path('search/', views.search, name='search'),
    path('material/<int:material_id>/preview/', views.preview_material, name='preview')
]