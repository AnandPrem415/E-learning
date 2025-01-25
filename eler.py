from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///elearning.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

# Extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_instructor = db.Column(db.Boolean, default=False)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

# Routes
@app.route('/')
def home():
    courses = Course.query.all()
    return render_template('index.html', courses=courses)

@app.route('/courses/<int:course_id>')
def course_details(course_id):
    course = Course.query.get_or_404(course_id)
    lessons = Lesson.query.filter_by(course_id=course.id).all()
    return render_template('course_details.html', course=course, lessons=lessons)

@app.route('/courses/<int:course_id>/lessons/<int:lesson_id>')
def lesson_details(course_id, lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    return render_template('lesson_details.html', lesson=lesson)

@app.route('/create_course', methods=['GET', 'POST'])
def create_course():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        new_course = Course(title=title, description=description, instructor_id=1)  # Assuming instructor ID = 1
        db.session.add(new_course)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_course.html')

# Main
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
