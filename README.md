# csv-analyzer

命令行 CSV 数据分析工具，读取 CSV 文件并计算统计信息。

## 功能

- 读取 CSV 文件，显示行数、列数、列名
- 计算指定数值列的均值、最大值、最小值
- 自动跳过非数值数据
- 完善的异常处理（文件不存在、文件为空、列不存在）
- 日志记录

## 安装

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
##使用

python src/analyzer/main.py
按提示输入 CSV 文件路径和要分析的列名。

##测试

pytest tests/test_main.py -v --cov=src/analyzer
8 个测试用例，覆盖率 72%。