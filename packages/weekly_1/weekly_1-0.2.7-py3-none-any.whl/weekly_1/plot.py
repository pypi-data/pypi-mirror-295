import pickle
import matplotlib.pyplot as plt

file = "fish_data.pkl"

def load_data():
    with open(file, "rb") as f:
        data = pickle.load(f)
    return data['fish_data'], data['fish_target']

def plot_data():
    fish_data, fish_target = load_data()

    if fish_data:
        lengths, weights = zip(*fish_data)
        targets = fish_target

        plt.figure(figsize=(10, 6))
        scatter = plt.scatter(lengths, weights, c=targets, cmap='bwr', marker='o')
        plt.xlabel('length')
        plt.ylabel('weight')
        plt.title('Fish Graph')
        plt.colorbar(scatter, label='Target (Bream: 1, Smelt: 0)')
        plt.show()
    else:
        print("데이터가 없습니다.")

