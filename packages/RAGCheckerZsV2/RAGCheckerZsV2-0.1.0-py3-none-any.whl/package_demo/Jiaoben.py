# -*- coding: utf-8 -*-
import pandas as pd
import json

# 读取Excel文件中的特定Sheet
excel_file_path = '../questions.xlsx'  # Excel文件的路径
df = pd.read_excel(excel_file_path,sheet_name='questions')
# question = df.iloc[:, 0]  # 注意：索引从0开始，第二列对应索引1


# 确保retrieved_context列中的内容是字典格式
def parse_retrieved_context(value):
    if isinstance(value, str):
        try:
            # 将字符串转换为字典
            return json.loads(value.replace("'", "\""))
        except json.JSONDecodeError:
            return value
    return value

# 应用解析函数到retrieved_context列
df['retrieved_context'] = df['retrieved_context'].apply(parse_retrieved_context)

# 将DataFrame转换为JSON格式
json_data = df.to_json(orient='records', force_ascii=False)

# 打印或保存JSON数据
print(json_data)

# 如果你希望将JSON保存到文件
with open('output.json', 'w', encoding='utf-8') as json_file:
    json_file.write(json_data)
