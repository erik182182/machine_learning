import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd

embarked_array = ["C", "S", "Q"]

data = pd.read_csv("titanic.csv")

ages = list(data.Age)
numb = list(range(1, len(ages) + 1))
colors = []
for i in range(0, len(ages)):
    if ages[i] >= 18:
        colors.append("r")
    else:
        colors.append("b")

plt.xlabel('Номер')
plt.ylabel('Возраст')

red_patch = mpatches.Patch(color='red', label='Совершеннолетние')
blue_patch = mpatches.Patch(color='blue', label='Несовершеннолетние')
plt.legend(handles=[red_patch, blue_patch])

plt.bar(numb, ages, color=colors)
plt.show()
