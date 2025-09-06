from django.db import models

class Member(models.Model):
    name = models.CharField(max_length=100)
    reg_number = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.reg_number})"

    def total_credits(self):
        return sum(task.credits for task in self.tasks.filter(is_completed=True))

    def total_tasks(self):
        return self.tasks.count()

    def completed_tasks(self):
        return self.tasks.filter(is_completed=True).count()

    class Meta:
        ordering = ['name']


class Task(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    credits = models.PositiveIntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} -> {self.member.name}"

    class Meta:
        ordering = ['-created_at']
