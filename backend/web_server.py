import json
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
# 导入我们之前写好的核心逻辑类
from app import ExamSystem

# 初始化系统实例
system = ExamSystem("data/人工智能编程语言学生名单.txt")


class SimpleAPIHandler(BaseHTTPRequestHandler):
    def _set_cors_headers(self, status_code=200):
        """设置跨域请求头(CORS)，允许前端页面跨域访问 API"""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        """处理浏览器的预检请求"""
        self._set_cors_headers()

    def do_GET(self):
        """处理前端发来的 GET 请求 (如查找学生)"""
        parsed_url = urllib.parse.urlparse(self.path)

        # 1. 路由解析：建议使用 .rstrip('/') 处理掉末尾可能的斜杠
        if parsed_url.path.rstrip('/') == '/api/search':
            # 解析 URL 中的查询参数 (?id=xxx)
            query_params = urllib.parse.parse_qs(parsed_url.query)
            target_id = query_params.get('id', [None])[0]

            # 统一先设置响应头（包含 200 状态码和 JSON 类型）
            self._set_cors_headers(200)

            # 调用核心逻辑查找学生
            found_student = None
            if target_id:
                for student in system.students:
                    if str(student.stu_id).strip() == str(target_id).strip():  # 增强匹配稳定性
                        found_student = student
                        break

            if found_student:
                response_data = {
                    "success": True,
                    "name": found_student.name,
                    "gender": found_student.gender,
                    "class_name": found_student.class_name,
                    "college": found_student.college
                }
            else:
                # 即使没找到，也返回 200 状态码和友好的 JSON 消息，避免前端 fetch 报错
                response_data = {
                    "success": False,
                    "message": "未找到该学生，请检查学号是否输入正确"
                }

            self.wfile.write(json.dumps(response_data).encode('utf-8'))

        else:
            # 如果路径完全不对，再返回错误
            self.send_error(404, "API Endpoint Not Found")

    def do_POST(self):
        """处理前端发来的 POST 请求 (如点名、生成文件)"""
        if self.path == '/api/rollcall':
            # 读取并解析前端发来的 JSON 数据体
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            count = data.get('count', 0)

            self._set_cors_headers()

            try:
                import random
                selected = random.sample(system.students, count)
                # 将对象列表转换为字典列表，以便序列化为 JSON
                result = [{"name": s.name, "id": s.stu_id} for s in selected]
                self.wfile.write(json.dumps({"students": result}).encode('utf-8'))
            except ValueError:
                self.wfile.write(json.dumps({"message": "输入数量超过总人数或无效"}).encode('utf-8'))

        elif self.path == '/api/generate_schedule':
            self._set_cors_headers()
            try:
                system.generate_exam_schedule()
                self.wfile.write(json.dumps({"status": "success"}).encode('utf-8'))
            except Exception as e:
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))

        elif self.path == '/api/generate_tickets':
            self._set_cors_headers()
            try:
                system.generate_admission_tickets()
                self.wfile.write(json.dumps({"status": "success"}).encode('utf-8'))
            except Exception as e:
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
        else:
            self.send_error(404, "API Endpoint Not Found")


def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleAPIHandler)
    print(f"🚀 后端 API 服务器已启动，正在监听端口 {port}...")
    print("👉 现在你可以直接双击打开 frontend/index.html 进行操作了！")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print("服务器已关闭。")


if __name__ == '__main__':
    run_server()