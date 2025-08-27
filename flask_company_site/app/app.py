from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from .config import Config
from .models import db, User, Post, Service, ContactMessage
from .forms import LoginForm, PostForm, ServiceForm, ContactForm

def create_app():
    app = Flask(__name__, instance_relative_config=True, template_folder="templates", static_folder="static")
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)

    login_manager = LoginManager(app)
    login_manager.login_view = "admin_login"
    login_manager.login_message_category = "warning"

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # ------- Public Routes -------
    @app.route("/")
    def index():
        posts = Post.query.filter_by(published=True).order_by(Post.created_at.desc()).limit(3).all()
        services = Service.query.order_by(Service.created_at.desc()).limit(6).all()
        return render_template("index.html", posts=posts, services=services)

    @app.route("/about")
    def about():
        return render_template("about.html")

    @app.route("/services")
    def services():
        services = Service.query.order_by(Service.created_at.desc()).all()
        return render_template("services.html", services=services)

    @app.route("/blog")
    def blog_list():
        page = request.args.get("page", 1, type=int)
        pagination = Post.query.filter_by(published=True).order_by(Post.created_at.desc()).paginate(page=page, per_page=5)
        return render_template("blog_list.html", pagination=pagination, posts=pagination.items)

    @app.route("/blog/<slug>")
    def blog_detail(slug):
        post = Post.query.filter_by(slug=slug, published=True).first_or_404()
        return render_template("blog_detail.html", post=post)

    @app.route("/contact", methods=["GET", "POST"])
    def contact():
        form = ContactForm()
        if form.validate_on_submit():
            msg = ContactMessage(
                name=form.name.data,
                email=form.email.data,
                subject=form.subject.data,
                message=form.message.data
            )
            db.session.add(msg)
            db.session.commit()
            flash("Thanks! We'll get back to you soon.", "success")
            return redirect(url_for("contact"))
        return render_template("contact.html", form=form)

    # ------- Admin Routes -------
    @app.route("/admin/login", methods=["GET", "POST"])
    def admin_login():
        if current_user.is_authenticated:
            return redirect(url_for("admin_dashboard"))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data.lower()).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash("Welcome back!", "success")
                return redirect(url_for("admin_dashboard"))
            flash("Invalid credentials", "danger")
        return render_template("admin/login.html", form=form)

    @app.route("/admin/logout")
    @login_required
    def admin_logout():
        logout_user()
        flash("Logged out.", "info")
        return redirect(url_for("admin_login"))

    @app.route("/admin")
    @login_required
    def admin_dashboard():
        post_count = Post.query.count()
        service_count = Service.query.count()
        msg_count = ContactMessage.query.count()
        return render_template("admin/dashboard.html", post_count=post_count, service_count=service_count, msg_count=msg_count)

    # --- Post CRUD ---
    @app.route("/admin/posts")
    @login_required
    def admin_posts():
        posts = Post.query.order_by(Post.created_at.desc()).all()
        return render_template("admin/posts.html", posts=posts)

    @app.route("/admin/posts/new", methods=["GET", "POST"])
    @login_required
    def admin_post_new():
        form = PostForm()
        if form.validate_on_submit():
            if Post.query.filter_by(slug=form.slug.data).first():
                flash("Slug already exists. Choose another.", "warning")
            else:
                p = Post(title=form.title.data, slug=form.slug.data, body=form.body.data, published=form.published.data)
                db.session.add(p)
                db.session.commit()
                flash("Post created.", "success")
                return redirect(url_for("admin_posts"))
        return render_template("admin/post_form.html", form=form, mode="new")

    @app.route("/admin/posts/<int:post_id>/edit", methods=["GET", "POST"])
    @login_required
    def admin_post_edit(post_id):
        post = db.session.get(Post, post_id) or abort(404)
        form = PostForm(obj=post)
        if form.validate_on_submit():
            post.title = form.title.data
            post.slug = form.slug.data
            post.body = form.body.data
            post.published = form.published.data
            db.session.commit()
            flash("Post updated.", "success")
            return redirect(url_for("admin_posts"))
        return render_template("admin/post_form.html", form=form, mode="edit", post=post)

    @app.route("/admin/posts/<int:post_id>/delete", methods=["POST"])
    @login_required
    def admin_post_delete(post_id):
        post = db.session.get(Post, post_id) or abort(404)
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted.", "info")
        return redirect(url_for("admin_posts"))

    # --- Service CRUD ---
    @app.route("/admin/services")
    @login_required
    def admin_services():
        services = Service.query.order_by(Service.created_at.desc()).all()
        return render_template("admin/services.html", services=services)

    @app.route("/admin/services/new", methods=["GET", "POST"])
    @login_required
    def admin_service_new():
        form = ServiceForm()
        if form.validate_on_submit():
            s = Service(name=form.name.data, description=form.description.data, price_inr=form.price_inr.data)
            db.session.add(s)
            db.session.commit()
            flash("Service created.", "success")
            return redirect(url_for("admin_services"))
        return render_template("admin/service_form.html", form=form, mode="new")

    @app.route("/admin/services/<int:service_id>/edit", methods=["GET", "POST"])
    @login_required
    def admin_service_edit(service_id):
        service = db.session.get(Service, service_id) or abort(404)
        form = ServiceForm(obj=service)
        if form.validate_on_submit():
            service.name = form.name.data
            service.description = form.description.data
            service.price_inr = form.price_inr.data
            db.session.commit()
            flash("Service updated.", "success")
            return redirect(url_for("admin_services"))
        return render_template("admin/service_form.html", form=form, mode="edit", service=service)

    @app.route("/admin/services/<int:service_id>/delete", methods=["POST"])
    @login_required
    def admin_service_delete(service_id):
        service = db.session.get(Service, service_id) or abort(404)
        db.session.delete(service)
        db.session.commit()
        flash("Service deleted.", "info")
        return redirect(url_for("admin_services"))

    # --- Messages ---
    @app.route("/admin/messages")
    @login_required
    def admin_messages():
        msgs = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
        return render_template("admin/messages.html", msgs=msgs)

    return app

app = create_app()
