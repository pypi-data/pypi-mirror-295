import pytest
from knn import calculate_distance, get_neighbors, predict

# 테스트할 훈련 데이터
training_data = [
    ([30, 600], '도미'),
    ([25, 500], '도미'),
    ([10, 300], '빙어'),
    ([15, 400], '빙어')
]

def test_calculate_distance():
    point1 = [30, 600]
    point2 = [25, 500]
    result = calculate_distance(point1, point2)
    assert round(result, 2) == 104.88  # 소수점 두 자리에서 104.88 정도가 나와야 함

def test_get_neighbors():
    test_data = [20, 450]
    neighbors = get_neighbors(training_data, test_data, 3)
    assert neighbors == ['도미', '빙어', '빙어']  # 3개의 가까운 이웃 확인

def test_predict():
    test_data = [20, 450]
    result = predict(training_data, test_data, 3)
    assert result == '빙어'  # 이웃 3개 중 빙어가 2개이므로 예측은 '빙어'


