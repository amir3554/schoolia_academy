from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from school.models import  Comment
from .models import Article


@login_required
def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id, student=request.user)
    comments = (Comment.objects
                .filter(receiver_content_type__model='article',
                        receiver_object_id=article.pk)
                .select_related('sender')
                .prefetch_related('children__sender')
                .order_by('-created_at'))
    return render(request, 'article.html', {
        'article': article,
        'comments': comments
    })

@login_required
def article_create(request):
    if request.method == 'POST':
        try:
            a = Article.objects.create(
                title=request.POST['title'],
                content=request.POST['content'],
                image=request.FILES.get('image'),
                student=request.user
            )
            return redirect('Article', a.pk)
        except:
            return render(request, 'article_form.html', {'article': None})
        
    return render(request, 'article_form.html', {'article': None})


@login_required
def article_update(request, article_id):
    article = get_object_or_404(Article, pk=article_id, student=request.user)
    if request.method == 'POST':
        article.title = request.POST.get('title') or article.title
        article.content = request.POST.get('content') or article.content
        if request.FILES.get('image'):
            article.image = request.FILES['image']
        article.save()
        return redirect('Article', article.pk)
    return render(request, 'article_form.html', {'article': article})


def articles_list(request):
    articles = Article.objects.all().order_by("-created_at")
    paginator = Paginator(articles, 15)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.page(page_number)
    return render(request, "article_list.html", { 'articles' : page_obj } )


@login_required
def my_articles(request):
    articles = Article.objects.filter(student=request.user).order_by("-created_at")
    paginator = Paginator(articles, 15)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.page(page_number)
    return render(request, "article_list.html", { 'articles' : page_obj } )


@login_required
@require_http_methods(['POST'])
def comment_add_comment_article(request, article_id, comment_id):
    article = get_object_or_404(Article.objects.only('id'), id=article_id)
    parent = get_object_or_404(Comment.objects.only("id"), id=comment_id)
    content = request.POST.get('content')
    if content is None:
        return redirect("Article", article.pk)
    Comment.objects.create(
        content=content,
        sender=request.user,
        receiver=parent,
        )
    return redirect("Article", article.pk)



@login_required
@require_http_methods(["POST"])
def comment_add_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    content = request.POST.get('content')
    if content is None:
        return redirect("Article", article.pk)
    Comment.objects.create(
        content=content,
        sender=request.user,
        receiver=article,
        )
    return redirect("Article", article.pk)
