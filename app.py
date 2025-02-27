from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Cấu hình Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Danh sách tài khoản mẫu (lưu trong bộ nhớ tạm)
users = {}

class User(UserMixin):
    def __init__(self, username, password):
        self.id = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Load user từ danh sách users
@login_manager.user_loader
def load_user(username):
    return users.get(username)

# Danh sách sinh viên mẫu
students = [
    {'id': 1, 'name': 'Nguyen Van A', 'dob': '2000-01-01', 'email': 'a@example.com', 'score': 85},
    {'id': 2, 'name': 'Tran Thi B', 'dob': '2001-02-14', 'email': 'b@example.com', 'score': 90}
]

# Trang chủ (chỉ hiển thị khi đã đăng nhập)
@app.route('/')
@login_required
def index():
    return render_template('index.html', students=students)

# Đăng ký tài khoản
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users:
            return "Tài khoản đã tồn tại!"

        users[username] = User(username, password)
        return redirect(url_for('login'))
    
    return render_template('register.html')

# Đăng nhập
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users.get(username)
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            return "Sai tài khoản hoặc mật khẩu!"

    return render_template('login.html')

# Đăng xuất
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        dob = request.form['dob']
        email = request.form['email']
        score = request.form['score']
        students.append({'id': len(students) + 1, 'name': name, 'dob': dob, 'email': email, 'score': score})
        return redirect(url_for('index'))
    
    return render_template('add_student.html')

if __name__ == '__main__':
    app.run(debug=True)
