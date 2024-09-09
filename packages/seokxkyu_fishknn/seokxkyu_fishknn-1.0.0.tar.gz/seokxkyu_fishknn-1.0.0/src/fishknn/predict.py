import pandas as pd
import os
from sklearn.neighbors import KNeighborsClassifier

home_path = os.path.expanduser('~')
file_path = f"{home_path}/code/fishknn/data/fish.csv"

def fish_pred():
    # 물고기의 길이와 무게 입력받기
    l = float(input("🐟 물고기의 길이를 입력하세요 (cm): "))
    w = float(input("🐟 물고기의 무게를 입력하세요  (g): "))
    
    # 파일이 없으면 초기 데이터로 학습 파일 생성
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        fish_class = int(input("🐟 이 물고기는 빙어이면 1, 도미이면 0을 입력하세요: "))
        fish_real_name = "빙어" if fish_class == 1 else "도미"
        df = pd.DataFrame({'length': [l], "weight": [w], "label": [fish_class]})
        df.to_csv(file_path, index=False)
        print(f"학습용 데이터가 없으므로 데이터를 저장합니다. 정답 : {fish_real_name}")
        return True

    # 학습 데이터가 존재하면 파일을 불러옴
    df = pd.read_csv(file_path)
    
    # 데이터가 5개 이하인 경우 데이터 추가
    if len(df) <= 5:
        fish_class = int(input("🐟 이 물고기는 빙어이면 1, 도미이면 0을 입력하세요: "))
        fish_real_name = "빙어" if fish_class == 1 else "도미"
        new_df = pd.DataFrame({'length': [l], "weight": [w], "label": [fish_class]})
        df = pd.concat([df, new_df], ignore_index=True)
        df.to_csv(file_path, index=False)
        print(f"학습용 데이터가 부족하므로 데이터를 추가합니다. 현재 데이터의 수: {len(df)}")
        return True

    # 학습 데이터 준비
    x = df.drop('label', axis=1)
    y = df['label']
    
    # 모델 학습
    model = KNeighborsClassifier()
    model.fit(x, y)
    
    # 예측
    input_data = pd.DataFrame([[l, w]], columns=['length', 'weight'])  
    # 입력 데이터에 열 이름 추가
    prediction = model.predict(input_data)
    fish_pred_name = "빙어" if prediction == 1 else "도미"
    
    # 예측 결과 출력
    print(f"🐟 이 물고기는 {fish_pred_name}입니다.")
    correct = input("🐟 예측이 맞습니까? (y/n): ").lower()
    
    if correct == 'y':
        # 예측이 맞으면 학습 데이터 추가
        fish_class = 1 if fish_pred_name == "빙어" else 0
        new_df = pd.DataFrame({'length': [l], "weight": [w], "label": [fish_class]})
        df = pd.concat([df, new_df], ignore_index=True)
        df.to_csv(file_path, index=False)
        print("🐟 예측 성공🥳")
    else:
        # 예측이 틀렸을 경우 정답을 자동으로 추가
        fish_class = 1 if fish_pred_name == "도미" else 0  # 예측과 반대의 값이 정답
        fish_real_name = "도미" if fish_class == 0 else "빙어"
        if len(df) < 50:  # 학습 데이터가 50개 미만이면 추가
            new_df = pd.DataFrame({'length': [l], "weight": [w], "label": [fish_class]})
            df = pd.concat([df, new_df], ignore_index=True)
            df.to_csv(file_path, index=False)
        print(f"🐟 오답입니다. 정답은 {fish_real_name}입니다.")
    return True

