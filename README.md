# 🦅 Team Tracker - Falcon

A beautiful and modern Django application to **track team members, assign tasks, and monitor credits earned**. Built with Django and styled with Tailwind CSS for a mobile-first, responsive experience.

![Team Tracker Dashboard](https://img.shields.io/badge/Django-5.2.6-green?style=for-the-badge&logo=django)
![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-CSS-blue?style=for-the-badge&logo=tailwindcss)

## ✨ Features

### 🏠 **Beautiful Dashboard**
- **Real-time statistics** with animated counters
- **Progress tracking** with visual progress bars
- **Top performers** leaderboard
- **Recent activity** timeline
- **Quick actions** for common tasks

### 👥 **Member Management**
- **Member profiles** with detailed information
- **Registration tracking** with unique numbers
- **Email management** and contact information
- **Performance metrics** per member
- **Task assignment** and progress monitoring

### 📋 **Task System**
- **Task creation** with descriptions and due dates
- **Credit assignment** for completed tasks
- **Status tracking** (pending/completed)
- **Progress visualization** with completion rates
- **Historical task data** and analytics

### 🏆 **Leaderboard & Analytics**
- **Ranking system** based on credits earned
- **Visual podium** for top 3 performers
- **Performance statistics** and success rates
- **Interactive charts** and progress indicators
- **Achievement tracking** and milestones

### 🎨 **Modern UI/UX**
- **Mobile-first responsive design**
- **Tailwind CSS** for beautiful styling
- **Font Awesome icons** for visual clarity
- **Smooth animations** and transitions
- **Interactive hover effects**
- **Dark/light mode ready**

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Django 5.2+
- Modern web browser

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd falcon
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install django
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Load sample data (optional)**
   ```bash
   python manage.py create_sample_data
   ```

7. **Start development server**
   ```bash
   python manage.py runserver
   ```

8. **Visit the application**
   - Main app: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## 📱 Screenshots & Pages

### 🏠 Dashboard
- **Overview statistics** with member count, task completion, and credits
- **Progress tracking** with visual completion rates
- **Top performers** showcase
- **Recent activity** feed
- **Quick action buttons**

### 👥 Members List
- **Grid layout** with member cards
- **Individual statistics** per member
- **Progress bars** showing completion rates
- **Quick actions** (view details, edit)
- **Search and filtering** capabilities

### 👤 Member Details
- **Comprehensive profile** with all member information
- **Task breakdown** (completed vs pending)
- **Credit tracking** and achievement history
- **Performance metrics** and success rates
- **Task management** tools

### 🏆 Leaderboard
- **Visual podium** for top 3 performers
- **Complete rankings** table
- **Performance statistics** comparison
- **Success rate indicators**
- **Achievement badges**

## 🛠️ Technical Stack

### Backend
- **Django 5.2.6** - Web framework
- **SQLite** - Database (easily changeable)
- **Django Admin** - Management interface

### Frontend
- **Tailwind CSS** - Utility-first CSS framework
- **Font Awesome** - Icon library
- **Vanilla JavaScript** - Interactions and animations
- **Responsive Design** - Mobile-first approach

### Features
- **Model-based architecture** with optimized queries
- **Admin customization** with enhanced interfaces
- **Template inheritance** for consistent design
- **Static file management** for assets
- **Management commands** for data operations

## 📊 Database Schema

### Member Model
```python
class Member(models.Model):
    name = models.CharField(max_length=100)
    reg_number = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Task Model
```python
class Task(models.Model):
    member = models.ForeignKey(Member, related_name="tasks")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    credits = models.PositiveIntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(null=True, blank=True)
```

## 🎯 Management Commands

### Create Sample Data
```bash
python manage.py create_sample_data
```
This command creates:
- 8 sample members with realistic data
- 30+ sample tasks with varying completion status
- Random credits and due dates
- Historical creation dates

## 🔧 Customization

### Adding New Features
1. **Extend models** in `members/models.py`
2. **Create migrations** with `python manage.py makemigrations`
3. **Update admin** in `members/admin.py`
4. **Add views** in `members/views.py`
5. **Create templates** in `templates/members/`
6. **Update URLs** in `members/urls.py`

### Styling Customization
1. **Modify Tailwind classes** in templates
2. **Add custom CSS** in `static/css/custom.css`
3. **Update color scheme** in base template
4. **Customize animations** and transitions

## 📈 Future Enhancements

### Planned Features
- **User authentication** for member login
- **Task assignment forms** in frontend
- **Email notifications** for due tasks
- **Export functionality** (CSV/PDF reports)
- **Advanced analytics** and charts
- **Mobile app** integration
- **API endpoints** for external systems
- **Team collaboration** features

### Performance Optimizations
- **Database optimization** with proper indexing
- **Caching implementation** for frequent queries
- **CDN integration** for static files
- **Progressive Web App** features

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Developer

Built with ❤️ using Django and Tailwind CSS for a beautiful, modern team management experience.

---

**Team Tracker - Falcon** - Empowering teams with beautiful task management and performance tracking.
