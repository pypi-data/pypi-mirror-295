# weekly_1

## Background
- 파이썬 ML scikit-learn 의 sklearn.neighbors.KNeighborsClassifier 모듈을 이용한 물고기 감별기 (도미, 빙어)

## Why?
- ML 교육 과정에서 배웠던 파이썬 scikit-learn의 전반적인 내용을 이해 및 실습할 수 있다.
- 길이와 무게를 입력하여 어떠한 어종(도미 혹은 빙어)으로 예측되는지 파악할 수 있다.
- 길이와 무게를 입력하여 정답과 오답을 반복하면서 점진적으로 진화하는 모델을 확인할 수 있다.
- 해당 데이터들이 어떻게 밀집되어 있는지를 그래프(산점도)를 통해 확인할 수 있다.

## Install
```bash
$ pip install weekly_1
$ pip install git+https://github.com/EstherCho-7/guess_fish.git@<Branch Name>

# or for dev
$ git clone git@github.com:EstherCho-7/guess_fish.git
$ source .venv/bin/activate

# no .venv?
$ pdm venv create
```

## Command
```bash
# 길이, 무게를 입력 받아 어종을 파악
$ guess-fish

# 입력된 데이터들이 어떻게 분포해있는지 산점도를 통해 확인
$ plot
```

## Usage
```bash
# If you want to start with no data,
$ rm -rf *.pkl

# Prediction
$ guess-fish
```
```bash
# Result
$ guess-fish
물고기의 길이: 10.8
물고기의 무게: 8.7
입력하신 물고기는 빙어
맞습니까? 맞으면 T, 아니라면 F를 입력해주시기 바랍니다.: T
저는 물고기 민수입니다.
$ guess-fish
물고기의 길이: 26.8
물고기의 무게: 450
입력하신 물고기는 도미
맞습니까? 맞으면 T, 아니라면 F를 입력해주시기 바랍니다.: T
저는 물고기 민수입니다.
```
```bash
# Plot
$ plot
```
## Result
![image](https://github.com/user-attachments/assets/bf79252c-d033-4ded-a4f8-8d45e3d3fc4c)

