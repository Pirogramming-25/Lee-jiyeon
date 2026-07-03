from django.shortcuts import render, get_object_or_404, redirect
from .models import Idea, DevTool, IdeaStar
from .forms import IdeaForm, DevToolForm
from django.db.models import Count

def idea_list(request):
    sort = request.GET.get('sort', '-created_at')
    if sort == 'stars':
        ideas = Idea.objects.annotate(star_count=Count('stars')).order_by('-star_count')
    else:
        ideas = Idea.objects.all().order_by(sort)
    return render(request, 'idea/idea_list.html', {'ideas': ideas})

def idea_detail(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    return render(request, 'idea/idea_detail.html', {'idea': idea})

def idea_create(request):
    if request.method == 'POST':
        form = IdeaForm(request.POST, request.FILES)
        if form.is_valid():
            idea = form.save()
            return redirect('idea_detail', pk=idea.pk)   
    else:
        form = IdeaForm()
    return render(request, 'idea/idea_form.html', {'form': form})

def idea_update(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    if request.method == 'POST':
        form = IdeaForm(request.POST, request.FILES, instance=idea)   
        if form.is_valid():
            form.save()
            return redirect('idea_detail', pk=idea.pk)   
    else:
        form = IdeaForm(instance=idea)     
    return render(request, 'idea/idea_form.html', {'form': form})

def idea_delete(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    idea.delete()
    return redirect('idea_list')    

def idea_star(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    star = IdeaStar.objects.filter(idea=idea).first()   
    if star:
        star.delete()          
    else:
        IdeaStar.objects.create(idea=idea)   
    return redirect(request.META.get('HTTP_REFERER', 'idea_list'))

def idea_interest(request, pk, action):
    idea = get_object_or_404(Idea, pk=pk)
    if action == 'up':
        idea.interest += 1
    elif action == 'down':
        idea.interest -= 1
    idea.save()
    return redirect(request.META.get('HTTP_REFERER', 'idea_list'))

# 개발툴 리스트
def devtool_list(request):
    devtools = DevTool.objects.all()
    return render(request, 'idea/devtool_list.html', {'devtools': devtools})

# 개발툴 디테일
def devtool_detail(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    return render(request, 'idea/devtool_detail.html', {'devtool': devtool})

# 개발툴 등록
def devtool_create(request):
    if request.method == 'POST':
        form = DevToolForm(request.POST)
        if form.is_valid():
            devtool = form.save()
            return redirect('devtool_detail', pk=devtool.pk)   
    else:
        form = DevToolForm()
    return render(request, 'idea/devtool_form.html', {'form': form})

# 개발툴 수정
def devtool_update(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    if request.method == 'POST':
        form = DevToolForm(request.POST, instance=devtool)
        if form.is_valid():
            form.save()
            return redirect('devtool_detail', pk=devtool.pk)
    else:
        form = DevToolForm(instance=devtool)
    return render(request, 'idea/devtool_form.html', {'form': form})

# 개발툴 삭제
def devtool_delete(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    devtool.delete()
    return redirect('devtool_list')