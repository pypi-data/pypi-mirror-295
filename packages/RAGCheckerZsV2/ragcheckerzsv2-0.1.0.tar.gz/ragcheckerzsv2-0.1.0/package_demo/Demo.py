# -*- coding: utf-8 -*-
import os
import time

from ragchecker import RAGResults, RAGChecker
from ragchecker.metrics import all_metrics

import os

import pandas as pd
import json
import argparse

# 解析命令行参数
def parse_arguments():
    parser = argparse.ArgumentParser(description='Process Excel file and convert to JSON')
    parser.add_argument('excel_file_path', type=str, help='Path to the Excel file')
    parser.add_argument('sheet_name', type=str, help='Name of the sheet to process')
    return parser.parse_args()

# 读取Excel文件并转换为JSON
def main():

    args = parse_arguments()

    # 读取Excel文件中的特定Sheet
    df = pd.read_excel(args.excel_file_path, sheet_name=args.sheet_name)

    # 确保retrieved_context列中的内容是字典并包围在[]内
    def parse_retrieved_context(value):
        if isinstance(value, str):
            try:
                # 将字符串转换为字典
                parsed_value = json.loads(value.replace("'", "\""))
                # 如果转换后是字典，包裹成列表
                if isinstance(parsed_value, dict):
                    return [parsed_value]
                return parsed_value
            except json.JSONDecodeError:
                return value
        elif isinstance(value, dict):
            # 如果本身是字典，包裹成列表
            return [value]
        return value

    # 应用解析函数到retrieved_context列
    df['retrieved_context'] = df['retrieved_context'].apply(parse_retrieved_context)

    # 将DataFrame转换为JSON格式
    json_data = df.to_json(orient='records', force_ascii=False)

    # 打印或保存JSON数据
    print(json_data)

    # 保存JSON到文件
    with open('../examples/output.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json_data)
    with open('../examples/output.json', 'r', encoding='utf-8') as file:
        content = file.read()

        # 在内容开头添加'{"results": ['，在末尾添加']'
    # 注意：这里假设A.txt的内容已经是某种形式的列表元素，或者你想要忽略这个警告
    new_content = '{"results": ' + content + '}'

    # 将新内容写回A.txt
    with open('../examples/output.json', 'w', encoding='utf-8') as file:
        file.write(new_content)
main()
# initialize ragresults from json/dict
with open("../examples/output.json", encoding='utf-8') as fp:
    rag_results = RAGResults.from_json(fp.read())

# set-up the evaluator
evaluator = RAGChecker(
    extractor_name="openai/gpt-4o-2024-08-06",
    checker_name="openai/gpt-4o-2024-08-06",
    batch_size_extractor=32,
    batch_size_checker=32
)
evaluator.evaluate(rag_results, all_metrics)
print("CCCC"+str(rag_results))