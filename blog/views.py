from django.shortcuts import get_object_or_404, render

from .models import Post


def home(request):
    posts = Post.objects.filter(publicado=True)
    return render(request, "blog/home.html", {"posts": posts})


def detalhe_post(request, pk):
    post = get_object_or_404(Post, pk=pk, publicado=True)
    return render(request, "blog/detalhe.html", {"post": post})
