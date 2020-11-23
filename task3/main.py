import numpy as np
import matplotlib.cm as cm
from matplotlib import pyplot as plt

from Cmeans import Cmeans

# создание точек
n = 100
points = np.array([[np.random.randint(low=0, high=100), np.random.randint(low=0, high=100)] for k in range(50)])

# создание цветовой схемы
x = np.arange(n)
color_arr = [i + x + (i * x) ** 2 for i in range(10)]
colors = cm.rainbow(np.linspace(0, 2, len(color_arr)))

# кластеризация cmeans
cmeans = Cmeans(points, 2, 3, .5)
cmeans.iter()
clusters = cmeans.find_clusters()

# отрисовка точек по цветам соответствующего кластера
plt.figure(figsize=(4, 4))
plt.scatter(points[:, 0], points[:, 1], color=colors[clusters])
plt.show()
