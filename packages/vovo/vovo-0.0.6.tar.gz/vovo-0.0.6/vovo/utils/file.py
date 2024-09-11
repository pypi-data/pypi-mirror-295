import os
from dataclasses import is_dataclass, asdict

import pandas as pd
import requests
from pydantic import BaseModel
from tqdm import tqdm


def download_file_with_temporary_save(url, save_path):
    """下载文件并保存"""

    temp_save_path = save_path + ".part"  # 使用临时文件路径

    try:
        # 发送HTTP请求获取文件
        response = requests.get(url, stream=True)
        response.raise_for_status()  # 如果请求不成功，会抛出异常

        # 获取文件总大小
        total_size = int(response.headers.get('content-length', 0))

        # 打开文件以二进制写入
        with open(temp_save_path, 'wb') as file:
            # 使用 tqdm 显示进度条
            with tqdm(total=total_size, unit='B', unit_scale=True, desc=temp_save_path, initial=0, ascii=True) as pbar:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:  # 过滤掉保持活动的空块
                        file.write(chunk)
                        pbar.update(len(chunk))

        # 下载完成后重命名临时文件为最终文件
        os.rename(temp_save_path, save_path)
    except Exception:
        if os.path.exists(temp_save_path):
            os.remove(temp_save_path)  # 删除临时文件
        raise


def save_to_csv(data, filename='output.csv'):
    """定义一个函数来转换 dataclass | pydantic model 数据到 DataFrame 并保存为 CSV"""
    # 检查每个记录的类型并进行适当的转换
    records_dict = []
    for record in data:
        if isinstance(record, BaseModel):
            # 如果是 Pydantic 模型
            records_dict.append(record.model_dump())
        elif is_dataclass(record):
            # 如果是标准 dataclass
            records_dict.append(asdict(record))
        else:
            raise TypeError("Unsupported data type")

    # 将字典列表转换为 DataFrame
    df = pd.DataFrame(records_dict)

    # 将 DataFrame 保存为 CSV 文件
    df.to_csv(filename, index=False)

