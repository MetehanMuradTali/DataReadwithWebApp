from django.shortcuts import render, get_object_or_404,HttpResponseRedirect,redirect,Http404
from .models import Post
from .forms import PostForm
from django.contrib import messages
# Create your views here.

def post_index(request):
    posts = Post.objects.all()
    return render(request, 'post/index.html', {'posts': posts})


def post_detail(request,id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'post/detail.html', {'post': post})


def post_create(request):
    if not request.user.is_authenticated:
        raise Http404

    form = PostForm(request.POST or None,request.FILES or None)
    if form.is_valid():
       post = form.save(commit=False)
       post.user = request.user
       post.save()

       messages.success(request,'Post başarılı şekilde oluşturuldu')
       return HttpResponseRedirect(post.get_absolute_url())

    context = {
        'form': form,
    }
    return render(request, 'post/form.html', context)

def post_update(request,id):
    if not request.user.is_authenticated:
        raise Http404
    post = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None,instance=post)
    if form.is_valid():
       form.save()
       messages.success(request,'Post başarılı şekilde güncellendi')
       return HttpResponseRedirect(post.get_absolute_url())

    context = {
        'form': form,
    }
    return render(request, 'post/form.html', context)

def post_delete(request,id):
    if not request.user.is_authenticated:
        raise Http404
    post = get_object_or_404(Post, id=id)
    post.delete()
    messages.success(request, 'Post başarılı şekilde silindi',extra_tags='mesaj-basarili')
    return redirect('post:index')


