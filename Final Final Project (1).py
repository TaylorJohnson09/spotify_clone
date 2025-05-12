from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from flask_migrate import Migrate
import stripe
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

# Define models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_premium = db.Column(db.Boolean, default=False)

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    artist = db.Column(db.String(100), nullable=False)

# Create the app
def create_app():
    app = Flask(__name__)

    # Configs
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SECRET_KEY'] = 'your_secret_key'
    stripe.api_key = "YOUR_STRIPE_SECRET_KEY"

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "login"

    # Define routes inside app context
    @app.route("/")
    def home():
        return redirect(url_for("login"))

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            username = request.form["username"]
            email = request.form["email"]
            password = generate_password_hash(request.form["password"])
            user = User(username=username, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for("dashboard"))
        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            user = User.query.filter_by(email=request.form["email"]).first()
            if user and check_password_hash(user.password, request.form["password"]):
                login_user(user)
                return redirect(url_for("dashboard"))
            flash("Login failed. Check credentials.")
        return render_template("login.html")

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("login"))

    @app.route("/dashboard")
    @login_required
    def dashboard():
        return render_template("dashboard.html")

    @app.route("/subscribe", methods=["POST"])
    @login_required
    def subscribe():
        user = User.query.get(current_user.id)
        user.is_premium = True
        db.session.commit()
        return redirect(url_for("dashboard"))

    @app.route("/songs")
    def songs():
        all_songs = Song.query.all()
        return render_template("songs.html", songs=all_songs)

    return app

# Required for login manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Run the app
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    file_path = db.Column(db.String(300), nullable=False)  # store path to the uploaded song file
@app.route("/dashboard")
@login_required
def dashboard():
    print("Single Ladies")  
    return render_template("dashboard.html")
