# weekly_hw1 - 물고기 판별기
***

## How this program works
1. 학습된 모델이 없는 상태
2. 사용자는 길이, 무게 데이터를 입력
3. 사용자가 입력하는 처음 5번째까지의 데이터를 바탕으로 예측값 출력(도미, 빙어)
4. 사용자는 예측값의 정답을 다시 입력
5. 위 과정을 반복
6. 모델은 쌓인 데이터를 바탕으로 학습을 반복하고 진화함

## Install
```bash
$ pip install fishml_guess 
```

## Usage
```bash
$ guess-fish
길이를 입력하세요(cm): # 길이 입력
무게를 입력하세요(g): # 무게 입력
예측 결과 도미입니다.🐠 
예측한 결과가 맞나요?(🐠/🐟): # 도미/빙어 중 정답을 입력
```

## Result
![image](https://github.com/user-attachments/assets/e1910049-cc4a-4643-97f2-cd18dd023500)

## Issue

데이터가 5개 이상일 때부터 물고기 판별기가 작동하도록 설정
5개 이상을 입력하더라도 데이터 입력만을 요구(예측값을 출력하지 않음)
guess-fish를 exit해야만 pickle 파일이 생성되고 모델 실행

![image](https://github.com/user-attachments/assets/50ba4e2f-2f3e-4269-b21c-ebf55df6954a)

## Refence
https://github.com/hahahellooo/hw_fishml.git
