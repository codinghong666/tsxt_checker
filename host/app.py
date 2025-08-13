import os
import tempfile
import zipfile
import shutil
from flask import Flask, render_template, request, jsonify
from checker import run_checker
import json
from datetime import datetime
app = Flask(__name__)

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'zip'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
RESULTS_DB = 'results_db.json'  # 存储结果的JSON文件
# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def load_results():
    """加载已有的检查结果"""
    if os.path.exists(RESULTS_DB):
        with open(RESULTS_DB, 'r') as f:
            return json.load(f)
    return []

def save_results(results):
    """保存检查结果"""
    with open(RESULTS_DB, 'w') as f:
        json.dump(results, f, indent=2 , ensure_ascii=False)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# Ensure upload folder ·exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'projectFile' not in request.files:
#         return jsonify({'success': False, 'message': 'No file part'})
    
#     student_id = request.form.get('studentId', 'unknown')
#     file = request.files['projectFile']
    
#     if file.filename == '':
#         return jsonify({'success': False, 'message': 'No selected file'})
    
#     if file and allowed_file(file.filename):
#         # Create a temporary directory to extract the zip
#         temp_dir = tempfile.mkdtemp()
#         zip_path = os.path.join(temp_dir, file.filename)
#         file.save(zip_path)
        
#         try:
#             # Extract the zip file
#             with zipfile.ZipFile(zip_path, 'r') as zip_ref:
#                 zip_ref.extractall(temp_dir)
            
#             # Run the checker
#             results = run_checker(temp_dir)
            
#             # Clean up
#             shutil.rmtree(temp_dir)
            
#             return jsonify({
#                 'success': True,
#                 'message': 'File successfully checked',
#                 'results': results
#             })
#         except Exception as e:
#             shutil.rmtree(temp_dir, ignore_errors=True)
#             return jsonify({
#                 'success': False,
#                 'message': f'Error processing file: {str(e)}'
#             })
#     else:
#         return jsonify({
#             'success': False,
#             'message': 'Invalid file type. Only ZIP files are allowed'
#         })


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'projectFile' not in request.files:
        return jsonify({'success': False, 'message': 'No file part'})
    
    student_id = request.form.get('studentId', 'unknown').strip()
    if not student_id:
        return jsonify({'success': False, 'message': 'Student ID is required'})
    
    file = request.files['projectFile']
    
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file'})
    
    if file and allowed_file(file.filename):
        temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(temp_dir, file.filename)
        file.save(zip_path)
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            results = run_checker(temp_dir)
            
            # 记录结果到数据库
            all_results = load_results()
            entry = {
                'student_id': student_id,
                'timestamp': datetime.now().isoformat(),
                'filename': file.filename,
                'results': results
            }
            all_results.append(entry)
            save_results(all_results)
            
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
    app.run(host='0.0.0.0', port=42071, debug=True)