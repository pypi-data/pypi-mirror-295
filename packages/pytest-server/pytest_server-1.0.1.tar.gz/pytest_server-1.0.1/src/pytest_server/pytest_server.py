import codecs
import ctypes
import os
import subprocess

from flask import Flask, Response, jsonify, request

app = Flask(__name__)
test_running = False


def is_admin():
    return ctypes.windll.shell32.IsUserAnAdmin()


@app.route("/runtests", methods=["POST"])
def stream_command():
    global test_running
    if test_running:
        # 如果测试已在运行，则直接返回提示信息
        return jsonify({"status": "Test already running."})
    else:
        test_running = True
        try:
            # venv/Scripts/python.exe
            python_path = request.form.get("python_path")
            main_file = request.form.get("main_file")
            build_path = request.form.get("build_path")

            def generate():
                os.chdir(os.path.dirname(main_file))
                process = subprocess.Popen(
                    f"{python_path} {main_file} {build_path}",
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                )

                def read_until_eof(stream):
                    decoder = codecs.getincrementaldecoder("utf-8")(
                        errors="replace"
                    )  # 使用'replace'策略处理非法字符
                    while True:
                        chunk = stream.read(512)  # 读取一块数据
                        if not chunk:
                            break
                        decoded_chunk = decoder.decode(chunk)
                        for line in decoded_chunk.splitlines(True):  # 处理换行符
                            yield line.rstrip("\n")

                # 用上面定义的函数读取并处理输出
                for line in read_until_eof(process.stdout):
                    yield line

                process.stdout.close()
                process.wait()
                if process.returncode != 0:
                    yield f"Command exited with code {process.returncode}\n"

            return Response(generate(), content_type="text/plain")
        finally:
            test_running = False


def run():
    if is_admin():
        app.run(debug=False, port=9999)
    else:
        print("请以管理员权限启动")
