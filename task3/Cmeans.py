import numpy as np

n = 100
class Cmeans():

    # инициализация
    def __init__(self, points, c=2, k=3, cut_param=0.9):
        self.points = points
        self.c = c
        self.k = k
        self.cut_value = cut_param
        self.max_iter = 100
        self.tolerance = 0.01
        self.dist = np.zeros((self.points.shape[0], self.k))
        self.centroids = np.array([[np.random.uniform(0, n), np.random.uniform(0, n)]
                                   for i in range(self.k)])
        self.rate = np.array([[np.random.uniform(0, 1)
                               for i in range(self.k)]
                              for j in range(self.points.shape[0])])
        self.clusters = np.array([])


    # нахождение центроидов
    def find_centers(self):
        self.centroids = (self.rate.T).dot(self.points) / self.rate.sum(axis=0)[:, None]

    def dif(self, par1, par2):
        return sum((i - j) ** 2 for i, j in zip(par1, par2))

    # обновление атрибутов на основе расчетов
    def update_rate(self):
        self.dist = np.array([[self.dif(i, j) for i in self.centroids] for j in self.points])
        self.rate = (1 / self.dist) ** (1 / (self.c - 1))
        self.update()
        self.rate = (self.rate / self.rate.sum(axis=1)[:, None])

    def update(self):
        arr = np.where(np.isinf(self.rate))
        for i in range(0, len(arr[0])):
            self.rate[arr[0][i]] = 0
            self.rate[arr[0][i]][arr[1][i]] = 1

    # итерации подсчетов центроидов
    def iter(self):
        iter = 1
        while iter < self.max_iter:
            prev_centroids = np.copy(self.centroids)
            self.find_centers()
            self.update_rate()
            if max([self.dif(i, k) for i, k in zip(self.centroids, prev_centroids)]) < self.tolerance:
                break
            iter += 1

    # получение кластеров
    def find_clusters(self):
        clusters = np.array([])
        for i in range(len(self.rate)):

            i_max = self.rate[i][0]
            i_max_indx = 0
            for j in range(len(self.rate[i])):
                if (self.rate[i][j] > i_max):
                    i_max = self.rate[i][j]
                    i_max_indx = j
            if (i_max > self.cut_value):
                clusters = np.append(list(clusters), i_max_indx + 1).astype(int)
            else:
                clusters = np.append(list(clusters), 0).astype(int)
        return clusters