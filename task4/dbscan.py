import math
import numpy as np
import matplotlib.pyplot as plt


class Point:

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return 'x=' + str(self.x) + ' ' + 'y=' + str(self.y)

    def __eq__(self, o: object) -> bool:
        return self.x == o.x and self.y == o.y

    def __hash__(self) -> int:
        return hash(tuple(self.__dict__.values()))


def get_eps_points(point):
    return [q for q in points if math.sqrt((point.x - q.x) ** 2 + (point.y - q.y) ** 2) < eps]


points = [Point(np.random.randint(low=0, high=100), np.random.randint(low=0, high=200)) for i in range(200)]
points.extend([Point(np.random.randint(low=150, high=400), np.random.randint(low=150, high=250)) for i in range(200)])
points.extend([Point(np.random.randint(low=300, high=400), np.random.randint(low=0, high=150)) for i in range(100)])
points.extend([Point(np.random.randint(low=300, high=400), np.random.randint(low=300, high=400)) for i in range(100)])
points.extend([Point(np.random.randint(low=0, high=400), np.random.randint(low=0, high=400)) for i in range(50)])

eps = 25
minPts = 5

clust_i = 0

visited_points = set()
clustered_points = set()
clusters = {"noise": []}

for point in points:
    if point not in visited_points:
        visited_points.add(point)
        eps_points = get_eps_points(point)
        if len(eps_points) < minPts:
            clusters["noise"].append(point)
        else:
            clust_i += 1
            if clust_i not in clusters:
                clusters[clust_i] = []
            clusters[clust_i].append(point)
            clustered_points.add(point)
            while eps_points:
                q = eps_points.pop()
                if q not in visited_points:
                    visited_points.add(q)
                    new_eps_points = get_eps_points(q)
                    if len(new_eps_points) > minPts:
                        eps_points.extend(new_eps_points)
                if q not in clustered_points:
                    clustered_points.add(q)
                    clusters[clust_i].append(q)
                    if q in clusters["noise"]:
                        clusters["noise"].remove(q)

for points in clusters.values():
    X = [p.x for p in points]
    Y = [p.y for p in points]
    plt.scatter(X, Y, color=np.random.rand(3, ))
plt.show()
