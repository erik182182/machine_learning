import plotly.graph_objects as go
import numpy as np
from sklearn.cluster import KMeans
from sklearn.svm import SVC

def train(f, titles, weights, parameter, count):
    for i in range(count):
        weights = update(f, titles, weights, parameter)
    return weights

def update(d, titles, weights, param):
    p = 1 / (1 + np.dot(d, weights))
    gr = np.dot(np.transpose(d), p - titles)
    gr /= len(d)
    gr *= param
    weights -= gr
    return weights

n = 100
x = np.random.randint(0, 100, n + 1)
y = np.random.randint(0, 100, n + 1)
z = np.random.randint(0, 100, n + 1)


#отрисовка точек
points = []
for i in range(n):
    points.append([x[i], y[i], z[i]])
kmeans = KMeans(n_clusters=2, random_state=0).fit(points)
clusters = kmeans.labels_
colors = ['red'] * n
for i in range(n):
    if clusters[i] == 1:
        colors[i] = 'blue'
fig = go.Figure(data=[go.Scatter3d(x=x, y=y, z=z, mode='markers',
                                   marker=dict(color=colors))])
fig.show()


# svc
svc = SVC(kernel='linear')
svc.fit(points[:n],clusters)

zz = lambda x,y: (-svc.intercept_[0]-svc.coef_[0][0]*x-svc.coef_[0][1]*y) / svc.coef_[0][2]

tmp = np.linspace(0,100,50)
xx,yx = np.meshgrid(tmp,tmp)

fig.add_trace(go.Surface(x=xx,y=yx,z=zz(xx,yx)))
fig.show()

x_new=np.random.randint(0,100)
y_new=np.random.randint(0,100)
z_new=np.random.randint(0,100)
points.append([x_new,y_new,z_new])

x[len(x)-1]=x_new
y[len(y)-1]=y_new
z[len(z)-1]=z_new
colors.append('green')


p = train(points[:(len(points) - 1)], clusters, [0, 0, 0], 0.001, 5000)
new_point = points[(len(points)-1)]
print(new_point)

predict_point_coords = 1 / (1 + np.dot(points, p))[(len(points)-1)] * 100
print(predict_point_coords)

if(predict_point_coords >= 0.5):
        predict_point_cluster = 'blue'
else:
    predict_point_cluster = 'red'
print(predict_point_cluster)