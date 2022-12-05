"""
Script to test behaviour of classes, including initialisation of objects and their methods
"""
import seaborn as sns
import raytracer as rt
import opticalelements as elems
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits import mplot3d

sns.set_theme(style="darkgrid")

# task 2 - testing initialization of class object
test_ray = rt.Ray()
print(test_ray)  # str method func
print(test_ray.p(), test_ray.k(), test_ray.vertices())  # return pos, dir, list of points
print(test_ray.append([1, 1, 1], [5, 6, 3]))
new_pos = [2, 2, 2]
new_dir = [8, 5, 4]
print(test_ray.append(new_pos, new_dir))  # append variables in the form [x,y,z]
print(test_ray.vertices())  # ensure list of points updates correctly

# testing raised exceptions when p and k are incorrectly-sized lists
my_pos = [5, 5, 4, 5]
my_dir = [4, 8, 9]
# my_ray = rt.Ray(my_pos, my_dir)
# print(f"my ray:{my_ray}")

# notimplemented error for "propagate ray" method
test_element = elems.OpticalElement()
# print(test_element.propagate_ray(test_ray))

new_ray = rt.Ray([1, 1, 0], [0, 0, 3])
test_spherical = elems.SphericalRefraction(3, 0.5, 1, 1, 2)
print(test_spherical.propagate_ray(new_ray))  # task 3 - inheritance of base class opticalelement
print(
    f"Intercept points of ray and spherical element:\n{test_spherical.intercept(new_ray)}"
)  # task 4 - intercept function

# task 5 - snell's law function
incident_dir = [0, 1, 4]
surface_norm = [0, 2, 1]
unit_incident_dir = elems.normalise_vector(incident_dir)
unit_surface_norm = elems.normalise_vector(surface_norm)
print(f"Refraction direction: {test_spherical.snell(unit_incident_dir, unit_surface_norm)}")

# task 6 + 7 - ntercept and propagate function for spherical element
pos = [0, 0, 0]
dir = [0.1, 0.1, 1]
unit_dir = elems.normalise_vector(dir)
test_ray = rt.Ray(pos, unit_dir)
test_spherical = elems.SphericalRefraction(5, 0.05, 1, 1, 2)
print(test_spherical.propagate_ray(test_ray))

# task 8 - output plane intercept + propagate functions
test_output_plane = elems.OutputPlane(100)
print(test_output_plane.propagate_ray(test_ray))
print(test_ray.vertices())

# ray plot function
# test_ray.plot(2, 1)

# task 9 - example rays through simple spherical surface
z0 = 100
spherical = elems.SphericalRefraction(z0, 0.03, 1, 1.5, 30)
output = elems.OutputPlane(250)

pos = []
rays = []
rays_up = []
rays_down = []
n = 10 
circle = np.linspace(0, np.pi * 2, n) # list of n equally-spaced points on a circle
spread = 10 # set radius of circle

# create n rays initialised on the circumference of the circle
for i in circle:
    x = spread * np.cos(i)
    y = spread * np.sin(i)

    pos = [x, y, 0]
    dir = [0, 0, 1]
    ray = rt.Ray(pos, dir)

    pos_up = [x, y + (z0 / 2), 0]
    dir_up = [0, -0.5, 1]
    ray_up = rt.Ray(pos_up, dir_up)

    pos_down = [x, y - (z0 / 2), 0]
    dir_down = [0, 0.5, 1]
    ray_down = rt.Ray(pos_down, dir_down)

    rays.append(ray)
    rays_up.append(ray_up)
    rays_down.append(ray_down)



# create set of 3D axis
ax = plt.axes(projection="3d")
ax.set_xlabel("z")
ax.set_ylabel("x")
ax.set_zlabel("y")

# propagate each ray through spherical surface onto output plane
# then plot onto either 2D or 3D axes
for ray, ray_up, ray_down in zip(rays, rays_up, rays_down):
    spherical.propagate_ray(ray)
    output.propagate_ray(ray)
    ray.three_d_plot(ax, "green")
    # ray.plot(2, 0)

    spherical.propagate_ray(ray_up)
    output.propagate_ray(ray_up)
    ray_up.three_d_plot(ax, "red")
    # ray.plot(2, 0)

    spherical.propagate_ray(ray_down)
    output.propagate_ray(ray_down)
    ray_down.three_d_plot(ax, "cadetblue")
    # ray.plot(2, 0)

plt.show()
