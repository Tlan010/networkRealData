import re
import pandas as pd
from datetime import datetime

def parse_iperf_log_with_fixed_values(file_path):
    """解析iperf日志并合并固定值"""
    data = []
    
    # 预定义的固定值
    default_fixed_values = {
        'P1(dBm)': 20,
        'Fre1(MHz)': 5220,
        'W1(MHz)': 80,
        'P2(dBm)': 20,
        'Fre2(MHz)': 5220,
        'W2(MHz)': 80,
        'P3(dBm)': 20,
        'Fre3(MHz)': 5220,
        'W3(MHz)': 80,
        'P4(dBm)': 20,
        'Fre4(MHz)': 5220,
        'W4(MHz)': 80,
        'd1(cm)': 0,    
        'd2(cm)': 10,
        'd3(cm)': 20,
        'd4(cm)': 30,
    }

    
    with open(file_path, 'r') as f:
        for line in f:
            # 只处理包含性能数据的行
            if not line.strip().startswith('[  ') or 'ms' not in line:
                continue
                
            try:
                # 分割并清理数据行
                parts = [p for p in line.split() if p]
                loss_rate = line.strip().split('(')[-1].split('%)')[0]
                # 提取动态指标
                dynamic_data = {
                    'Transfer(KBytes)': float(parts[4]),
                    'Bandwidth(Kbits/sec)': float(parts[6]),
                    'Jitter(ms)': float(parts[8]),
                    'Loss_Rate(%)': float(loss_rate)
                }
                
                # 合并固定值和动态数据
                row = {**default_fixed_values, **dynamic_data}
                data.append(row)
                
            except (IndexError, ValueError) as e:
                print(f"跳过解析错误行: {line.strip()} | 错误: {e}")
    
    # 确保列顺序符合要求
    columns = [
        'P1(dBm)', 'Fre1(MHz)', 'W1(MHz)','d1(cm)',
        # 'P2(dBm)', 'Fre2(MHz)', 'W2(MHz)','d2(cm)',
        'P3(dBm)', 'Fre3(MHz)', 'W3(MHz)','d3(cm)',
        'P4(dBm)', 'Fre4(MHz)', 'W4(MHz)','d4(cm)',
        'Transfer(KBytes)', 'Bandwidth(Kbits/sec)', 
        'Jitter(ms)', 'Loss_Rate(%)'
    ]
    
    return pd.DataFrame(data)[columns]  # 按指定顺序排列列
    
# 使用示例
if __name__ == "__main__":
    # 从文件读取日志
    input_file = r".\rawData\100k-train\1-3-4-500.txt"
    output_file = r".\extractedData\100k\train\1-3-4-500.csv" 
    # 解析日志文件
    df = parse_iperf_log_with_fixed_values(input_file)
    df['Loss_Rate(%)'].fillna(100,inplace=True)
    # 保存为CSV
    df.to_csv(output_file, index=False)
    print(f"成功解析并保存结果到 {output_file}")
    print("\n前5行数据预览:")
    print(df.head())
    
    # 基本统计信息
    print("\n基本统计信息:")
    print(df.describe())
        
