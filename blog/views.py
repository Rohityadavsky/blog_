from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import get_object_or_404, redirect
from .models import  Comment,Blog
from .forms import CommentForm
from django.core.mail import send_mail

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blog_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def add_comment(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.user = request.user
            comment.save()
            return redirect('blog_detail', pk=blog.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment.html', {'form': form})

def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    return redirect('blog_detail', pk=comment.blog.pk)


def share_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        email = request.POST['email']
        send_mail(
            f"Check out this blog: {blog.title}",
            f"Read it here: {request.build_absolute_uri(blog.get_absolute_url())}",
            'from@example.com',
            [email],
            fail_silently=False,
        )
        return redirect('blog_list')
    return render(request, 'blog/share_blog.html', {'blog': blog})
