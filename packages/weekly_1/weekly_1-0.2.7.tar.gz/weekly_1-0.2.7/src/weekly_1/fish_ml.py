from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import pickle
import os

file="fish_data.pkl"


def load_data():
    if not os.path.exists(file) or os.path.getsize(file)==0:
        return [], []
    with open(file, "rb") as f:
        fish=pickle.load(f)
    return fish['fish_data'], fish['fish_target']


def save_data(fish_data, fish_target):
    with open(file, "wb") as f:
        pickle.dump({'fish_data': fish_data, 'fish_target': fish_target}, f)

def guess_fish():
    fish_data, fish_target=load_data()

    length=float(input("물고기의 길이: "))
    weight=float(input("물고기의 무게: "))

    k=5
    model=KNeighborsClassifier(n_neighbors=k)

    if fish_data:
        if len(fish_data)<k:
            model.set_params(n_neighbors=len(fish_data))
        model.fit(fish_data, fish_target)
        prediction=model.predict([[length, weight]])
        predicted_type="도미" if prediction[0]==1 else "빙어"
        
        print(f"입력하신 물고기는 {predicted_type}")

    else:
        predicted_type="도미" if np.random.choice([0, 1])==1 else "빙어"
        print(f"입력하신 물고기는 {predicted_type}")

    answer=input("맞습니까? 맞으면 T, 아니라면 F를 입력해주시기 바랍니다.: ").strip().upper()

    if answer=="T":
        target=1 if predicted_type=="도미" else 0
        print("저는 물고기 민수입니다.")
    elif answer=="F":
        target=0 if predicted_type=="도미" else 1
        print("저는 물고기 준수입니다.")
    else:
        print("잘못 입력하셨습니다. Bye")
        return

    fish_data.append([length, weight])
    fish_target.append(target)
        
    model.fit(fish_data, fish_target)
    save_data(fish_data, fish_target)
