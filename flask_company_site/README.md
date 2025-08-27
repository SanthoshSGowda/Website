# Flask Company Website (Blog + Admin)

A production-ready Flask starter for a company website with:
- Public pages (Home, About, Services, Blog, Contact)
- Admin dashboard (login/logout)
- Blog CRUD (create, edit, publish/unpublish)
- Services CRUD
- Contact form storing messages
- SQLite + SQLAlchemy + Flask-Migrate
- Flask-Login + password hashing

## Quick Start

```bash
# 1) Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2) Install deps
pip install -r requirements.txt

# 3) Initialize database (creates admin user: admin@example.com / password: admin123)
flask --app app.app db upgrade
python seed.py

# 4) Run dev server
flask --app app.app --debug run
```

## Default Admin
- Email: `admin@example.com`
- Password: `admin123` (change after first login)

## Environment
- By default, SQLite DB is stored at `instance/site.db`
- To change configs, edit `app/config.py`
