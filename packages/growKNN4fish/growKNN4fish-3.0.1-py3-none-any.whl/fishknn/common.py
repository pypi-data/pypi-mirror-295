import os
import pickle
import pandas as pd
import plotext as plx

filepath=os.path.dirname(os.path.abspath(__file__))

def load_df():
    """
    저장된 csv파일이 있는지 확인하고 DataFrame형식으로 반환합니다.
    """
    if os.path.exists(f"{filepath}/data/fish.csv"):
        df = pd.read_csv(f"{filepath}/data/fish.csv")
        df = df[["Length","Weight","Label"]]
    else:
        df = pd.DataFrame({"Length":[],"Weight":[],"Label":[]})

    return df

def save_csv(df,path=f"{filepath}/data"):
    """
    DataFrame을 csv파일로 저장합니다.

    Args:
        - df : DataFrame
        - path : csv파일을 저장할 경로. 기본값은 패키지 내부 data directory
    """
    os.makedirs(path,exist_ok=True)
    
    df.to_csv(f"{path}/fish.csv")

def load_pkl():
    """
    저장된 pkl파일을 가져옵니다.

    Args:
        None
    Returns:
        - knn : 저장된 pkl파일을 모형으로 반환
    """
    if os.path.exists(f"{filepath}/model/model.pkl"):
        with open(f"{filepath}/model/model.pkl", "rb") as f:
            knn=pickle.load(f)
    else:
        knn=None    
    
    return knn

def save_pkl(model,path=f"{filepath}/model"):
    """
    pkl파일을 저장합니다.

    Args:
        - model : 훈련된 knn 모형
        - path : pkl파일을 저장할 경로. 기본값은 패키지 내부 model directory
    Returns:
        - path : pkl파일이 저장된 경로.
    """
    os.makedirs(path,exist_ok=True)

    save_path = f"{path}/model.pkl".replace("//","/")
    with open(save_path, "wb") as f:
        pickle.dump(model,f)

    return save_path

def draw_plot(df, highlight_one=False, plotsize=(60,25)):
    """
    Scatter plot generator
    산점도를 그려줍니다. 마지막 하나를 강조할 것인지 여부를 정할 수 있으며, 산점도의 크기를 변경할 수 있습니다.

    Args:
        - df : DataFrame을 넣어줍니다. DataFrame은 "Length", "Weight", "Label" column을 포함해야 합니다.
        - highlight_one : 마지막 하나를 강조(빨간색으로 표시)할 것인지 여부, 기본값은 False
        - plotsize : plot의 크기를 tuple형태로 받습니다. 기본값은 (60,25)
    """

    bream_data=df[df["Label"]=="도미"]
    smelt_data=df[df["Label"]=="빙어"]

    bream_l=bream_data["Length"]
    bream_w=bream_data["Weight"]

    smelt_l=smelt_data["Length"]
    smelt_w=smelt_data["Weight"]

    plx.scatter(bream_l,bream_w, color="blue", marker="*")
    plx.scatter(smelt_l,smelt_w, color="green", marker="*")

    if highlight_one:
        plx.scatter([df.iloc[-1,0]],[df.iloc[-1,1]],color="red", marker="*")

    plx.xlabel("Length")
    plx.ylabel("Weight")

    plx.plotsize(plotsize[0],plotsize[1])

    plx.show()