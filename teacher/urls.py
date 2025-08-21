from django.urls import path
from . import views


urlpatterns = [
    path('manage-courses/', views.CoursesManageListView.as_view(), name="CoursesManage"),
    path('manage-units/course/<int:course_id>/', views.UnitsManageListView.as_view(), name="UnitsManage"),
    path('manage-lessons/course/<int:course_id>/unit/<int:unit_id>/', views.LessonsManageListView.as_view(), name="LessonsManage"),
    
    path('course/create/', views.CourseCreateView.as_view(), name='CourseCreate'),
    path('unit/create/', views.UnitCreateView.as_view(), name='UnitCreate'),
    path('lesson/create/', views.LessonCreateView.as_view(), name='LessonCreate'),

    path('course/delete/<int:pk>/', views.delete_course, name='CourseDelete'),
    path('unit/delete/<int:pk>/', views.delete_unit, name='UnitDelete'),
    path('lesson/delete/<int:pk>/', views.delete_lesson, name='LessonDelete'),

    path('course/<int:pk>/update/', views.CourseUpdateView.as_view(), name='CourseUpdate'),
    path('unit/<int:pk>/update/', views.UnitUpdateView.as_view(), name='UnitUpdate'),
    path('lesson/<int:pk>/update/', views.LessonUpdateView.as_view(), name='LessonUpdate'),
]
