from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from school.models import  Comment
from .models import Article
import random
from utils.s3 import upload_fileobj_to_s3, public_url

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
            title = request.POST.get('title')
            content = request.POST.get('content')
            f = request.FILES.get("image")

            image_url = None
            if f:
                try:
                    f.open()
                except Exception:
                    pass

                try:
                    f.seek(0)
                except Exception:
                    pass

                # توليد اسم عشوائي للملف
                key = f"media/courses/{random.randint(1,1000)}-{random.randint(1,1000)}-{f.name}"
                
                # رفع الملف على S3
                upload_fileobj_to_s3(f, key, content_type=f.content_type)

                # الحصول على الرابط العمومي
                image_url = public_url(key)

            # إنشاء المقال وربط الصورة كرابط
            a = Article.objects.create(
                title=title,
                content=content,
                image=image_url,   # لاحظ هنا نمرر الرابط بدل ملف
                student=request.user
            )

            return redirect('Article', a.pk)
        except Exception as e:
            print(e)
            return render(request, 'article_form.html', {'article': None})

    return render(request, 'article_form.html', {'article': None})




@login_required
def article_update(request, article_id):
    article = get_object_or_404(Article, pk=article_id, student=request.user)

    if request.method == 'POST':
        # حدّث الحقول النصية
        article.title = request.POST.get('title') or article.title
        article.content = request.POST.get('content') or article.content

        # إن وُجد ملف جديد ارفعه إلى S3 واحفظ رابطَه
        f = request.FILES.get('image')
        if f:
            try:
                f.open()
            except Exception:
                pass
            try:
                f.seek(0)
            except Exception:
                pass

            key = f"media/courses/{random.randint(1,1000)}-{random.randint(1,1000)}-{f.name}"
            upload_fileobj_to_s3(f, key, content_type=getattr(f, "content_type", None))
            article.image = public_url(key)   # نخزن URL الناتج #type:ignore

        article.save()
        return redirect('Article', article.pk)

    return render(request, 'article_form.html', {'article': article})




# @login_required
# def article_create(request):
#     if request.method == 'POST':
#         try:
#             a = Article.objects.create(
#                 title=request.POST['title'],
#                 content=request.POST['content'],
#                 image=request.FILES.get('image'),
#                 student=request.user
#             )
#             return redirect('Article', a.pk)
#         except:
#             return render(request, 'article_form.html', {'article': None})
        
#     return render(request, 'article_form.html', {'article': None})


# @login_required
# def article_update(request, article_id):
#     article = get_object_or_404(Article, pk=article_id, student=request.user)
#     if request.method == 'POST':
#         article.title = request.POST.get('title') or article.title
#         article.content = request.POST.get('content') or article.content
#         if request.FILES.get('image'):
#             article.image = request.FILES['image']
#         article.save()
#         return redirect('Article', article.pk)
#     return render(request, 'article_form.html', {'article': article})


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
