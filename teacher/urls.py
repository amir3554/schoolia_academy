from django.urls import path
from . import views


urlpatterns = [
    path('course/create/', views.CourseCreateView.as_view(), name='CourseCreate'),
    path('unit/create/', views.UnitCreateView.as_view(), name='UnitCreate'),
    path('lesson/create/', views.LessonCreateView.as_view(), name='LessonCreate'),
    path('course/<int:pk>/update/', views.CourseUpdateView.as_view(), name='CourseUpdate'),
    path('unit/<int:pk>/update/', views.UnitUpdateView.as_view(), name='UnitUpdate'),
    path('lesson/<int:pk>/update/', views.LessonUpdateView.as_view(), name='LessonUpdate'),
]
