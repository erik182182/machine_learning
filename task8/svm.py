import pygame as pg
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm

x = []
y = []
coords = []
clust = []


pg.init()
sc = pg.display.set_mode((600, 400))
sc.fill((255, 255, 255))
pg.display.update()

clock = pg.time.Clock()
fps = 60


flag = True
while flag:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            flag = False
        if i.type == pg.MOUSEBUTTONDOWN:
            if i.button == 1:
                pg.draw.circle(sc, (255, 0, 50), i.pos, 10)
                pg.display.update()
                clust.append(0)
            elif i.button == 3:
                pg.draw.circle(sc, (0, 255, 0), i.pos, 10)
                pg.display.update()
                clust.append(1)
            x.append(i.pos[0])
            y.append(i.pos[1])
            coords.append(i.pos)
        if i.type == pg.KEYDOWN:
            if i.key == pg.K_RIGHT:
                model = svm.SVC(kernel='linear', C=1.0)
                X = np.array(coords)
                Y = np.array(clust)
                model.fit(X, Y)
                m = model.coef0
                w = model.coef_[0]
                n = -w[0] / w[1]
                xx = np.linspace(0, 1000, 1000)
                yy = n * xx - (model.intercept_[0]) / w[1]
                pg.draw.line(sc, (0, 0, 255), (xx[0], yy[0]), (xx[-1], yy[-1]), 2)
                pg.display.update()
                plt.axis([0.0, 600.0, 600.0, 0.0])
                plt.plot(xx, yy, c='r')
                plt.scatter(X[:, 0], X[:, 1], c=Y)
                plt.show()
    clock.tick(fps)