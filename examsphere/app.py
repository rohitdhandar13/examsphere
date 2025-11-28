import os
from flask import Flask, render_template, request, redirect, session, url_for, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret")

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "127.0.0.1"),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", "Rohitd@555"),
    "database": os.environ.get("DB_NAME", "examsphere"),
    "port": int(os.environ.get("DB_PORT", 3306)),
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

@app.route("/")
def index():
    try:
        db = get_db()
        cur = db.cursor(dictionary=True)
        cur.execute("SELECT id, title, category, organization, apply_link, description, last_date FROM jobs ORDER BY created_at DESC LIMIT 8")
        jobs = cur.fetchall()
        cur.close(); db.close()
    except Exception as e:
        app.logger.error("DB error on index: %s", e)
        jobs = []
    return render_template("index.html", jobs=jobs)

@app.route("/jobs")
def jobs():
    q = request.args.get('q','').strip()
    cat = request.args.get('category','').strip()
    try:
        db = get_db()
        cur = db.cursor(dictionary=True)
        sql = "SELECT id, title, category, organization, apply_link, description, last_date FROM jobs WHERE 1=1"
        params = []
        if q:
            sql += " AND (title LIKE %s OR organization LIKE %s OR description LIKE %s)"
            like = f"%{q}%"
            params.extend([like, like, like])
        if cat:
            sql += " AND category = %s"
            params.append(cat)
        sql += " ORDER BY created_at DESC"
        cur.execute(sql, params)
        jobs = cur.fetchall()
        cur.close(); db.close()
    except Exception as e:
        app.logger.error("DB error on jobs: %s", e)
        jobs = []
    return render_template("jobs.html", jobs=jobs, q=q, category=cat)

@app.route("/job/<int:job_id>")
def job_detail(job_id):
    try:
        db = get_db()
        cur = db.cursor(dictionary=True)
        cur.execute("SELECT * FROM jobs WHERE id=%s", (job_id,))
        job = cur.fetchone()
        cur.close(); db.close()
    except Exception as e:
        app.logger.error("DB error on job_detail: %s", e)
        job = None
    if not job:
        return render_template("404.html"), 404
    return render_template("job_detail.html", job=job)

@app.route("/signup", methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name','').strip()
        email = request.form.get('email','').strip().lower()
        password = request.form.get('password','')
        if not name or not email or not password:
            flash("Fill all fields", "warning")
            return redirect(url_for('signup'))
        try:
            db = get_db()
            cur = db.cursor()
            cur.execute("SELECT id FROM users WHERE email=%s", (email,))
            if cur.fetchone():
                cur.close(); db.close()
                flash("Email already registered", "warning")
                return redirect(url_for('signup'))
            hashed = generate_password_hash(password)
            cur.execute("INSERT INTO users (name,email,password) VALUES (%s,%s,%s)", (name,email,hashed))
            db.commit()
            cur.close(); db.close()
            flash("Account created. Please log in.", "success")
            return redirect(url_for('login'))
        except Exception as e:
            app.logger.error("DB error on signup: %s", e)
            flash("Server error. Try again later.", "danger")
            return redirect(url_for('signup'))
    return render_template("signup.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            db = get_db()
            cur = db.cursor(dictionary=True)
            cur.execute("SELECT * FROM users WHERE email=%s", (email,))
            user = cur.fetchone()
            cur.close()
            db.close()
        except Exception as e:
            app.logger.error("DB error on login: %s", e)
            return render_template('login.html', error="Server error, try again.")

        if not user:
            return render_template('login.html', error="Invalid email or password")

        db_password = user["password"]  # hashed password

        # verify password
        if check_password_hash(db_password, password):
            session['user_id'] = user["id"]
            session['user_name'] = user["name"]
            session['email'] = user["email"]
            session['is_admin'] = user.get("is_admin", 0)
            return redirect('/dashboard')
        else:
            return render_template('login.html', error="Invalid email or password")

    return render_template('login.html')



def current_user():
    if session.get('user_id'):
        return {"id": session.get('user_id'), "name": session.get('user_name'), "is_admin": session.get('is_admin', False)}
    return None

@app.route("/dashboard")
def dashboard():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    user = current_user()
    try:
        db = get_db()
        cur = db.cursor(dictionary=True)
        cur.execute("SELECT a.id, j.title, j.organization, a.applied_on FROM applications a JOIN jobs j ON a.job_id=j.id WHERE a.user_id=%s ORDER BY a.applied_on DESC", (user['id'],))
        apps = cur.fetchall()
        cur.close(); db.close()
    except Exception as e:
        app.logger.error("DB error on dashboard: %s", e)
        apps = []
    return render_template("dashboard.html", user=user, applications=apps)

@app.route("/apply/<int:job_id>", methods=['POST'])
def apply_job(job_id):
    if not session.get('user_id'):
        flash("Please login to apply", "warning")
        return redirect(url_for('login'))
    user_id = session['user_id']
    try:
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT id FROM applications WHERE user_id=%s AND job_id=%s", (user_id, job_id))
        if cur.fetchone():
            flash("You already applied for this job", "info")
        else:
            cur.execute("INSERT INTO applications (user_id, job_id) VALUES (%s,%s)", (user_id, job_id))
            db.commit()
            flash("Application submitted", "success")
        cur.close(); db.close()
    except Exception as e:
        app.logger.error("DB error on apply: %s", e)
        flash("Server error. Try again later.", "danger")
    return redirect(url_for('job_detail', job_id=job_id))

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out", "info")
    return redirect(url_for('index'))

@app.route('/admin/add-job', methods=['GET','POST'])
def admin_add_job():
    user = current_user()
    if not user or not user.get('is_admin'):
        return "Forbidden", 403
    if request.method == 'POST':
        title = request.form.get('title')
        category = request.form.get('category')
        organization = request.form.get('organization')
        apply_link = request.form.get('apply_link')
        description = request.form.get('description')
        last_date = request.form.get('last_date') or None
        try:
            db = get_db()
            cur = db.cursor()
            cur.execute("INSERT INTO jobs (title, category, organization, apply_link, description, last_date) VALUES (%s,%s,%s,%s,%s,%s)",
                        (title, category, organization, apply_link, description, last_date))
            db.commit()
            cur.close(); db.close()
            flash("Job added", "success")
            return redirect(url_for('admin_add_job'))
        except Exception as e:
            app.logger.error("DB error admin add job: %s", e)
            flash("Server error", "danger")
    return render_template('admin_add_job.html')

if __name__ == '__main__':
    app.run(debug=True)
