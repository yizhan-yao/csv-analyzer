import pytest
import os
import tempfile
from analyzer.main import read_csv, get_basic_info, get_column_stats, format_report


def make_csv(content):
    """创建临时 CSV 文件，返回文件路径"""
    f = tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False, encoding="utf-8"
    )
    f.write(content)
    f.close()
    return f.name


class TestReadCsv:

    def test_read_normal(self):
        path = make_csv("name,age\nAlice,25\nBob,30\n")
        headers, rows = read_csv(path)
        assert headers == ["name", "age"]
        assert len(rows) == 2
        os.unlink(path)

    def test_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            read_csv("/不存在的文件.csv")

    def test_not_csv_extension(self):
        path = make_csv("name,age\nAlice,25\n")
        txt_path = path.replace(".csv", ".txt")
        os.rename(path, txt_path)
        with pytest.raises(ValueError):
            read_csv(txt_path)
        os.unlink(txt_path)



class TestGetColumnStats:

    def setup_method(self):
        """每个测试前准备好数据"""
        self.headers = ["name", "age", "score"]
        self.rows = [
            ["Alice", "25", "88.5"],
            ["Bob", "30", "92.0"],
            ["Charlie", "35", "75.5"],
        ]

    def test_stats_normal(self):
        stats = get_column_stats(self.headers, self.rows, "score")
        assert stats["count"] == 3
        assert stats["max"] == 92.0
        assert stats["min"] == 75.5
        assert stats["mean"] == 85.33

    def test_column_not_found(self):
        with pytest.raises(ValueError):
            get_column_stats(self.headers, self.rows, "不存在的列")

    def test_skip_non_numeric(self):
        """非数值列应该抛出 ValueError"""
        with pytest.raises(ValueError):
            get_column_stats(self.headers, self.rows, "name")



class TestFormatReport:

    def test_format_output(self):
        info = {"row_count": 3, "col_count": 3, "columns": ["name", "age", "score"]}
        stats_list = [{"column": "score", "count": 3, "mean": 85.33, "max": 92.0, "min": 75.5}]
        result = format_report(info, stats_list)
        assert "行数：3" in result
        assert "score" in result
        assert "85.33" in result
