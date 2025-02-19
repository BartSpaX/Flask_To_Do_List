from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Task, bcrypt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "supersecretkey"

db.init_app(app)
bcrypt.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Strona główna
@app.route("/")
def home():
    return render_template("index.html")

# Rejestracja użytkownika
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = bcrypt.generate_password_hash(request.form["password"]).decode("utf-8")

        if User.query.filter_by(username=username).first():
            return "Użytkownik już istnieje!"

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))

    return render_template("register.html")

# Logowanie użytkownika
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("home"))
        else:
            error = "Błędna nazwa użytkownika lub hasło!"

    return render_template("login.html", error=error)

# Wylogowanie użytkownika
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

# Dostęp do Panelu Administratora tylko dla użytkownika z role = admin
@app.route("/admin")
@login_required
def admin():
    if current_user.role != "admin":
        return redirect(url_for("home"))
    users = User.query.filter(User.role == "user").all()
    return render_template("admin.html", users=users)

@app.route("/admin/manage-users")
@login_required
def manage_users():
    if current_user.role != "admin":
        return redirect(url_for("home"))
    users = User.query.all()
    return render_template("manage_users.html", users=users)

@app.route("/admin/manage-users/user/<int:user_id>")
@login_required
def edit_user(user_id):
    if current_user.role != "admin":
        return redirect(url_for("home"))
    user = User.query.get(user_id)
    if not user:
        return "Użytkownik nie istnieje!", 404
    return render_template("edit_user.html", user=user)

@app.route("/admin/manage-users/user/<int:user_id>/edit", methods=["POST"])
@login_required
def update_user(user_id):
    if current_user.role != "admin":
        return redirect(url_for("home"))
    user = User.query.get(user_id)
    if not user:
        return "Użytkownik nie istnieje!", 404
    user.username = request.form["username"]
    user.role = request.form["role"]
    db.session.commit()
    return redirect(url_for("manage_users"))

@app.route("/admin/manage-users/user/delete-user/<int:user_id>", methods=["POST"])
@login_required
def delete_user(user_id):
    if current_user.role != "admin":
        return redirect(url_for("home"))
    user = User.query.get(user_id)
    if not user:
        return "Użytkownik nie istnieje!", 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"Użytkownik {user.username} został usunięty."}), 200

@app.route("/admin/manage-users/user/add", methods=["POST"])
@login_required
def add_new_user():
    if not current_user.is_authenticated or current_user.role != "admin":
        return jsonify({"error": "Brak uprawnień"}), 403

    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        role = data.get("role", "user")

        if not username or not password:
            return jsonify({"error": "Wszystkie pola są wymagane."}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({"error": "Użytkownik o takiej nazwie już istnieje."}), 409

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        new_user = User(username=username, password=hashed_password, role=role)
        
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": f"Użytkownik {username} został dodany jako {role}!"}), 201

    except Exception as e:
        db.session.rollback()  # Cofnięcie transakcji w razie błędu
        return jsonify({"error": f"Błąd serwera: {str(e)}"}), 500

# API: Pobieranie zadań użytkownika
@app.route("/api/tasks", methods=["GET"])
@login_required
def get_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return jsonify([{"id": t.id, "title": t.title, "done": t.done} for t in tasks])

# API: Dodanie zadania
@app.route("/api/tasks", methods=["POST"])
@login_required
def add_task():
    data = request.get_json()
    new_task = Task(title=data["title"], user_id=current_user.id)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"id": new_task.id, "title": new_task.title, "done": new_task.done}), 201

# API: Zmiana statusu zadania
@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
@login_required
def update_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not task:
        return jsonify({"message": "Task not found"}), 404

    data = request.get_json()
    task.done = data["done"]
    db.session.commit()
    return jsonify({"id": task.id, "title": task.title, "done": task.done})

# API: Usunięcie zadania
@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
@login_required
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not task:
        return jsonify({"message": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"})

# API: Przydzielenie zadania konkretnemu użytkownikowi z poziomu Panelu Administratora
@app.route("/api/admin/assign-task", methods=["POST"])
@login_required
def assign_task():
    if current_user.role != "admin":
        return jsonify({"error": "Nie masz uprawnień do tej operacji"}), 403

    data = request.get_json()
    user_id = data.get("user_id")
    title = data.get("title")

    if not user_id or not title:
        return jsonify({"error": "Brak wymaganych danych"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Użytkownik nie istnieje"}), 404

    new_task = Task(title=title, user_id=user_id)
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"message": f"Zadanie '{title}' przypisane do {user.username}"}), 201

@app.route("/user/settings", methods=["GET"])
@login_required
def user_settings():
    return render_template("user_settings.html")

@app.route("/user/settings/edit", methods=["POST"])
@login_required
def edit_your_account():
    # if current_user.id != user_id:
    #     return jsonify({"error": "Brak uprawnień do tej opercaji!"}), 403
    
    data = request.get_json()
    username = data.get("username")

    if User.query.filter_by(username=username).first():
            return jsonify({"error": "Nazwa użytkownika jest już zajęta!"})
            
    user = User.query.get(current_user.id)

    user.username = username
    db.session.commit()
    return jsonify({"message": "Zapisano ustawienia!"})


if __name__ == "__main__":
    app.run(debug=True)
