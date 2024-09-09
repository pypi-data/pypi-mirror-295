import os
import pickle
from sklearn.neighbors import KNeighborsClassifier

model_path='/home/hahahellooo/homework/fish/src/fish'
# 사용자로부터 길이와 무게를 입력받는 함수
def input_data():
    while True:
        try:
            length = float(input("길이를 입력하세요(cm): "))
            weight = float(input("무게를 입력하세요(g): "))
            return [length, weight]
        except ValueError:
            print("숫자를 입력해주세요")

# 모델 저장 함수
def save_model(model, training_data, targets, model_path, filename="knn_model.pkl"):
    file_path = os.path.join(model_path, filename)

    with open(file_path, 'wb') as f:
        pickle.dump((model, training_data, targets), f)
    print("모델 저장 완료!")


# 모델 불러오기 함수
def load_model(model_path, filename="knn_model.pkl"):
    
    file_path=os.path.join(model_path, filename)
    
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            model, training_data, targets = pickle.load(f)
        print("모델 불러오기 성공!")
        return model, training_data, targets
    else:
        print("모델이 없습니다. 새로 학습을 시작합니다. ")
        return None, [], []

# 메인 함수
def main():
    filename = "knn_model.pkl"

    # 저장된 모델 불러오기
    model, training_data, targets = load_model(model_path, filename)

    if not model:
        k = 5
        model=KNeighborsClassifier(n_neighbors=k) # KNN 모델
    
    while True:
        data = input_data()
        
        if len(training_data) >=  model.n_neighbors:
            # 학습 데이터가 충분할 경우 모델을 학습하고 예측
            model.fit(training_data, targets)
            prediction = model.predict([data])[0] # 예측값 반환(도미 or 빙어)
            # 예측 결과 출력
            if prediction == 0:
                print("예측 결과 도미입니다.🐠")
            else:
                print("예측 결과 빙어입니다.🐟")
            
            # 예측 결과에 대한 사용자 피드백 받기
            feedback = input("예측한 결과가 맞나요?(🐠/🐟): ").strip()
            
            # 피드백에 따라 라벨 저장(도미:0, 빙어:1)
            if feedback == "도미":
                label = 0
            elif feedback == "빙어":
                label = 1
            else:
                print("다시 입력해주세요.")
                continue

            training_data.append(data)
            targets.append(label)
        
        else:    
                # 훈련 데이터가 없을 때는 데이터와 라벨을 입력하여 학습 데이터로 저장
            print("훈련 데이터가 부족합니다. 데이터를 입력해주세요.")
            feedback = input("정답 (도미/빙어): ").strip()
            # 피드백에 따라 label 저장
            if feedback == "도미":
                label = 0
            elif feedback == "빙어":
                label = 1
            else:
                print("다시 입력해주세요.")
                continue

            training_data.append(data)
            targets.append(label)
        
        # 모델 및 학습 데이터 저장
        save_model(model, training_data, targets, model_path, filename)
# 프로그램 실행
if __name__ == "__main__":
    main()

