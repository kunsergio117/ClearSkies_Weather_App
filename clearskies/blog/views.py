
from django.shortcuts import render
from .models import Post

# Blog app view function to filter posts by the input city
def index(request, location=None):
    if location:
        posts = Post.objects.filter(location__iexact=location)
    else:
        posts = Post.objects.all()

    # Additional context data if needed
    context = {
        'posts': posts,
        'searched_location': location
    }
    return render(request, 'main/index.html', context)
