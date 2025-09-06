from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from members.models import Member, Task
import random

class Command(BaseCommand):
    help = 'Create sample data for the Team Tracker application'

    def handle(self, *args, **options):
        # Clear existing data
        Task.objects.all().delete()
        Member.objects.all().delete()

        # Sample members data
        members_data = [
            {'name': 'Alice Johnson', 'reg_number': 'REG001', 'email': 'alice.johnson@example.com'},
            {'name': 'Bob Smith', 'reg_number': 'REG002', 'email': 'bob.smith@example.com'},
            {'name': 'Charlie Brown', 'reg_number': 'REG003', 'email': 'charlie.brown@example.com'},
            {'name': 'Diana Ross', 'reg_number': 'REG004', 'email': 'diana.ross@example.com'},
            {'name': 'Edward Wilson', 'reg_number': 'REG005', 'email': 'edward.wilson@example.com'},
            {'name': 'Fiona Davis', 'reg_number': 'REG006', 'email': 'fiona.davis@example.com'},
            {'name': 'George Miller', 'reg_number': 'REG007', 'email': 'george.miller@example.com'},
            {'name': 'Hannah Lee', 'reg_number': 'REG008', 'email': 'hannah.lee@example.com'},
        ]

        # Create members
        members = []
        for member_data in members_data:
            member = Member.objects.create(**member_data)
            members.append(member)
            self.stdout.write(f'Created member: {member.name}')

        # Sample tasks data
        task_titles = [
            'Complete project documentation',
            'Review code implementation',
            'Prepare presentation slides',
            'Conduct user testing',
            'Write unit tests',
            'Design database schema',
            'Implement authentication',
            'Create API endpoints',
            'Update user interface',
            'Optimize performance',
            'Fix reported bugs',
            'Research new technologies',
            'Setup development environment',
            'Deploy to staging',
            'Create user manual',
            'Analyze requirements',
            'Design system architecture',
            'Implement data validation',
            'Create backup strategy',
            'Monitor system metrics',
        ]

        task_descriptions = [
            'This task involves creating comprehensive documentation for the project.',
            'Review the codebase and provide feedback on implementation quality.',
            'Prepare slides for the upcoming team presentation.',
            'Conduct thorough testing with end users to gather feedback.',
            'Write comprehensive unit tests to ensure code quality.',
            'Design an efficient and scalable database schema.',
            'Implement secure user authentication and authorization.',
            'Create RESTful API endpoints for the application.',
            'Update the user interface to improve user experience.',
            'Optimize application performance and reduce load times.',
            'Investigate and fix bugs reported by users.',
            'Research emerging technologies that could benefit the project.',
            'Setup a consistent development environment for the team.',
            'Deploy the application to the staging environment.',
            'Create detailed user documentation and guides.',
            'Analyze project requirements and create specifications.',
            'Design the overall system architecture and components.',
            'Implement robust data validation and error handling.',
            'Create a comprehensive backup and recovery strategy.',
            'Setup monitoring to track system performance and health.',
        ]

        # Create tasks for each member
        for member in members:
            num_tasks = random.randint(3, 8)
            member_tasks = random.sample(list(zip(task_titles, task_descriptions)), num_tasks)
            
            for i, (title, description) in enumerate(member_tasks):
                # Random completion status (70% chance of completion)
                is_completed = random.random() < 0.7
                
                # Random credits between 10 and 100
                credits = random.randint(1, 10) * 10
                
                # Random due date (within next 30 days)
                due_date = timezone.now() + timedelta(days=random.randint(1, 30))
                
                # Random creation date (within last 60 days)
                created_days_ago = random.randint(1, 60)
                created_at = timezone.now() - timedelta(days=created_days_ago)
                
                task = Task.objects.create(
                    member=member,
                    title=f"{title} - {member.name}",
                    description=description,
                    credits=credits,
                    is_completed=is_completed,
                    due_date=due_date,
                )
                
                # Update created_at to simulate historical data
                task.created_at = created_at
                task.save()
                
                status = "✅" if is_completed else "⏳"
                self.stdout.write(f'  {status} Created task: {task.title} ({credits} credits)')

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully created {len(members)} members and {Task.objects.count()} tasks!'
            )
        )
