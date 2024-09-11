# simple selfstudy fish

## Introduce

- KNN 알고리즘을 실습하는 용도의 프로젝트
- 아무런 모델이 없는 상태에서 시작해서 모델을 생성, 학습, 예측하도록 진행하는 것이 목표

## Installation

- pip 모듈을 이용
```
$ pip install <project_name>
```

## Usage

### ssf start

- 설치 이후 아래 명령어를 입력하여 메인 화면으로 진입
```
$ ssf start
```

- 시작하면 물고기의 길이와 무게를 입력하는 창이 활성화
```
- Length : 
```
```
- Weight : 
```

- 입력 단위는 cm/g 으로 진행하며, 이후 프로그램은 다음의 정보를 바탕으로 물고기의 예측을 진행함.

```
Is fish is <fish_prediction>? [yes/no]
```

- yes, no를 입력시 해당 정보에 대한 부분을 학습.
- 이 과정을 반복함.
