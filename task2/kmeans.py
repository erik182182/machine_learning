import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


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


def get_centers(points: [], k: int) -> []:
    max_distance: float = 0

    center_points = []

    point_a: Point = None
    point_b: Point = None

    for i in range(0, len(points)):
        point2 = points[i]
        for j in range(i + 1, len(points)):
            point1 = points[j]
            distance = np.math.sqrt(pow((point2.x - point1.x), 2) + pow((point2.y - point1.y), 2))
            if distance > max_distance:
                max_distance = distance
                point_a = point2
                point_b = point1

    center_points.append(point_a)
    center_points.append(point_b)

    points.remove(point_a)
    points.remove(point_b)

    for i in range(0, k - len(center_points)):
        max_distance = 0
        new_center_point = None

        for j in range(0, len(points)):
            point2 = points[j]
            min_distance = 0
            for q in range(0, len(center_points)):
                point1 = center_points[q]
                distance = np.math.sqrt(pow((point2.x - point1.x), 2) + pow((point2.y - point1.y), 2))
                if min_distance == 0 or distance < min_distance:
                    min_distance = distance

            if max_distance < min_distance:
                max_distance = min_distance
                new_center_point = point2
        center_points.append(new_center_point)
        points.remove(new_center_point)
    return center_points

# соотносит точки и центроиды кластеров
def create_cluster_by_points(points: [], center_points: []) -> {}:
    clusters = {}
    for point in points:
        min_distance_to_center_point = 0
        cluster = None

        for center_point in center_points:
            distance = np.math.sqrt(pow((point.x - center_point.x), 2) + pow((point.y - center_point.y), 2))
            if min_distance_to_center_point == 0 or distance < min_distance_to_center_point:
                min_distance_to_center_point = distance
                cluster = center_point

        cluster_points = clusters.get(cluster) if clusters.get(cluster) is not None else []
        cluster_points.append(point)
        clusters.update({cluster: cluster_points})

    return clusters

# возвращает пересчитанные центроиды кластеров
def new_centers(clusters: {}) -> []:
    cluster_center_points = clusters.keys()
    new_cluster_center = []
    for cluster_center_point in cluster_center_points:
        cluster_points = clusters.get(cluster_center_point)
        center_x = 0
        center_y = 0
        for cluster_point in cluster_points:
            center_x += cluster_point.x
            center_y += cluster_point.y

        center_x = center_x / len(cluster_points)
        center_y = center_y / len(cluster_points)
        new_cluster_center.append(Point(x=center_x, y=center_y))

    return new_cluster_center

# возвращает итоговый объект кластера. центроиды:точки
def get_cluster(points: [], k: int) -> {}:
    center = get_centers(points.copy(), k)

    clusters = create_cluster_by_points(points.copy(), center.copy())
    new_center = new_centers(clusters)
    while center != new_center:
        clusters = create_cluster_by_points(points.copy(), new_center.copy())
        center = new_center
        new_center = new_centers(clusters)
    return clusters


# создание точек
count = 100
x = np.random.randint(low=0, high=100, size=count)
y = np.random.randint(low=0, high=100, size=count)

points = []

for i in range(0, count):
    point: Point = Point(x=x[i], y=y[i])
    points.append(point)

# создание кластеров для каждого значения k и сравнение
sum_distance = 0
max_cluster_count = 10
k = 2
best_cluster = {}

cluster_distance = [None] * max_cluster_count
clusters_k = [None] * max_cluster_count
cluster_rel_distance = [None] * max_cluster_count
while k < max_cluster_count:
    clusters_k[k] = get_cluster(points.copy(), k)
    # рассчет расстояних от всех точек до центров кластеров
    cluster_center_points = clusters_k[k].keys()
    distance = 0
    for cluster_center_point in cluster_center_points:
        cluster_points = clusters_k[k].get(cluster_center_point)
        point2 = cluster_center_point
        for point1 in cluster_points:
            distance += np.math.sqrt(pow((point2.x - point1.x), 2) + pow((point2.y - point1.y), 2))
    cluster_distance[k] = distance
    if k > 3:
        cluster_rel_distance[k - 1] = np.math.fabs(cluster_distance[k - 1] - cluster_distance[k]) / np.math.fabs(
            cluster_distance[k - 2] - cluster_distance[k - 1])
    sum_distance = distance
    k += 1

# нахождение оптимального значения k
index = cluster_rel_distance.index(min([i for i in cluster_rel_distance if i is not None]))
best_cluster = clusters_k[index]


# отрисовка точек и кластеров 
for center in best_cluster.keys():
    points = best_cluster.get(center)
    x = []
    y = []
    for point in points:
        x.append(point.x)
        y.append(point.y)

    plt.scatter(x, y, color=np.random.rand(3, ))
    plt.scatter(center.x, center.y, color="red", s=150)

    plt.xlabel('X')
    plt.ylabel('Y')

    patch = mpatches.Patch(color='blue', label='Лучшее значение кластеров: k=' + str(index))
    plt.legend(handles=[patch])

plt.show()
