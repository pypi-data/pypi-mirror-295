import pandas as pd
import os
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
#import sys

home_path = os.path.expanduser('~')
file_path = f"{home_path}/data/fishpip/fish.csv"

#l = sys.argv[1] # 길이
#w = sys.argv[2] # 무게
#fish_class = sys.argv[3] # 정답

def watch_data():
    df = pd.read_csv(file_path)
    df_b = df[df['label'] == 0]
    df_s = df[df['label'] == 1]

    fig, ax = plt.subplots()
    _=ax.scatter(df_b['length'], df_b['weight'], label = 'Bream', c = 'r', edgecolor = 'black')
    _=ax.scatter(df_s['length'], df_s['weight'], label = 'Smelt', c = 'b', edgecolor = 'black')
    _=ax.set_xlabel('length')
    _=ax.set_ylabel('weight')
    _=ax.legend()
    plt.show()

def fish_pred(l:float,w:float, fish_class:int):
    if fish_class == 0:
        fish_real_name = "Bream"
    else:
        fish_real_name = "Smelt"
    # 파일이 없다면 예측이고 뭐고 파일부터 만들자
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok = True)
        df = pd.DataFrame({'length' : [l], "weight" : [w], "label" : [fish_class]})
        df.to_csv(file_path, index = False)
        print(f"학습용 데이터가 없으므로 데이터를 저장합니다. 정답 : {fish_real_name}")
        return True

    # 파일이 있다면
    df = pd.read_csv(file_path)
    if len(df) <= 5:
        new_df = pd.DataFrame({'length' : [l], "weight" : [w], "label" : [fish_class]})
        # df.append(new_df, ignore_index=True).to_csv(file_path, index=False)
        df = pd.concat([df, new_df], ignore_index=True)
        df.to_csv(file_path, index=False)
        print(f"학습용 데이터가 부족하므로 데이터를 추가합니다. 현재 데이터의 수 : {len(df)}")
        return True
    x = df.drop('label', axis = 1)
    y = df['label']
    
    model = KNeighborsClassifier()
    model.fit(x,y)

    prediction = model.predict([[l,w]])
    
    if prediction == 0:
        fish_pred_name = "Bream"
    else:
        fish_pred_name = "Smelt"
    
    # 예측이 정답이라면 학습용 csv에 추가
    if prediction == fish_class:
        new_df = pd.DataFrame({'length' : [l], "weight" : [w], "label" : [fish_class]})
        df.append(new_df, ignore_index=True).to_csv(file_path, index=False)
        print(f"정답입니다. 정답은 {fish_real_name}입니다.")
        print(f"예측값 : {fish_pred_name}")
        return True
    else:
        # 데이터가 너무 적으면 오답이여도 넣은게 좋아보입니다.
        if len(df) < 50:
            new_df = pd.DataFrame({'length' : [l], "weight" : [w], "label" : [fish_class]})
            df = pd.concat([df, new_df], ignore_index=True)
            df.to_csv(file_path, index=False)
        print(f"오답입니다. 정답은 {fish_real_name}입니다.")
        print(f"예측값 : {fish_pred_name}")
        return True
