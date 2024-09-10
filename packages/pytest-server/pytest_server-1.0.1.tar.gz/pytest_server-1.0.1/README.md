# pytest_server
### Start service
```shell
pytest-server
```
### Usage
```python
import os
import sys

from pytest_server.client import run_tests, upload_allure_results

# 传入外部参数
project_name = sys.argv[1]
build_number = sys.argv[2]
build_url = sys.argv[3]
project_path = os.path.dirname(os.path.abspath(__file__))
# 确定allure测试结果生成路径
result_path = os.path.join(project_path, "allure-results")
result_path_build = os.path.join(result_path, build_number)
# 执行测试
run_tests(
    project_path=project_path,
    build_path=result_path_build
)
# 上传allure结果文件
upload_allure_results(
    password='123456',
    allure_result_path=result_path,
    jenkins_project_path=rf'D:\jenkins\workspace\{project_name}',
    ssh_host='Administrator@192.168.100.18',
    hostkey='AAAAC3NzaC1lZDI1NTE5AAAAIHh2w7oqUW+zfUx75l6DwrKld9DlCWsXfwPkfS+2YycY',
)
```