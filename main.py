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

n = [3, 10, 20, 30, 40, 50] # number of evenly-spaced points to create for each circle
spread = 5 # set max. radius of collimated beam to 5mm
spread_range = np.linspace(1, spread, len(n))
print(spread_range)

def make_beam(n, spread_range):
    """Function to create evenly-spaced points on concentric circles.

    Parameters
    ----------
    n : array-like
        List of number of points to generate for each concentric ring
    spread-range : array-like
        List of radii of each concentric circle

    Returns
    -------
    rays : array-like
        Set of rays initialised by the points generated on the circles
        
    """

    rays = []
    for num in n:
        points = np.linspace(0, np.pi * 2, num) # list of n equally-spaced points on a circle
        for i in points:
            x = np.cos(i)
            y = np.sin(i)
            for rad in spread_range:
                pos = [rad * x, rad * y, 0] # initialise position of rays in z = 0 plane
                dir = [0, 0, 1]
                ray = rt.Ray(pos, dir)
                rays.append(ray)
    return rays

# create set of 3D axis
ax = plt.axes(projection="3d")
ax.set_xlabel("z/mm")
ax.set_ylabel("x/mm")
ax.set_zlabel("y/mm")

rays = make_beam(n, spread_range)

# propagate each ray through spherical surface onto output plane
# then plot onto either 2D or 3D axes
for ray in rays:
    spherical.propagate_ray(ray)
    output.propagate_ray(ray)
    ray.three_d_plot(ax, "green")
    # ray.plot(2, 0)

plt.show()
