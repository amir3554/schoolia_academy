from django.urls import path
from . import views

urlpatterns = [
    path('articles-list/', views.articles_list, name='ArticleList'),
    path('my-articles-list/', views.my_articles, name='MyArticles'),
    path('article/<int:article_id>/', views.article_detail, name="Article"),
    path('article/create/', views.article_create, name="ArticleCreate"),
    path('article/<int:article_id>/update/', views.article_update, name="ArticleUpdate"),
    path('comment-add-article/<int:article_id>/', views.comment_add_article, name="CommentAddArticle"),
    path('comment-add-comment-article/<int:article_id>/<int:comment_id>/', views.comment_add_comment_article, name='CommentAddCommentArticle'),
]
