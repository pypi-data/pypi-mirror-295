import os
import time

import requests


def run_tests(project_path, build_path):
    # 请求接口在本地执行测试
    url = "http://localhost:9999/runtests"
    response = requests.post(
        url,
        data={
            "python_path": os.path.join(project_path, "venv/Scripts/python.exe"),
            "main_file": os.path.join(project_path, "main.py"),
            "build_path": build_path,
        },
        stream=True,
        proxies=None,
    )
    for line in response.iter_lines(decode_unicode=True):
        if line:
            print(line.encode("utf-8").decode("gbk", "ignore"))
    time.sleep(2)


def upload_allure_results(
    password,
    allure_result_path,
    jenkins_project_path,
    ssh_host="admin@192.168.100.12",
    hostkey="SHA256:bYke1QiOG0h/qS2cCli3SB/1ot7fWTWnuX8ETsYfOUM",
):
    """
    下载安装putty：https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html
    安装putty后，将安装目录的pscp.exe拷贝到 C:\Windows\System32目录
    """
    cmd_upload_report = rf"pscp -pw {password} -r -batch -hostkey {hostkey} {allure_result_path} {ssh_host}:{jenkins_project_path}"
    print(cmd_upload_report)
    os.system(cmd_upload_report)
