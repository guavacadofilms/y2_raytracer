import seaborn as sns
import raytracer as rt
import opticalelements as elems
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits import mplot3d

sns.set_theme(style="darkgrid")

# task 12  - trace a bundle of rays for a uniform collimated beam

z0 = 100 # set centre of spherical surface
spherical = elems.SphericalRefraction(z0, 0.03, 1, 1.5, 30)
output = elems.OutputPlane(300)

rays = rt.make_bundle(8)

# create set of 3D axis
# ax = plt.axes(projection="3d")
# ax.set_xlabel("z/mm")
# ax.set_ylabel("x/mm")
# ax.set_zlabel("y/mm")

# propagate each ray through spherical surface onto output plane
# then plot onto either 2D or 3D axes
for ray in rays:
    spherical.propagate_ray(ray)
    output.propagate_ray(ray)
    # ray.three_d_plot(ax)
    ray.plot(2, 0)
plt.show()

# create spot diagram at z=0 plane
for ray in rays:
    ray.spot_diag(0)
plt.show()
