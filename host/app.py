import os
import tempfile
import zipfile
import shutil
from flask import Flask, render_template, request, jsonify
from checker import run_checker
app = Flask(__name__)

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'zip'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def run_checker(extracted_path):
#     """
#     Simulate running the checker and returning results
#     In a real implementation, this would call your actual checker script
#     """
#     # This is where you would call your checker.py
#     # For this example, we'll simulate it
    
#     # In a real implementation, you would do something like:
#     # import checker
#     # results = checker.check_project(extracted_path)
#     # return results
    
#     # Simulated results
#     results = """=== Project Check Results ===

# Frontend Checks:
# ✅ Home page loads successfully
# ✅ Navigation to About page works
# ❌ Contact page missing required form elements

# Backend Checks:
# ✅ /api/data endpoint returns correct status
# ✅ Database connection established
# ❌ /api/users missing required fields

# === Summary ===
# Passed: 4/6 checks"""
    
#     # Write to check.txt (simulating what your checker would do)
#     check_file = os.path.join(extracted_path, 'check.txt')
#     with open(check_file, 'w') as f:
#         f.write(results)
    
#     return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'projectFile' not in request.files:
        return jsonify({'success': False, 'message': 'No file part'})
    
    student_id = request.form.get('studentId', 'unknown')
    file = request.files['projectFile']
    
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file'})
    
    if file and allowed_file(file.filename):
        # Create a temporary directory to extract the zip
        temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(temp_dir, file.filename)
        file.save(zip_path)
        
        try:
            # Extract the zip file
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Run the checker
            results = run_checker(temp_dir)
            
            # Clean up
            shutil.rmtree(temp_dir)
            
            return jsonify({
                'success': True,
                'message': 'File successfully checked',
                'results': results
            })
        except Exception as e:
            shutil.rmtree(temp_dir, ignore_errors=True)
            return jsonify({
                'success': False,
                'message': f'Error processing file: {str(e)}'
            })
    else:
        return jsonify({
            'success': False,
            'message': 'Invalid file type. Only ZIP files are allowed'
        })

if __name__ == '__main__':
    app.run(debug=True)