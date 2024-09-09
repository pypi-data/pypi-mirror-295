# fishKNN

물고기의 길이와 무게를 입력하면 해당 물고기가 도미인지 빙어인지 예측하는 프로그램입니다. 예측 후에는 해당 예측이 맞았는지 확인하며, 해당 데이터를 csv로 저장하고 다시 학습을 진행하는 진화형 KNN 프로그램입니다.

### Versions
- `0.5.x` : project init publish. predict & get-pkl.
- `1.2.x` : help msg added.
- `2.0.x` : scatter plot added.
- `3.0.x` : common.py added (remove duplicated code) 

### Installation
```
$ pip install growKNN4fish
```

### Usage
```bash
$ fish-help      # 사용가능한 CLI Command를 출력합니다.
    ╭──────────────────────── 사용할 수 있는 CLI Command ───────────────────────╮
    │                                                                           │
    │ $ fish-predict    # 길이와 무게를 입력받아 물고기의 종류를 예측합니다.    │
    │ $ show-data       # 저장된 csv파일을 DataFrame형식으로 출력합니다.        │
    │ $ get-pkl         # 저장된 pkl파일을 원하는 위치로 복사합니다.            │
    │ $ draw-plot       # 저장된 csv파일을 scatter plot으로 출력합니다.         │
    │                                                                           │
    ╰───────────────────────────────────────────────────────────────────────────╯

$ fish-predict   # 길이와 무게를 입력하면 물고기의 종류를 예측합니다.
🆕 물고기의 길이를 입력하세요(cm) :
🆕 물고기의 무게를 입력하세요(kg) :
🆕 도미가 맞나요? (y/n)
⛔ y 또는 n으로 답해주세요.    # y, n(대소문자 구분X) 외의 값을 입력할 경우 발생. 올바른 값을 입력할 때까지 반복.

🆕 훈련을 시작합니다.
#### scatter plot 출력 (>=v2.0.0)
     ┌─────────────────────────────────────────────────────┐
 2.02┤                                                    *│
     │                                                     │
     │                                                     │
 1.56┤                                                     │
     │                                                     │
     │                                                     │
     │                                           *         │
 1.10┤                                          *          │
     │                                                     │
     │                                                     │
 0.63┤                                                     │
     │                                                     │
     │                                                     │
 0.17┤                                                     │
     │  *                                                  │
     │                                                     │
     │                                                     │
-0.29┤                                                     │
     │                                                     │
     │                                                     │
-0.75┤* *                                                  │
     └┬────────────┬────────────┬────────────┬────────────┬┘
    -0.74        -0.10        0.54         1.18        1.82
Weight                       Length
⛔ 충분한 데이터가 없습니다.    # csv에 저장된 데이터가 1개인 경우
🆕 훈련을 종료합니다. (훈련시간 : 0초)

$ get-pkl   # model.pkl 파일을 원하는 위치에 저장합니다. 추후 테스트를 위해 pkl파일을 가져오기 위한 프로그램입니다.
🆕 pkl파일을 저장할 경로를 입력해주세요(현재 경로기준 상대경로)
 >>> /home/root2/hw/fishKNN/

⛔ 훈련된 pkl파일이 없습니다.       # 저장된 pkl파일이 없는 경우 발생.
⛔ 모델 훈련 후 다시 확인해주세요.
$ show-data # 지금까지 저장된 csv를 DataFrame형태로 출력
   Length  Weight Label
0    35.0   700.0    도미
1    31.5   500.0    도미

⛔ 저장된 데이터가 없습니다.    # 저장된 csv가 없는 경우

$ draw-plot # 지금까지 저장된 csv를 scatter plot으로 출력
     ┌─────────────────────────────────────────────────────┐
 2.02┤                                                    *│
     │                                                     │
     │                                                     │
 1.56┤                                                     │
     │                                                     │
     │                                                     │
     │                                           *         │
 1.10┤                                          *          │
     │                                                     │
     │                                                     │
 0.63┤                                                     │
     │                                                     │
     │                                                     │
 0.17┤                                                     │
     │  *                                                  │
     │                                                     │
     │                                                     │
-0.29┤                                                     │
     │                                                     │
     │                                                     │
-0.75┤* *                                                  │
     └┬────────────┬────────────┬────────────┬────────────┬┘
    -0.74        -0.10        0.54         1.18        1.82
Weight                       Length
```

### Dependency
![pandas>=2.2.2](https://img.shields.io/badge/pandas>=2.2.2-150458.svg?style=for-the-badge&logo=pandas&logoColor=FFFFFF)

![scikit-learn>=1.5.1](https://img.shields.io/badge/scikit--learn>=1.5.1-F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=FFFFFF)

![plotext>=5.2.8](https://img.shields.io/badge/plotext>=5.2.8-000000.svg?style=for-the-badge&logo=python&logoColor=FFFFFF)

### License
- MIT
