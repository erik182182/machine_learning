import numpy as np
import pandas as pd

symptom_csv = pd.read_csv('symptom.csv', delimiter=';')
disease_csv = pd.read_csv('disease.csv', delimiter=';')


symptoms_list = [np.random.randint(0, 2) for i in range(len(symptom_csv) - 1)]
print('Симптомы: ')
print(symptoms_list)
disease_to_prob = dict(
    zip(disease_csv['Болезнь'], (disease_csv['Количество'] / disease_csv['Количество'][len(disease_csv['Количество']) - 1])))

d_prob = list(disease_to_prob.values())[:-1]
for i in range(len(d_prob) - 1):
    for j in range(len(symptom_csv) - 1):
        if symptoms_list[j] == 1:
            d_prob[i] *= float(symptom_csv.iloc[j][i + 1].replace(',', '.'))
print('Диагноз: ' + list(disease_to_prob.keys())[d_prob.index(max(d_prob))])