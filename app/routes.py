import os
import cloudinary.uploader
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.forms import NewsForm, LoginForm, ResetPasswordForm
from app.models import News, User, Video

main = Blueprint('main', __name__)

# 🔹 Categories
categories = [
    ("top", "टॉप न्यूज़"),
    ("state", "राज्य-शहर"),
    ("Science&Tech", "विज्ञान और तकनीक"),
    ("cricket", "क्रिकेट"),
    ("national", "देश"),
    ("international", "विदेश"),
    ("sports", "स्पोर्ट्स"),
    ("bollywood", "बॉलीवुड"),
    ("education", "जॉब - एजुकेशन"),
    ("business", "बिज़नेस"),
    ("lifestyle", "लाइफस्टाइल"),
    ("spiritual", "जीवन मंत्र"),
]

# 🔧 Utility: Extract YouTube video ID
def extract_youtube_id(url):
    if "watch?v=" in url:
        return url.split("watch?v=")[-1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[-1].split("?")[0]
    return None

# 🏠 Home Page
@main.route('/')
def home():
    news_list = News.query.order_by(News.created_at.desc()).all()
    videos = Video.query.order_by(Video.created_at.desc()).limit(6).all()
    return render_template('home.html', news_list=news_list, videos=videos, categories=categories)

# 📰 News Detail Page
@main.route('/news/<int:news_id>')
def news_detail(news_id):
    news = News.query.get_or_404(news_id)
    return render_template('news_detail.html', news=news)

# 🔐 Admin Login
@main.route('/admin/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html', form=form)

# 🔓 Logout
@main.route('/admin/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

# 📋 Admin Dashboard
@main.route('/admin/dashboard')
@login_required
def dashboard():
    news_list = News.query.order_by(News.created_at.desc()).all()
    video_list = Video.query.order_by(Video.created_at.desc()).all()
    return render_template('dashboard.html', news_list=news_list, video_list=video_list)

# ➕ Add News with Cloudinary
@main.route('/admin/news/add', methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        image_url = None

        if form.image.data:
            upload_result = cloudinary.uploader.upload(form.image.data)
            image_url = upload_result.get('secure_url')

        new_article = News(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            image=image_url
        )
        db.session.add(new_article)
        db.session.commit()
        flash('✅ News added successfully with Cloudinary image!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('add_news.html', form=form)

# 🗑 Delete News
@main.route('/admin/news/delete/<int:news_id>')
@login_required
def delete_news(news_id):
    news = News.query.get_or_404(news_id)
    db.session.delete(news)
    db.session.commit()
    flash('🗑 News deleted successfully.', 'warning')
    return redirect(url_for('main.dashboard'))



# 📂 Filter by Category
@main.route('/category/<string:category>')
def category_filter(category):
    news_list = News.query.filter_by(category=category).order_by(News.created_at.desc()).all()
    return render_template('home.html', news_list=news_list, categories=categories)

# ➕ Add YouTube Video
@main.route('/admin/videos/add', methods=['GET', 'POST'])
@login_required
def add_video():
    if request.method == 'POST':
        title = request.form.get('title')
        youtube_url = request.form.get('youtube_url')
        video_id = extract_youtube_id(youtube_url)

        if title and video_id:
            new_video = Video(title=title, youtube_url=video_id)
            db.session.add(new_video)
            db.session.commit()
            flash('✅ YouTube video added successfully!', 'success')
            return redirect(url_for('main.videos'))

        flash('❗ Invalid YouTube link or title missing.', 'danger')

    return render_template('add_video.html')

# 🎥 Public Video Page
@main.route('/videos')
def videos():
    video_list = Video.query.order_by(Video.created_at.desc()).all()
    return render_template('videos.html', video_list=video_list)

# 🗑 Delete Video
@main.route('/admin/video/delete/<int:video_id>')
@login_required
def delete_video(video_id):
    video = Video.query.get_or_404(video_id)
    db.session.delete(video)
    db.session.commit()
    flash('🗑️ Video deleted successfully.', 'warning')
    return redirect(url_for('main.dashboard'))

# 🔐 Reset Admin Password
@main.route('/admin/reset-password', methods=['GET', 'POST'])
@login_required
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        if check_password_hash(current_user.password, form.old_password.data):
            current_user.password = generate_password_hash(form.new_password.data)
            db.session.commit()
            flash("🔐 Password successfully updated. Please log in again.", "success")
            logout_user()
            return redirect(url_for('main.login'))
        else:
            flash("❌ Old password is incorrect.", "danger")

    return render_template("reset_password.html", form=form)

# 🔍 Search
from sqlalchemy import or_
from flask import request, render_template
from app.models import News, Video

@main.route('/search')
def search():
    query = request.args.get('q', '').strip().lower()

    if query:
        news_list = News.query.filter(
            or_(
                News.title.ilike(f"%{query}%"),
                News.content.ilike(f"%{query}%"),
                News.category.ilike(f"%{query}%")
            )
        ).order_by(News.created_at.desc()).all()

        video_list = Video.query.filter(
            Video.title.ilike(f"%{query}%")
        ).order_by(Video.created_at.desc()).all()
    else:
        news_list = []
        video_list = []

    return render_template('home.html', news_list=news_list, video_list=video_list, categories=categories)

# Add this at the top
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import db
from app.models import User  # Your Admin model

# Route to edit admin name
# ✅ ROUTE: Edit Admin Username (and Name)
@main.route('/admin/edit-admin', methods=['GET', 'POST'])
@login_required
def edit_admin():
    if request.method == 'POST':
        new_name = request.form.get('name')
        new_username = request.form.get('username')

        # Check if new username is already taken by another user
        if new_username and new_username != current_user.username:
            existing_user = User.query.filter_by(username=new_username).first()
            if existing_user:
                flash('❌ Username already taken. Please choose a different one.', 'danger')
                return render_template('edit_admin.html', admin=current_user)

        # Update fields
        current_user.name = new_name
        current_user.username = new_username
        db.session.commit()

        flash('✅ Admin name and username updated successfully! Please login again.', 'success')
        logout_user()  # Force logout after username change
        return redirect(url_for('main.login'))

    return render_template('edit_admin.html', admin=current_user)

@main.route('/initdb')
def initdb():
    from app import db
    db.create_all()
    return '✅ Tables created in database!'

@main.route("/db_check")
def db_check():
    from app import db
    return f"Connected to: {db.engine.url}"

@main.route("/check_admin")
def check_admin():
    from app.models import User
    user = User.query.first()
    if user:
        return f"Admin user found: {user.username}"
    else:
        return "No admin user found"

@app.route("/initdb")
def init_db_web():
    from app.models import User
    from werkzeug.security import generate_password_hash

    username = "Sresti_@345!_News234"
    password = generate_password_hash("ChangeThis@123!")
    if not User.query.filter_by(username=username).first():
        admin = User(username=username, password=password)
        db.session.add(admin)
        db.session.commit()
        return "Admin created"
    return "Admin already exists"
