from flask import Flask, render_template, request, jsonify
import csv
import json

app = Flask(__name__)

# Load student data from CSV file (only once when app starts)
def load_students():
    students = []
    with open('students.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            students.append({
                'sno': row['Sno'],
                'htno': row['HTNo'],
                'name': row['Full Name'],
                'admno': row['Admn no'],
                'rollno': row['Roll no'],
                'category': row['Caste Category'],
                'dob': row['DOB'],
                'father': row['Father Name'],
                'parent_mobile': row['Parent Mobile'],
                'student_mobile': row['Student Mobile'],
                'email': row['Email']
            })
    return students

# Load data into memory (happens once at startup)
STUDENTS = load_students()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/students')
def get_students():
    """API endpoint to get all or filtered students"""
    search = request.args.get('search', '').lower()
    category = request.args.get('category', 'ALL')
    
    filtered = STUDENTS
    
    # Filter by category
    if category != 'ALL':
        filtered = [s for s in filtered if s['category'] == category]
    
    # Filter by search term
    if search:
        filtered = [s for s in filtered if 
            search in s['name'].lower() or
            search in s['rollno'].lower() or
            search in s['htno'].lower() or
            search in s['email'].lower() or
            search in s['student_mobile']
        ]
    
    return jsonify({
        'total': len(filtered),
        'students': filtered
    })

@app.route('/api/student/<htno>')
def get_student(htno):
    """Get single student by HT number"""
    student = next((s for s in STUDENTS if s['htno'] == htno), None)
    if student:
        return jsonify(student)
    return jsonify({'error': 'Student not found'}), 404

if __name__ == '__main__':
    print(f"Loaded {len(STUDENTS)} students into memory")
    app.run(debug=True, host='0.0.0.0', port=5000)