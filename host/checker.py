# import os
# import sys
# import subprocess
# import requests
# from bs4 import BeautifulSoup
# import unittest
# import time
# import shutil

# class FlaskSignSystemChecker:
#     def __init__(self, student_project_path):
#         self.student_path = student_project_path
#         self.template_path = os.path.join(student_project_path, 'templates')
#         self.process = None
#         self.port = 5001 # Flask 默认端口
#         self.tot_score = 0
#     def check_structure(self):
#         """检查文件结构是否符合要求"""
#         required_files = [
#             'app.py',
#             'templates/sign.html',
#             'templates/view.html'
#         ]
        
#         missing_files = []
#         for file in required_files:
#             if not os.path.exists(os.path.join(self.student_path, file)):
#                 missing_files.append(file)
        
#         if missing_files:
#             return False, f"缺少必要文件: {', '.join(missing_files)}"
#         self.tot_score += 25
#         return True, "文件结构检查通过"
    
#     def start_student_app(self):
#         """启动学生应用"""
#         try:
#             python_path = sys.executable
#             self.process = subprocess.Popen(
#                 [python_path, 'app.py'],
#                 cwd=self.student_path,
#                 stdout=subprocess.PIPE,
#                 stderr=subprocess.PIPE,
#                 env={'FLASK_ENV': 'development'}
#             )
            
#             # 更智能的启动检测
#             start_time = time.time()
#             timeout = 5  # 延长超时时间到30秒
            
#             while time.time() - start_time < timeout:
#                 try:
#                     # 检查进程是否仍在运行
#                     if self.process.poll() is not None:
#                         stdout, stderr = self.process.communicate()
#                         raise RuntimeError(
#                             f"应用进程已终止\n"
#                             f"标准输出: {stdout.decode('utf-8')}\n"
#                             f"标准错误: {stderr.decode('utf-8')}"
#                         )
                    
#                     # 尝试连接应用
#                     response = requests.get(
#                         f'http://localhost:{self.port}/',
#                         timeout=2,
#                         headers={'User-Agent': 'Checker'}
#                     )
                    
#                     # 即使返回403也认为应用已启动
#                     if response.status_code < 500:  # 接受任何非5xx状态码
#                         print(f"应用已响应，状态码: {response.status_code}")
#                         return
                    
#                 except requests.exceptions.RequestException:
#                     # 连接失败，继续等待
#                     time.sleep(0.5)
#                     continue
            
#             # 超时处理
#             stdout, stderr = self.process.communicate()
#             raise RuntimeError(
#                 f"应用启动超时\n"
#                 f"标准输出: {stdout.decode('utf-8')}\n"
#                 f"标准错误: {stderr.decode('utf-8')}"
#             )
            
#         except Exception as e:
#             raise RuntimeError(f"无法启动学生应用: {str(e)}")
#     def test_routes(self):
#         """测试路由是否正常工作"""
#         session = requests.Session()
#         headers = {
#             'User-Agent': 'Checker/1.0',
#             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#             'Connection': 'keep-alive'
#         }
        
#         results = []
#         tests = [
#             ('GET', '/', 200, '签到页面'),
#             ('GET', '/view', 200, '查看页面'),
#             ('POST', '/sign', 302, '签到提交', {'name': '测试用户'})
#         ]
        
#         for test in tests:
#             method, route, expected_status, description = test[:4]
#             data = test[4] if len(test) > 4 else None
            
#             try:
#                 if method == 'GET':
#                     response = session.get(
#                         f'http://localhost:{self.port}{route}',
#                         headers=headers,
#                         allow_redirects=False
#                     )
#                 else:
#                     headers['Content-Type'] = 'application/x-www-form-urlencoded'
#                     response = session.post(
#                         f'http://localhost:{self.port}{route}',
#                         data=data,
#                         headers=headers,
#                         allow_redirects=False
#                     )
                
#                 if response.status_code == expected_status:
#                     results.append((True, f"{description} ({route}) 正常"))
#                 else:
#                     results.append((False, f"{description} ({route}) 返回状态码: {response.status_code}"))
#                     print(f"响应头: {response.headers}")
#                     print(f"响应内容: {response.text[:200]}")
                    
#             except Exception as e:
#                 results.append((False, f"{description} ({route}) 测试失败: {str(e)}"))
        
#         return results
        
#     def stop_student_app(self):
#         """停止学生应用"""
#         if self.process:
#             self.process.terminate()
#             self.process.wait()
    

#     # def test_functionality(self):
#     #     """测试功能是否正常"""
#     #     results = []
        
