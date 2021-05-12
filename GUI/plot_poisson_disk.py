import poisson_disk.poisson_disc as poi
import matplotlib.pyplot as plt

r = 0.25
data = poi.Bridson_sampling(radius=r)

ax = plt.gca()
for p in data:
    ax.add_patch(plt.Circle(p, r, color='b', fill=False, clip_on=False))
datax, datay = data[:,0], data[:,1]
plt.scatter(datax, datay, s=1, color='k')
ax.set_aspect(1)
plt.show()