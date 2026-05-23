# Creatiff

## Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [For Frontend Developers](#for-frontend-developers)
- [Docker Commands](#docker-commands)

## Prerequisites

- **Docker** 20.10 or higher
- **Docker Compose** 1.29 or higher
- **Git** for version control

### Installing Docker

#### On Windows:
1. Download **Docker Desktop** from the official website: https://www.docker.com/products/docker-desktop
2. Run the installer and follow the instructions
3. Restart your computer after installation
4. Verify the installation:
   ```powershell
   docker --version
   docker-compose --version
   ```

#### On macOS:
1. Download **Docker Desktop** for Mac: https://www.docker.com/products/docker-desktop
2. Run the installer
3. Verify the installation:
   ```bash
   docker --version
   docker-compose --version
   ```

#### On Linux:
Install Docker and Docker Compose using your distribution's package manager.

## Quick Start

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd creatiff
```

### Step 2: Create the .env File

1. In the project root directory, find the `.env.example` file, copy it and rename to `.env` file
2. Copy the env variables from direct messages into the `.env` file.

### Step 3: Run the Project with Docker Compose

Execute the command in the project root directory:

```bash
docker-compose up -d
```

This command will:
- Build Docker images (if necessary)
- Start the Django application container
- Start the PostgreSQL database container
- Run them in the background (`-d` flag)
- Automatically complete migrations, fill the database and create a superuser

### Step 6: Verify the Application

Open your browser and navigate to:
- **Homepage:** http://localhost:8000
- **Admin Panel:** http://localhost:8000/admin
- **Wagtail CMS:** http://localhost:8000/cms

Your project is running and ready to work! 🎉

## Project Structure

```
creatiff/
├── creatiff/                          # Django project configuration
│   ├── settings.py                    # Main Django settings
│   ├── urls.py                        # Main URL routing
│   ├── wsgi.py                        # WSGI configuration
│   └── asgi.py                        # ASGI configuration
│
├── main/                              # Main application
│   ├── models.py                      # Database models
│   ├── views.py                       # View logic
│   ├── forms.py                       # Django forms
│   ├── urls.py                        # App URL patterns
│   ├── admin.py                       # Admin panel settings
│   │
│   ├── templates/                     # HTML templates (frontend)
│   │   └── main/
│   │       ├── base.html              # Base template
│   │       ├── homepage.html          # Homepage
│   │       └── components/
│   │           ├── header.html        # Header component
│   │           ├── footer.html        # Footer component
│   │           └── contact_form.html  # Contact form
│   │
│   ├── static/                        # Static files (CSS, JS, images)
│   │   └── main/
│   │       ├── base.css               # Base styles
│   │       ├── homepage.css           # Homepage styles
│   │       └── components/
│   │           ├── header.css         # Header styles
│   │           ├── footer.css         # Footer styles
│   │           └── contact_form.css   # Form styles
│   │
│   ├── management/
│   │   └── commands/
│   │       └── seed.py                # Database seeding command
│   │
│   └── migrations/                    # Database migrations
│
├── media/                             # User-uploaded files
│   └── header_logo/                   # Header logo
│
├── manage.py                          # Django management script
├── requirements.txt                   # Python dependencies
├── Dockerfile                         # Docker image configuration
├── docker-compose.yml                 # Docker Compose configuration
├── entrypoint.sh                      # Container startup script
├── .env                               # Environment variables (create manually)
├── .gitignore                         # Git ignore file
└── README.md                          # This file
```

## For Frontend Developers

### Where is the Frontend Code?

All frontend code is located in:
```
main/templates/    - HTML files
main/static/       - CSS and JavaScript files
```

### What Should Frontend Developers Change?

#### 1. **HTML Templates** (`main/templates/main/`)

This is where all HTML files are located:
- **base.html** - base template (overall structure)
- **homepage.html** - homepage
- **components/** - individual components (header, footer, forms)

Make all HTML changes in these files.

#### 2. **Styles** (`main/static/main/`)

CSS files are organized by component:
- **base.css** - global styles
- **homepage.css** - homepage styles
- **components/header.css** - header styles
- **components/footer.css** - footer styles
- **components/contact_form.css** - form styles

#### 3. **JavaScript** (if to be added)

To add JavaScript, create files in:
```
main/static/main/js/
```

#### 4. **Media Files** (`media/`)

User-uploaded files (logos, images) are stored in:
```
media/header_logo/  - logos
media/              - other files
```

### How to Preview Changes?

1. Edit the desired HTML or CSS file
2. Save your changes
3. Refresh the page in your browser
4. Changes should appear immediately

## Docker Commands

### Basic Commands

**Start the application:**
```bash
docker-compose up
```

**Start in background mode:**
```bash
docker-compose up -d
```

**Stop the application:**
```bash
docker-compose down
```

**View logs:**
```bash
docker-compose logs -f
```

**View logs for a specific service:**
```bash
docker-compose logs -f web
docker-compose logs -f db
```

### Useful Django Commands

**Create migrations after model changes:**
```bash
docker-compose exec web python manage.py makemigrations
```

**Apply migrations:**
```bash
docker-compose exec web python manage.py migrate
```

### Rebuilding Containers

To rebuild the images (e.g., after changing requirements.txt):
```bash
docker-compose up -d --build
```

### If you need to clean everything and start from scratch
```bash
docker-compose down -v
docker system prune -a
docker-compose up -d --build
```