#     #     try:
#     #         # 测试签到功能
#     #         test_name = "测试用户_" + str(int(time.time()))
#     #         response = requests.post(f'http://localhost:{self.port}/sign', data={'name': test_name})
            
            
#     #         # 检查签到名单
#     #         view_response = requests.get(f'http://localhost:{self.port}/view')
#     #         soup = BeautifulSoup(view_response.text, 'html.parser')
#     #         names = [li.text for li in soup.find_all('li')]
            
#     #         if test_name in names:
#     #             results.append((True, "签到名单显示正常"))
#     #         else:
#     #             results.append((False, "签到名单中没有找到测试用户"))
            
#     #         # 检查页面跳转链接
#     #         sign_page = requests.get(f'http://localhost:{self.port}/').text
#     #         view_page = requests.get(f'http://localhost:{self.port}/view').text
            
#     #         if 'href="/view"' in sign_page:
#     #             results.append((True, "签到页跳转链接正常"))
#     #         else:
#     #             results.append((False, "签到页缺少查看页面的跳转链接"))
                
#     #         if 'href="/"' in view_page:
#     #             results.append((True, "查看页返回链接正常"))
#     #         else:
#     #             results.append((False, "查看页缺少返回签到页的链接"))
                
#     #     except Exception as e:
#     #         results.append((False, f"功能测试失败: {str(e)}"))
        
#     #     return results
#     def test_functionality(self):
#         """测试功能是否正常，包含实际跳转验证"""
#         results = []
#         session = requests.Session()
#         base_url = f'http://localhost:{self.port}'
        
#         try:
#             # 1. 测试首页跳转链接
#             home_response = session.get(f'{base_url}/')
#             home_soup = BeautifulSoup(home_response.text, 'html.parser')
            
#             # 查找查看页面的链接
#             view_link = home_soup.find('a', href='/view')
#             if not view_link:
#                 results.append((False, "签到页缺少查看页面的跳转链接"))
#             else:
#                 # 实际点击链接测试跳转
#                 try:
#                     view_response = session.get(
#                         f"{base_url}{view_link['href']}",
#                         allow_redirects=True
#                     )
# # 替换原来的验证条件
#                     if (view_response.status_code == 200 and 
#                         ('/view' in view_response.url or 
#                         'view' in view_response.url)):  # 不限制是否包含.html
#                         self.tot_score += 25
#                         results.append((True, "跳转成功"))
#                     else:
#                         results.append((False, f"跳转到查看页面失败，状态码: {view_response.status_code}"))
#                 except Exception as e:
#                     results.append((False, f"跳转到查看页面时出错: {str(e)}"))
            
#             # 2. 测试查看页面返回链接
#             view_response = session.get(f'{base_url}/view')
#             view_soup = BeautifulSoup(view_response.text, 'html.parser')
            
#             # 查找返回签到页的链接
#             back_link = view_soup.find('a', href='/')
#             if not back_link:
#                 results.append((False, "查看页缺少返回签到页的链接"))
#             else:
#                 # 实际点击链接测试跳转
#                 try:
#                     home_response = session.get(
#                         f"{base_url}{back_link['href']}",
#                         allow_redirects=True
#                     )
#                     if home_response.status_code == 200 and ('/' in home_response.url or 'sign.html' in home_response.url):
#                         self.tot_score += 25
#                         results.append((True, "查看页返回链接正常(实际跳转成功)"))
#                     else:
#                         results.append((False, f"返回签到页失败，状态码: {home_response.status_code}"))
#                 except Exception as e:
#                     results.append((False, f"返回签到页时出错: {str(e)}"))
            
#             # 3. 测试签到功能
#             test_name = f"测试用户_{int(time.time())}"
#             try:
#                 sign_response = session.post(
#                     f'{base_url}/sign',
#                     data={'name': test_name},
#                     allow_redirects=False
#                 )
            
                
#                 # 检查签到名单
#                 view_response = session.get(f'{base_url}/view')
#                 view_soup = BeautifulSoup(view_response.text, 'html.parser')
#                 names = [li.text.strip() for li in view_soup.find_all('li')]
                
#                 if test_name in names:
#                     self.tot_score += 25
#                     results.append((True, "签到名单显示正常"))
#                 else:
#                     results.append((False, f"签到名单中没有找到测试用户，当前名单: {names}"))
                    
#             except Exception as e:
#                 results.append((False, f"签到功能测试失败: {str(e)}"))
                
#         except Exception as e:
#             results.append((False, f"功能测试过程中出错: {str(e)}"))
        
#         return results
#     def run_checks(self):
#         outputs = []
#         """运行所有检查"""
#         print("=== 开始检查 Flask 签到系统 ===")
        
