# Internship Management Platform (PFA & Internship Tracking)

A comprehensive Django web application for managing internship requests, offers, and tracking students in their End-of-Year Projects (PFA).

## 🎯 Features

### For Students
- Submit internship applications
- Track application status
- Manage ongoing internships
- Submit weekly reports
- Track PFA progress with Kanban board

### For Companies
- Publish internship offers
- Review applications
- Manage recruited interns
- Communicate with students and teachers

### For Teachers
- Supervise internships
- Validate weekly reports
- Track PFA progress
- Manage defense schedules

### For Administrators
- Full platform management
- User management
- Statistics and reporting
- Export data to CSV/Excel

## 🏗️ Tech Stack

- **Backend**: Django 4.2+ with Django REST Framework
- **Database**: PostgreSQL (SQLite for development)
- **Frontend**: Django Templates + Bootstrap 5 + Vanilla JavaScript
- **Authentication**: Django Allauth (multi-role)
- **File Storage**: Django Storages + Pillow
- **Notifications**: In-app notifications + Email
- **Charts**: Chart.js

## 📋 Installation

### Prerequisites
- Python 3.9+
- PostgreSQL 12+ (or SQLite for development)
- Redis (optional, for Celery)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd plateforme_stage
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
```bash
cp .env.example .env
# Edit .env with your configuration
```

### Step 5: Setup Database
```bash
# For PostgreSQL (recommended)
createdb plateforme_stage_db

# Or use SQLite (development only)
# Set USE_SQLITE=True in .env
```

### Step 6: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 7: Create Superuser
```bash
python manage.py createsuperuser
```

### Step 8: Load Initial Data (Optional)
```bash
python manage.py seed_data
```

### Step 9: Run Development Server
```bash
python manage.py runserver
```

Visit `http://localhost:8000` in your browser.

## 📁 Project Structure

```
plateforme_stage/
├── config/                  # Project configuration
│   ├── settings/
│   │   ├── base.py         # Base settings
│   │   ├── development.py  # Dev settings
│   │   └── production.py   # Prod settings
│   ├── urls.py             # Main URL configuration
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── accounts/           # User profiles & authentication
│   ├── offres/             # Internship offers
│   ├── candidatures/       # Applications
│   ├── stages/             # Ongoing internships
│   ├── pfa/                # End-of-Year Projects
│   ├── dashboard/          # User dashboards
│   ├── notifications/      # Notifications system
│   └── core/               # Shared utilities
├── templates/              # HTML templates
├── static/                 # CSS, JS, images
├── media/                  # Uploaded files
├── requirements.txt
├── .env.example
└── manage.py
```

## 👥 User Roles

1. **Student (ETUDIANT)**: Browse offers, apply, track internships
2. **Company (ENTREPRISE)**: Post offers, review applications
3. **Teacher (ENSEIGNANT)**: Supervise, validate reports
4. **Administrator (ADMIN)**: Full platform access

## 🔐 Authentication

The platform uses Django Allauth for authentication with email-based login.

### Register a New Account
1. Visit `/accounts/signup/`
2. Choose your role (Student, Company, or Teacher)
3. Fill in the required information
4. Verify your email

### Login
Visit `/accounts/login/` with your email and password.

## 📊 Key Features

### Internship Offers Module
- CRUD operations for companies
- Advanced filtering (type, duration, location, skills)
- Full-text search
- Save favorites
- Share offers

### Applications Module
- One-click apply (if profile complete)
- Application limit (configurable, default: 5)
- Status tracking
- Email notifications
- Application history

### Internship Tracking Module
- Visual timeline
- Weekly reports
- Teacher validation
- Automatic PDF generation
- Internal messaging

### PFA Management Module
- Kanban board for tasks
- Gantt chart view
- Document versioning
- Meeting tracking
- Automatic supervisor assignment

## 🔒 Security

- Role-based access control (RBAC)
- CSRF protection on all forms
- File upload validation
- Audit logging
- Secure password hashing

## 📧 Email Configuration

Configure SMTP settings in `.env`:

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-password
```

## 🚀 Deployment

### Production Settings
1. Set `DEBUG=False` in `.env`
2. Configure allowed hosts
3. Use PostgreSQL database
4. Set up Redis for Celery
5. Configure S3 for file storage (optional)
6. Set up SSL/HTTPS

### Using Docker (Optional)
```bash
docker-compose up -d
```

## 🧪 Testing

```bash
python manage.py test
```

## 📝 Admin Interface

Access the admin panel at `/admin/` with superuser credentials.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

For issues and questions, please open an issue on GitHub.

---

**Built with Django ❤️**
