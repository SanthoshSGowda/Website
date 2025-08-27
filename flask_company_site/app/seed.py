from .app import app, db, User, Post, Service
from sqlalchemy.exc import IntegrityError

with app.app_context():
    # Create admin user if not exists
    if not User.query.filter_by(email="admin@example.com").first():
        u = User(email="admin@example.com", name="Admin")
        u.set_password("admin123")
        db.session.add(u)
        db.session.commit()
        print("Created default admin: admin@example.com / admin123")
    else:
        print("Admin user already exists.")

    # Sample content
    if Service.query.count() == 0:
        db.session.add_all([
            Service(name="Web Development", description="Full‑stack web applications using Flask.", price_inr=75000),
            Service(name="DevOps Setup", description="CI/CD, Docker, Kubernetes pipelines.", price_inr=95000),
            Service(name="Consulting", description="Architecture, code reviews, training.", price_inr=50000),
        ])
        db.session.commit()
        print("Seeded Services.")

    if Post.query.count() == 0:
        db.session.add_all([
            Post(title="Welcome to Our Company", slug="welcome-to-our-company", body="We build reliable software.", published=True),
            Post(title="How We Work", slug="how-we-work", body="Process, transparency, and results.", published=True),
        ])
        db.session.commit()
        print("Seeded Posts.")
