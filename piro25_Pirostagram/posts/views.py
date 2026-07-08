from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm
from django.http import JsonResponse
from .models import Post, Comment
from .models import Post, Comment, Story
from django.contrib.auth.models import User
from django.db.models import Q

def post_list(request):
    if request.user.is_authenticated:
        # 내가 팔로우한 사람들 + 나
        following_users = request.user.profile.following.all()
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        stories = Story.objects.filter(author__in=following_users).order_by('-created_at')
        # 추천 유저 (내가 팔로우 안 한 사람들)
        suggested = User.objects.exclude(id=request.user.id).exclude(id__in=following_users)
    else:
        posts = Post.objects.all().order_by('-created_at')
        stories = Story.objects.none()
        suggested = User.objects.none()
    return render(request, 'posts/post_list.html', {
        'posts': posts, 'stories': stories, 'suggested': suggested,
    })

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user      
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'posts/post_form.html', {'form': form})

@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:         
        return redirect('post_list')
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/post_form.html', {'form': form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author == request.user:       
        post.delete()
    return redirect('post_list')

@login_required
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user

    if user in post.likes.all():
        post.likes.remove(user)     
        liked = False
    else:
        post.likes.add(user)        
        liked = True

    return JsonResponse({
        'liked': liked,                     
        'like_count': post.likes.count(),  
    })

@login_required
def comment_create(request, pk):
    post = get_object_or_404(Post, pk=pk)
    content = request.POST.get('content')
    if content:
        comment = Comment.objects.create(
            post=post,
            author=request.user,
            content=content,
        )
        return JsonResponse({
            'comment_id': comment.id,
            'author': comment.author.username,
            'content': comment.content,
            'comment_count': post.comments.count(),
        })
    return JsonResponse({'error': '내용 없음'}, status=400)

@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author == request.user:   
        post = comment.post
        comment.delete()
        return JsonResponse({'comment_count': post.comments.count()})
    return JsonResponse({'error': '권한 없음'}, status=403)


@login_required
def story_create(request):
    if request.method == 'POST':
        images = request.FILES.getlist('images')   
        for img in images:
            Story.objects.create(author=request.user, image=img)
        return redirect('post_list')
    return render(request, 'posts/story_form.html')


@login_required
def follow_toggle(request, user_id):
    target = get_object_or_404(User, id=user_id)
    my_profile = request.user.profile

    if target in my_profile.following.all():
        my_profile.following.remove(target)   
        following = False
    else:
        my_profile.following.add(target)     
        following = True

    return JsonResponse({'following': following})

def profile(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)
    posts = Post.objects.filter(author=profile_user).order_by('-created_at')

    is_following = False
    if request.user.is_authenticated:
        is_following = profile_user in request.user.profile.following.all()

    follower_count = profile_user.followers.count()   
    following_count = profile_user.profile.following.count()

    return render(request, 'posts/profile.html', {
        'profile_user': profile_user,
        'posts': posts,
        'is_following': is_following,
        'follower_count': follower_count,
        'following_count': following_count,
    })


def user_search(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = User.objects.filter(
            Q(username__icontains=query) | Q(first_name__icontains=query)
        )
    return render(request, 'posts/user_search.html', {
        'query': query,
        'results': results,
    })