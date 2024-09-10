from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
import numpy as np
import random
import json
import os

home_path = os.path.expanduser('~')
file_path = f"{home_path}/code/data"

fish = {
        0: '도미',
        1: '빙어'
    }

def save_data(file:str, data:list):
    with open(f"{file_path}/{file}", 'w') as f:
        json.dump(data, f)

def get_data(file):
    with open(f"{file_path}/{file}", 'r') as f:
        return json.load(f)

def main():
    model = KNeighborsClassifier()
    
    # 데이터 파일이 없을 때, 빈 파일 생성해주기
    if not os.path.exists(f"{file_path}/data.json"):
        os.makedirs(os.path.dirname(file_path), exist_ok = True)
        save_data("data.json", [])
        save_data("target.json", [])

    x_train = get_data("data.json")
    y_train = get_data("target.json")

    length = float(input("🐟 물고기의 길이를 입력하세요 (cm): "))
    weight = float(input("🐟 물고기의 무게를 입력하세요  (g): "))

    # n_neighbors의 기본값이 5이기 때문에 최소 5개의 데이터 필요
    # 데이터 5개 쌓일때까지 random으로 물고기 종류 지정
    if len(x_train) < 5:
        prd = random.choice([0, 1])
    else:
        model.fit(x_train, y_train)
        prd = int(model.predict([[length, weight]])[0])
    
    print(f"🐟 이 물고기는 {fish[prd]}입니다.")
    
    while True:
        correct = input("🐟 예측이 맞습니까? (y/n): " ).strip().lower()
    
        if correct == 'y':
            print("🐟 예측 성공🥳")
            break
        elif correct == 'n':
            print("🐟 예측 실패😱")
            prd = 1 - prd # prd 값이 0이면 1로, 1이면 0으로 바꿔주기
            break
        else:
            print("🐟 올바른 입력이 아닙니다.")
            continue

    x_train.append([length, weight])
    y_train.append(prd)

    save_data("data.json", x_train)
    save_data("target.json", y_train)

def chart():
    fish = get_data("data.json")
    target = get_data("target.json")

    bream = []
    smelt = []

    for i in range(len(fish)):
        if target[i] == 0:
            bream.append(fish[i])
        else:
            smelt.append(fish[i])

    bream = np.array(bream)
    smelt = np.array(smelt)
    plt.scatter(bream[:,0], bream[:,1], marker="o")
    plt.scatter(smelt[:,0], smelt[:,1], marker="8")
    plt.xlabel('length')
    plt.ylabel('weight')
    plt.show()
