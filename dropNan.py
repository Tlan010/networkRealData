import pandas as pd

def drop_nan(df,change_point):
    #Drop rows with 100 of Loss_Rate(%) cloumn
    filtered_df = df[df['Loss_Rate(%)'] != 100.0].copy()
    filtered_df['original_index'] = filtered_df.index
    filtered_df=filtered_df.reset_index(drop=True)


    mask = filtered_df['original_index'].isin(change_point)
    new_change_point = filtered_df.index[mask].tolist()

    # 移除original_index列（最终输出）
    final_df = filtered_df.drop(columns=['original_index'])
    return final_df,new_change_point

if __name__ == "__main__":
    # 从文件读取文件
    input_file = r".\extractedData\new\1-4.csv" 
    change_point=[]
    df,change_point = drop_nan(pd.read_csv(input_file),change_point=change_point)
    print(change_point)
    output_file = rf".\extractedData\new\1-4-dropnan{'-'.join(map(str, change_point))}.csv" 
    df.to_csv(output_file, index=False)