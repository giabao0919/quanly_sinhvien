from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Một danh sách sinh viên mẫu
students = [
    {'id': 1, 'name': 'Nguyen Van A', 'dob': '2000-01-01', 'email': 'a@example.com', 'score': 85},
    {'id': 2, 'name': 'Tran Thi B', 'dob': '2001-02-14', 'email': 'b@example.com', 'score': 90}
]

# Trang chủ hiển thị danh sách sinh viên
@app.route('/')
def index():
    return render_template('index.html', students=students)

# Thêm sinh viên mới (không kiểm tra tính hợp lệ)
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        dob = request.form['dob']
        email = request.form['email']
        score = int(request.form['score'])

        new_id = len(students) + 1
        students.append({'id': new_id, 'name': name, 'dob': dob, 'email': email, 'score': score})
        return redirect(url_for('index'))
    return render_template('add_student.html')

# Sửa thông tin sinh viên (không có phân quyền, bất kỳ ai cũng có thể sửa)
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = next((s for s in students if s['id'] == id), None)
    if student is None:
        return redirect(url_for('index'))

    if request.method == 'POST':
        student['name'] = request.form['name']
        student['dob'] = request.form['dob']
        student['email'] = request.form['email']
        student['score'] = int(request.form['score'])
        return redirect(url_for('index'))

    return render_template('edit_student.html', student=student)

# Chạy ứng dụng
if __name__ == '__main__':
    app.run(debug=True)
