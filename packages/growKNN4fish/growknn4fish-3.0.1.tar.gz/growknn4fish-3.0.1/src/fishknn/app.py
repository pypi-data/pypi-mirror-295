from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import numpy as np
import os

from fishknn import common


def predict():
    """
    어종 분류기

    길이와 무게를 input으로 받으면 해당 물고기가 도미인지 빙어인지 예측합니다.
    해당 예측이 맞는지 input으로 받으며 해당 데이터를 csv로 저장합니다.

    - 기존에 저장된 csv 데이터가 있는지 확인합니다. 
      해당 파일을 DataFrame으로 불러오고 없으면 빈 DataFrame을 생성합니다.
        
    - 예측을 위해 model.pkl파일이 있는지 확인합니다.
      파일이 있는 경우 훈련된 model에 의해 예측하고 없을 경우 도미로 예측합니다.

    Args:
        - None
    Inputs:
        - l : 물고기의 길이(cm)
        - w : 물고기의 무게(kg)
        - chk : 물고기에 대한 예측이 맞는지 확인 (y/n)
    Returns:
        - DataFrame
    """

    CLASSES=["빙어","도미"]

    l=float(input("🆕 물고기의 길이를 입력하세요(cm) : "))
    w=float(input("🆕 물고기의 무게를 입력하세요(kg) : "))

    df = common.load_df()
    knn= common.load_pkl()
    ## 모델이 있는지
    if knn:
        ll=df["Length"].to_list()
        ll.append(l)
        
        wl=df["Weight"].to_list()
        wl.append(w)

        mu=np.mean(np.column_stack([ll, wl]),axis=0)
        std=np.std(np.column_stack([ll, wl]),axis=0)

        scaled_l=(l-mu[0])/std[0]
        scaled_w=(l-mu[1])/std[1]

        pred=knn.predict([[scaled_l,scaled_w]])
        pred=CLASSES[int(pred)]
    else:
        pred="도미"

    while True:
        rst = input(f"🆕 {pred}가 맞나요? (y/n)")
        if rst.lower()=="y":
            df=pd.concat([df,pd.DataFrame({"Length":[l],"Weight":[w],"Label":[pred]})])
            break
        elif rst.lower()=="n":
            df=pd.concat([df,pd.DataFrame({"Length":[l],"Weight":[w],"Label":[CLASSES[1-CLASSES.index(pred)]]})])
            break
        else:
            print("⛔ y 또는 n으로 답해주세요.")
            continue
            
    common.save_csv(df)

    return df


def train(data):
    """
    물고기 예측 훈련기

    KNN 알고리즘을 이용하여 물고기의 종류를 예측하는 모형을 훈련합니다.
    훈련이 끝나면 해당 모델을 pkl파일로 저장합니다.

    - 받은 데이터의 길이(row 수) 1인 경우 훈련을 하지 않고 넘어갑니다.
    - 받은 데이터의 길이(row 수) 5 미만인 경우 훈련에 사용하는 이웃의 수를 n으로 합니다.
    - 받은 데이터의 길이(row 수) 5 이상인 경우 훈련에 사용하는 이웃의 수를 5로 합니다.

    Args:
        - data : 물고기의 길이와 무게, 레이블 정도가 담긴 DataFrame
    Returns:
        - model : 훈련된 모형을 반환합니다.
    """

    print("🆕 훈련을 시작합니다.")


    import time
    from datetime import datetime

    t=time.time()
    df=data

    n=len(df)

    if n<2:
        print("⛔ 충분한 데이터가 없습니다.")
        print(f"🆕 훈련을 종료합니다. (훈련시간 : {datetime.fromtimestamp(time.time()-t).second}초)")
        return None
    elif n<5:
        knn=KNeighborsClassifier(n_neighbors=n)
    else:
        knn=KNeighborsClassifier(n_neighbors=5)
    
    fish_data=np.column_stack( [list(map(float,df["Length"].to_list())), list(map(float,df["Weight"].to_list()))] )
    fish_label=df["Label"].apply(lambda x:int(x=="도미")).to_list()

    mu = np.mean(fish_data,axis=0)
    std = np.std(fish_data,axis=0)

    z = (fish_data - mu) / std

    knn.fit(z,fish_label)
    
    common.save_pkl(knn)

    common.draw_plot(df,True)

    print(f"🆕 훈련을 종료합니다. (훈련시간 : {datetime.fromtimestamp(time.time()-t).second}초)")

    return knn
    

def get_pkl():
    """
    python package 경로에 저장된 pkl파일을 원하는 위치에 저장할 수 있도록 합니다.

    추후 저장된 pkl파일을 이용하여 예측 성능 테스트를 진행하고자 하는 경우
    모형을 load하기 편하도록 pkl파일을 복사하는 기능입니다.
    """
    
    knn=common.load_pkl()

    if knn:
        default_path=os.path.abspath(os.path.curdir)
        
        print("🆕 pkl파일을 저장할 경로를 입력해주세요(현재 경로기준 상대경로)")
        path=input(f" >>> {default_path}/")
        path=f"{default_path}/{path}"

        save_path=common.save_pkl(knn,path)
        print(f"🆕 저장이 완료되었습니다.(저장경로 : {save_path})")
    else:
        print("⛔ 훈련된 pkl파일이 없습니다.\n⛔ 모델 훈련 후 다시 확인해주세요.")

def show_data():
    """
    지금까지 csv로 저장된 data를 DataFrame형식으로 출력합니다.
    """
    
    df = common.load_df()
    print(df)


def draw_plot():
    """
    지금까지 csv로 저장된 data를 scatter plot으로 출력합니다.
    """

    df = common.load_df()

    common.draw_plot(df)

def run():
    df = predict()
    train(df)