#         # 检查文件结构
#         structure_ok, structure_msg = self.check_structure()
#         outputs.append(structure_msg+'\n')
#         print(f"文件结构检查: {'✓' if structure_ok else '✗'} {structure_msg}")
#         if not structure_ok:
#             return False
        
#         # 启动学生应用
#         try:
#             self.start_student_app()
#             print("学生应用已启动")
            
#             # 测试路由
#             print("\n路由测试:")
#             for success, msg in self.test_routes():
#                 print(f"{'✓' if success else '✗'} {msg}")
#                 outputs.append(msg+'\n')
            
#             # 测试功能
#             print("\n功能测试:")
#             for success, msg in self.test_functionality():
#                 print(f"{'✓' if success else '✗'} {msg}")
#                 outputs.append(msg+'\n')
#             outputs.append(f"总分: {self.tot_score}\n")
#             return outputs
            
#         except Exception as e:
#             print(f"检查过程中出错: {str(e)}")
#             return False
#         finally:
#             self.stop_student_app()
#             print("\n学生应用已停止")
        
#             print(f"总分: {self.tot_score}")

# def run_checker(extracted_path):
    
#     student_path = extracted_path
#     checker = FlaskSignSystemChecker(student_path)
#     return checker.run_checks()



import os
import sys
import subprocess
import requests
from bs4 import BeautifulSoup
import unittest
import time
import shutil

