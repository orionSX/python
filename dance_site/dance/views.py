from django.shortcuts import render, get_object_or_404, redirect
from .models import DanceGroup, DanceStyle, Dancer, Performance

# Главная страница с кратким списком танцоров
def index(request):
    dancers = Dancer.objects.select_related('group').all()
    return render(request, 'dance/index.html', {'dancers': dancers})

# CRUD для Dancer
def add_or_edit_dancer(request, id=None):
    dancer = None if id is None else get_object_or_404(Dancer, id=id)
    groups = DanceGroup.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        age = request.POST['age']
        group_id = request.POST['group_id']
        group = get_object_or_404(DanceGroup, id=group_id)
        if dancer:
            dancer.name = name
            dancer.age = age
            dancer.group = group
            dancer.save()
        else:
            Dancer.objects.create(name=name, age=age, group=group)
        return redirect('index')
    return render(request, 'dance/edit_dancer.html', {'dancer': dancer, 'groups': groups})

def delete_dancer(request, id):
    dancer = get_object_or_404(Dancer, id=id)
    dancer.delete()
    return redirect('index')

def dancer_detail(request, id):
    dancer = get_object_or_404(Dancer, id=id)
    return render(request, 'dance/detail.html', {'dancer': dancer})

# CRUD для DanceGroup
def list_groups(request):
    groups = DanceGroup.objects.all()
    return render(request, 'dance/groups.html', {'groups': groups})

def add_or_edit_group(request, id=None):
    group = None if id is None else get_object_or_404(DanceGroup, id=id)
    if request.method == "POST":
        name = request.POST['name']
        city = request.POST['city']
        if group:
            group.name = name
            group.city = city
            group.save()
        else:
            DanceGroup.objects.create(name=name, city=city)
        return redirect('list_groups')
    return render(request, 'dance/edit_group.html', {'group': group})

def delete_group(request, id):
    group = get_object_or_404(DanceGroup, id=id)
    group.delete()
    return redirect('list_groups')

# CRUD для DanceStyle
def list_styles(request):
    styles = DanceStyle.objects.all()
    return render(request, 'dance/styles.html', {'styles': styles})

def add_or_edit_style(request, id=None):
    style = None if id is None else get_object_or_404(DanceStyle, id=id)
    if request.method == "POST":
        name = request.POST['name']
        if style:
            style.name = name
            style.save()
        else:
            DanceStyle.objects.create(name=name)
        return redirect('list_styles')
    return render(request, 'dance/edit_style.html', {'style': style})

def delete_style(request, id):
    style = get_object_or_404(DanceStyle, id=id)
    style.delete()
    return redirect('list_styles')

# CRUD для Performance
def list_performances(request):
    performances = Performance.objects.select_related('group', 'style').all()
    return render(request, 'dance/performances.html', {'performances': performances})

def add_or_edit_performance(request, id=None):
    performance = None if id is None else get_object_or_404(Performance, id=id)
    groups = DanceGroup.objects.all()
    styles = DanceStyle.objects.all()
    if request.method == "POST":
        group_id = request.POST['group_id']
        style_id = request.POST['style_id']
        date = request.POST['date']
        location = request.POST['location']
        group = get_object_or_404(DanceGroup, id=group_id)
        style = get_object_or_404(DanceStyle, id=style_id)
        if performance:
            performance.group = group
            performance.style = style
            performance.date = date
            performance.location = location
            performance.save()
        else:
            Performance.objects.create(group=group, style=style, date=date, location=location)
        return redirect('list_performances')
    return render(request, 'dance/edit_performance.html', {'performance': performance, 'groups': groups, 'styles': styles})

def delete_performance(request, id):
    performance = get_object_or_404(Performance, id=id)
    performance.delete()
    return redirect('list_performances')
