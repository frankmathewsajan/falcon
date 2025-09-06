
# Team Tracker - Falcon (Django App)

A Django application to **track people under you**, with their **registration details, tasks assigned, and credits earned**.

---

## 🚀 Features

* Add **Members** with:

  * Name
  * Registration Number
  * Email
* Assign **Tasks** to members:

  * Title, Description
  * Credits
  * Completion status
* Track **total credits** earned per member
* Simple **Django Admin dashboard** for managing members and tasks
* Web pages to:

  * List all members
  * View details of a member with their tasks & credits

---

## 🛠️ Setup Instructions

1. **Create Django Project & App**

   ```bash
   django-admin startproject falcon
   cd falcon
   python manage.py startapp members
   ```

2. **Add app to settings**
   In `falcon/settings.py`:

   ```python
   INSTALLED_APPS = [
       ...
       "members",
   ]
   ```

---

## 📦 Models

In `members/models.py`:

```python
from django.db import models

class Member(models.Model):
    name = models.CharField(max_length=100)
    reg_number = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.name} ({self.reg_number})"


class Task(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    credits = models.PositiveIntegerField(default=0)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} -> {self.member.name}"
```

Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## ⚙️ Admin Setup

In `members/admin.py`:

```python
from django.contrib import admin
from .models import Member, Task

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("name", "reg_number", "email")

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "member", "credits", "is_completed")
    list_filter = ("is_completed",)
```

---

## 📖 Views

In `members/views.py`:

```python
from django.shortcuts import render, get_object_or_404
from .models import Member

def member_list(request):
    members = Member.objects.all()
    return render(request, "members/member_list.html", {"members": members})

def member_detail(request, reg_number):
    member = get_object_or_404(Member, reg_number=reg_number)
    total_credits = sum(task.credits for task in member.tasks.filter(is_completed=True))
    return render(request, "members/member_detail.html", {
        "member": member,
        "total_credits": total_credits,
    })
```

---

## 🌐 URLs

In `members/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.member_list, name="member_list"),
    path("<str:reg_number>/", views.member_detail, name="member_detail"),
]
```

In `falcon/urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    path("members/", include("members.urls")),
]
```

---

## 🖼️ Templates

**`templates/members/member_list.html`**

```html
<h1>Team Members</h1>
<ul>
  {% for member in members %}
    <li>
      <a href="{% url 'member_detail' member.reg_number %}">
        {{ member.name }} ({{ member.reg_number }})
      </a>
    </li>
  {% endfor %}
</ul>
```

**`templates/members/member_detail.html`**

```html
<h2>{{ member.name }} ({{ member.reg_number }})</h2>
<p>Email: {{ member.email }}</p>

<h3>Tasks</h3>
<ul>
  {% for task in member.tasks.all %}
    <li>
      {{ task.title }} - {{ task.credits }} credits 
      {% if task.is_completed %}✅{% else %}❌{% endif %}
    </li>
  {% endfor %}
</ul>

<p><b>Total Credits:</b> {{ total_credits }}</p>
```

---

## 🎯 Next Steps / Bonus Features

* Add **authentication** → each member logs in to view their tasks
* Add **task assignment forms** in frontend
* Create a **leaderboard** ranking members by credits
* Export reports (CSV/Excel)
* Use the templates thing defult with djgo with tailwind for beutiful mobile first dash baords and UI,