class FlaskSignSystemChecker:
    def __init__(self, student_project_path):
        self.student_path = student_project_path
        self.template_path = os.path.join(student_project_path, 'templates')
        self.process = None
        self.port = 5001 # Flask default port
        self.tot_score = 0
    
    def check_structure(self):
        """Check if the file structure meets requirements"""
        required_files = [
            'app.py',
            'templates/sign.html',
            'templates/view.html'
        ]
        
        missing_files = []
        for file in required_files:
            if not os.path.exists(os.path.join(self.student_path, file)):
                missing_files.append(file)
        
        if missing_files:
            return False, f"Missing required files: {', '.join(missing_files)}"
        self.tot_score += 25
        return True, "File structure check passed"
    
    def start_student_app(self):
        """Start the student application"""
        try:
            python_path = sys.executable
            self.process = subprocess.Popen(
                [python_path, 'app.py'],
                cwd=self.student_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env={'FLASK_ENV': 'development'}
            )
            
            # Smarter startup detection
            start_time = time.time()
            timeout = 5  # Extended timeout to 30 seconds
            
            while time.time() - start_time < timeout:
                try:
                    # Check if process is still running
                    if self.process.poll() is not None:
                        stdout, stderr = self.process.communicate()
                        raise RuntimeError(
                            f"Application process terminated\n"
                            f"Stdout: {stdout.decode('utf-8')}\n"
                            f"Stderr: {stderr.decode('utf-8')}"
                        )
                    
                    # Try to connect to the application
                    response = requests.get(
                        f'http://localhost:{self.port}/',
                        timeout=2,
                        headers={'User-Agent': 'Checker'}
                    )
                    
                    # Consider the app started even if it returns 403
                    if response.status_code < 500:  # Accept any non-5xx status code
                        print(f"Application responded, status code: {response.status_code}")
                        return
                    
                except requests.exceptions.RequestException:
                    # Connection failed, keep waiting
                    time.sleep(0.5)
                    continue
            
            # Timeout handling
            stdout, stderr = self.process.communicate()
            raise RuntimeError(
                f"Application startup timeout\n"
                f"Stdout: {stdout.decode('utf-8')}\n"
                f"Stderr: {stderr.decode('utf-8')}"
            )
            
        except Exception as e:
            raise RuntimeError(f"Failed to start student application: {str(e)}")
    
    def test_routes(self):
        """Test if routes are working properly"""
        session = requests.Session()
        headers = {
            'User-Agent': 'Checker/1.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection': 'keep-alive'
        }
        
        results = []
        tests = [
            ('GET', '/', 200, 'Sign-in page'),
            ('GET', '/view', 200, 'View page'),
            ('POST', '/sign', 302, 'Sign-in submission', {'name': 'Test User'})
        ]
        
        for test in tests:
            method, route, expected_status, description = test[:4]
            data = test[4] if len(test) > 4 else None
            
            try:
                if method == 'GET':
                    response = session.get(
                        f'http://localhost:{self.port}{route}',
                        headers=headers,
                        allow_redirects=False
                    )
                else:
                    headers['Content-Type'] = 'application/x-www-form-urlencoded'
                    response = session.post(
                        f'http://localhost:{self.port}{route}',
                        data=data,
                        headers=headers,
                        allow_redirects=False
                    )
                
                if response.status_code == expected_status:
                    results.append((True, f"{description} ({route}) working"))
                else:
                    results.append((False, f"{description} ({route}) returned status code: {response.status_code}"))
                    print(f"Response headers: {response.headers}")
                    print(f"Response content: {response.text[:200]}")
                    
            except Exception as e:
                results.append((False, f"{description} ({route}) test failed: {str(e)}"))
        
        return results
        
    def stop_student_app(self):
        """Stop the student application"""
        if self.process:
            self.process.terminate()
            self.process.wait()
    
    def test_functionality(self):
        """Test if functionality works properly, including actual redirect verification"""
        results = []
        session = requests.Session()
        base_url = f'http://localhost:{self.port}'
        
        try:
            # 1. Test home page redirect link
            home_response = session.get(f'{base_url}/')
            home_soup = BeautifulSoup(home_response.text, 'html.parser')
            
            # Find view page link
            view_link = home_soup.find('a', href='/view')
            if not view_link:
                results.append((False, "Sign-in page missing view page redirect link"))
            else:
                # Actually click the link to test redirect
                try:
                    view_response = session.get(
                        f"{base_url}{view_link['href']}",
                        allow_redirects=True
                    )
                    # Replace original verification condition
                    if (view_response.status_code == 200 and 
                        ('/view' in view_response.url or 
                        'view' in view_response.url)):  # Don't restrict .html inclusion
                        self.tot_score += 25
                        results.append((True, "Redirect successful"))
                    else:
                        results.append((False, f"Redirect to view page failed, status code: {view_response.status_code}"))
                except Exception as e:
                    results.append((False, f"Error redirecting to view page: {str(e)}"))
            
            # 2. Test view page return link
            view_response = session.get(f'{base_url}/view')
            view_soup = BeautifulSoup(view_response.text, 'html.parser')
            
            # Find return to sign-in page link
            back_link = view_soup.find('a', href='/')
            if not back_link:
                results.append((False, "View page missing return to sign-in page link"))
            else:
                # Actually click the link to test redirect
                try:
                    home_response = session.get(
                        f"{base_url}{back_link['href']}",
                        allow_redirects=True
                    )
                    if home_response.status_code == 200 and ('/' in home_response.url or 'sign.html' in home_response.url):
                        self.tot_score += 25
                        results.append((True, "View page return link working (actual redirect successful)"))
                    else:
                        results.append((False, f"Return to sign-in page failed, status code: {home_response.status_code}"))
                except Exception as e:
                    results.append((False, f"Error returning to sign-in page: {str(e)}"))
            
            # 3. Test sign-in functionality
            test_name = f"Test_User_{int(time.time())}"
            try:
                sign_response = session.post(
                    f'{base_url}/sign',
                    data={'name': test_name},
                    allow_redirects=False
                )
            
                # Check sign-in list
                view_response = session.get(f'{base_url}/view')
                view_soup = BeautifulSoup(view_response.text, 'html.parser')
                names = [li.text.strip() for li in view_soup.find_all('li')]
                
                if test_name in names:
                    self.tot_score += 25
                    results.append((True, "Sign-in list displayed correctly"))
                else:
                    results.append((False, f"Test user not found in sign-in list, current list: {names}"))
                    
            except Exception as e:
                results.append((False, f"Sign-in functionality test failed: {str(e)}"))
                
        except Exception as e:
            results.append((False, f"Error during functionality testing: {str(e)}"))
        
        return results
    
    def run_checks(self):
        outputs = []
        """Run all checks"""
        print("=== Starting Flask Sign-in System Check ===")
        
        # Check file structure
        structure_ok, structure_msg = self.check_structure()
        outputs.append(structure_msg)
        print(f"File structure check: {'✓' if structure_ok else '✗'} {structure_msg}")
        if not structure_ok:
            return False
        
        # Start student application
        try:
            self.start_student_app()
            print("Student application started")
            
            # Test routes
            print("\nRoute testing:")
            for success, msg in self.test_routes():
                print(f"{'✓' if success else '✗'} {msg}")
                outputs.append('\n'+msg)
            
            # Test functionality
            print("\nFunctionality testing:")
            for success, msg in self.test_functionality():
                print(f"{'✓' if success else '✗'} {msg}")
                outputs.append('\n'+msg)
            outputs.append(f"\nTotal score: {self.tot_score}")
            return outputs
            
        except Exception as e:
            print(f"Error during checking: {str(e)}")
            return False
        finally:
            self.stop_student_app()
            print("\nStudent application stopped")
        
            print(f"Total score: {self.tot_score}")

def run_checker(extracted_path):
    student_path = extracted_path
    checker = FlaskSignSystemChecker(student_path)
    return checker.run_checks()