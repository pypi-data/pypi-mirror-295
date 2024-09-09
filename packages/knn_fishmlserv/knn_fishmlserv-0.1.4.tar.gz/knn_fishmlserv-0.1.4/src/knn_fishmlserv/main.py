from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
import numpy as np
#import plotext as plot


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
        self.length = 0
        self.weight = 0
        self.neighbors = neighbors
        
        # KNN 모델 초기화
        self.kn = KNeighborsClassifier(n_neighbors=self.neighbors)

        print("나가기를 원하면 exit을 입력하세요")

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
            return True  # 종료

        if length + weight > 30:
            answer = '도미'
        else:
            answer = '빙어'
        print(f"이 녀석은 바로 {answer}")

        # 정답 입력받기
        yn = input("정답을 입력하세요(Y/N):").strip().lower()
        if yn == "n":  
            if answer == fish[0]: 
                answer = fish[1]  
            elif answer == fish[1]: 
                answer = fish[0]  

        for _ in range(self.neighbors):
            # 초기 데이터 추가
            self.fish_data.append([length, weight])
            self.fish_target.append(answer)
            self.length = length
            self.weight = weight
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
            return True
        
        # 입력받은 데이터를 예측
        predict = self.kn.predict([[length, weight]])[0]
        
        print(f"이 녀석은 바로 {predict}")
        fish = ['도미','빙어']        
        # 정답 입력받기
        yn = input("정답을 입력하세요(Y/N):").strip().lower()
        print(f" yn : {yn}") 
        answer = predict
        if yn == "n":  
            if predict == fish[0]: 
                answer = fish[1]  
            elif predict == fish[1]: 
                answer = fish[0]

        # 새로운 데이터 추가
        self.fish_data.append([length, weight])
        self.fish_target.append(answer)
        self.length = length
        self.weight = weight
        # 모델 다시 학습
        self.kn.fit(self.fish_data, self.fish_target)
        
        return True

    def draw_graph(self):
        # Convert fish_data to numpy array for easier manipulation
        fish_data_np = np.array(fish_classifier.fish_data)

        # Use kneighbors method to find neighbors
        distances, indexes = fish_classifier.kn.kneighbors([[self.length, self.weight]])

        # Plotting
        plt.scatter(fish_data_np[:, 0], fish_data_np[:, 1])  # All fish data points
        plt.scatter(self.length,self.weight, marker='^')  # New data point
        plt.scatter(fish_data_np[indexes, 0], fish_data_np[indexes, 1], marker='D')  # Nearest neighbors
        plt.xlabel('length')
        plt.ylabel('weight')
        plt.show()

    def draw_graph_scatter(self):
        fish_data_np = np.array(self.fish_data)

        distances, indexes = self.kn.kneighbors([[self.length, self.weight]])
        x = fish_data_np[:, 0]
        #x = [1,10,24,35,67]
        y = fish_data_np[:, 1]
        print(x)
        #y = [2,345,345,656,677]
        print(y)
        # Create scatter plot of the fish data
        plot.scatter(x, y, color='blue')

        neighbor_points = fish_data_np[indexes[0]]
        print(neighbor_points[:,0])
        print(neighbor_points[:,1])

        plot.scatter(neighbor_points[:, 0], neighbor_points[:, 1], color='red')

        plot.title("Fish Data Scatter Plot with Neighbors")
        plot.xlabel("Length")
        plot.ylabel("Weight")

        # Display the plot
        plot.show()

    def run(self):
        self.add_initial_data()
        # 반복적으로 입력받기
        while True:
            if not self.fit_and_predict():
                break  # 종료 신호가 오면 종료
        self.draw_graph()
        #self.draw_graph_scatter()
# 프로그램 실행
fish_classifier = FishClassifier()
#fish_classifier.run()
