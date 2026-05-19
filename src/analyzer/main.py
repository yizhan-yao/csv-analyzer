import csv
import os
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def read_csv(filepath):
    logger.info(f"读取文件：{filepath}")
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"文件不存在：{filepath}")
    if not filepath.endswith(".csv"):
        raise ValueError(f"不是 CSV 文件：{filepath}")

    with open(filepath, encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader, None)
        if headers is None:
            raise ValueError("文件为空")
        rows = list(reader)

    logger.info(f"读取完成：{len(rows)} 行，{len(headers)} 列")
    return headers, rows


def get_basic_info(headers, rows):
    return {
        "row_count": len(rows),
        "col_count": len(headers),
        "columns": headers,
    }


def get_column_stats(headers, rows, column):
    logger.debug(f"计算列统计：{column}")
    if column not in headers:
        raise ValueError(f"列不存在：{column}")

    col_index = headers.index(column)
    values = []
    for row in rows:
        try:
            values.append(float(row[col_index]))
        except (ValueError, IndexError):
            logger.warning(f"跳过无法转换的值：{row[col_index] if col_index < len(row) else '缺失'}")

    if not values:
        raise ValueError(f"列 '{column}' 没有有效的数值数据")

    return {
        "column": column,
        "count": len(values),
        "mean": round(sum(values) / len(values), 2),
        "max": max(values),
        "min": min(values),
    }


def format_report(info, stats_list):
    lines = [
        f"行数：{info['row_count']}",
        f"列数：{info['col_count']}",
        f"列名：{', '.join(info['columns'])}",
        "",
    ]
    for stats in stats_list:
        lines.append(f"--- {stats['column']} ---")
        lines.append(f"  有效数据：{stats['count']} 个")
        lines.append(f"  均值：{stats['mean']}")
        lines.append(f"  最大值：{stats['max']}")
        lines.append(f"  最小值：{stats['min']}")
    return "\n".join(lines)


def main():
    filepath = input("请输入 CSV 文件路径：")
    try:
        headers, rows = read_csv(filepath)
        info = get_basic_info(headers, rows)
        print(f"\n列名：{', '.join(headers)}")

        column = input("请输入要分析的列名：")
        stats = get_column_stats(headers, rows, column)
        print(format_report(info, [stats]))
    except FileNotFoundError as e:
        print(f"错误：{e}")
        logger.error(e)
    except ValueError as e:
        print(f"错误：{e}")
        logger.error(e)


if __name__ == "__main__":
    main()
