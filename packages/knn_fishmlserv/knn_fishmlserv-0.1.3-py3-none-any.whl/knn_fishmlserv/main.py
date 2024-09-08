from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
import numpy as np

def ping():
    print("pong")

def is_exit(result_e):
    if result_e.lower() == 'exit':
        print("프로그램을 종료합니다.")
        return True  # 프로그램 종료를 위한 신호 반환
    return False

class FishClassifier:
    def __init__(self, neighbors=5):
        # 데이터 초기화
        self.fish_data = []
        self.fish_target = []
        self.neighbors = neighbors
        
        # KNN 모델 초기화
        self.kn = KNeighborsClassifier(n_neighbors=self.neighbors)

    def add_initial_data(self):
        # 초기 데이터 입력받기
        length_input = input("물고기의 길이를 입력하세요: ")
        if is_exit(length_input):
            return False
        weight_input = input("물고기의 무게를 입력하세요: ")
        if is_exit(length_input):
            return False

        # 입력값이 유효한지 확인
        try:
            length = float(length_input)
            weight = float(weight_input)
        except ValueError:
            print("잘못된 입력입니다. 숫자를 입력하세요. :")
            return False  # 종료

        if length + weight > 30:
            answer = '도미'
        else:
            answer = '빙어'
        print(f"이 녀석은 바로 {answer}")

        # 정답 입력받기
        answer = input("정답을 입력하세요: ")

        for _ in range(self.neighbors):
            # 초기 데이터 추가
            self.fish_data.append([length, weight])
            self.fish_target.append(answer)

        # 모델 학습
        self.kn.fit(self.fish_data, self.fish_target)
        return True  # 계속 실행

    def fit_and_predict(self):
        length_input = input("물고기의 길이를 입력하세요: ")
        if is_exit(length_input):
            return False
        weight_input = input("물고기의 무게를 입력하세요: ")
        if is_exit(weight_input):
            return False
        try:
            length = float(length_input)
            weight = float(weight_input)
        except ValueError:
            print("잘못된 입력입니다. 숫자를 입력하세요. :")
            return False  # 종료
        
        # 입력받은 데이터를 예측
        predict = self.kn.predict([[length, weight]])[0]
        
        print(f"이 녀석은 바로 {predict}")
        
        # 정답 입력받기
        answer = input("정답을 입력하세요: ")
        
        # 새로운 데이터 추가
        self.fish_data.append([length, weight])
        self.fish_target.append(answer)

        # 모델 다시 학습
        self.kn.fit(self.fish_data, self.fish_target)
        
        return True
    def draw_graph(self):
        # Convert fish_data to numpy array for easier manipulation
        fish_data_np = np.array(fish_classifier.fish_data)

        # Use kneighbors method to find neighbors
        distances, indexes = fish_classifier.kn.kneighbors([[25, 150]])

        # Plotting
        plt.scatter(fish_data_np[:, 0], fish_data_np[:, 1])  # All fish data points
        plt.scatter(25, 150, marker='^')  # New data point
        plt.scatter(fish_data_np[indexes, 0], fish_data_np[indexes, 1], marker='D')  # Nearest neighbors
        plt.xlabel('length')
        plt.ylabel('weight')
        plt.show()

    def run(self):
        self.add_initial_data()
        # 반복적으로 입력받기
        # 반복적으로 입력받기
        while True:
            if not self.fit_and_predict():
                break  # 종료 신호가 오면 종료
        self.draw_graph()
# 프로그램 실행
fish_classifier = FishClassifier()
#fish_classifier.run()
