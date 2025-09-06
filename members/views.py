from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, Count, Q
from .models import Member, Task

def member_list(request):
    """Display list of all members with their stats"""
    members = Member.objects.annotate(
        total_credits=Sum('tasks__credits', filter=Q(tasks__is_completed=True)),
        total_tasks=Count('tasks'),
        completed_tasks=Count('tasks', filter=Q(tasks__is_completed=True))
    ).order_by('-total_credits')
    
    context = {
        'members': members,
        'total_members': members.count(),
        'top_performer': members.first() if members else None,
    }
    return render(request, "members/member_list.html", context)

def member_detail(request, reg_number):
    """Display detailed view of a specific member"""
    member = get_object_or_404(Member, reg_number=reg_number)
    tasks = member.tasks.all()
    completed_tasks = tasks.filter(is_completed=True)
    pending_tasks = tasks.filter(is_completed=False)
    
    total_credits = sum(task.credits for task in completed_tasks)
    
    context = {
        'member': member,
        'tasks': tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'total_credits': total_credits,
        'completion_rate': (completed_tasks.count() / tasks.count() * 100) if tasks.count() > 0 else 0,
    }
    return render(request, "members/member_detail.html", context)

def leaderboard(request):
    """Display leaderboard of members ranked by credits"""
    members = Member.objects.annotate(
        total_credits=Sum('tasks__credits', filter=Q(tasks__is_completed=True)),
        total_tasks=Count('tasks'),
        completed_tasks=Count('tasks', filter=Q(tasks__is_completed=True))
    ).order_by('-total_credits')
    
    # Get top 3 performers
    top_members = list(members[:3])
    first_place = top_members[0] if len(top_members) > 0 else None
    second_place = top_members[1] if len(top_members) > 1 else None
    third_place = top_members[2] if len(top_members) > 2 else None
    
    context = {
        'members': members,
        'first_place': first_place,
        'second_place': second_place,
        'third_place': third_place,
        'page_title': 'Leaderboard'
    }
    return render(request, "members/leaderboard.html", context)

def dashboard(request):
    """Display main dashboard with overview stats"""
    total_members = Member.objects.count()
    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(is_completed=True).count()
    total_credits = Task.objects.filter(is_completed=True).aggregate(
        total=Sum('credits')
    )['total'] or 0
    
    recent_members = Member.objects.order_by('-created_at')[:5]
    recent_tasks = Task.objects.order_by('-created_at')[:10]
    
    top_performers = Member.objects.annotate(
        total_credits=Sum('tasks__credits', filter=Q(tasks__is_completed=True))
    ).order_by('-total_credits')[:5]
    
    context = {
        'total_members': total_members,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'total_credits': total_credits,
        'completion_rate': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
        'recent_members': recent_members,
        'recent_tasks': recent_tasks,
        'top_performers': top_performers,
    }
    return render(request, "members/dashboard.html", context)
