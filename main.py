import seaborn as sns
import raytracer as rt
import opticalelements as elems
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits import mplot3d

sns.set_theme(style="darkgrid")

####################################################

# task 12  - trace a bundle of rays for a uniform collimated beam

z0 = 100  # set centre of spherical surface
spherical = elems.SphericalRefraction(z0, 0.03, 1, 1.5, 30)
output = elems.OutputPlane(200)

rays = rt.make_bundle(5)

# ax = rt.make_3d_axis()  # uncomment to create set of 3D axis

# propagate each ray through spherical surface onto output plane
# then plot onto either 2D or 3D axes

for ray in rays:
    spherical.propagate_ray(ray)
    output.propagate_ray(ray)
    # ray.three_d_plot(ax) (uncomment to plot in 3D)
    ray.plot(2, 0)
plt.show()

####################################################

# task 13 - create spot diagram at z=200 plane
for ray in rays:
    ray.spot_diag(2)
plt.show()

# calculate RMS spot radius
rms = rt.rms_radius(rays)
print("Geometric spot size:", rms)

####################################################

# task 14 - compare to diffraction limit

d = 10  # diameter of input beam in mm
f = 100  # paraxial focal length of spherical surface
wavelength = 588e-6
theta = 0.10016742116155995
NA = np.sin(theta)  # numerical aperture
d_lim = (1.22 * wavelength) / (2 * NA)  # radius of airy disk
print("Diffraction limit:", d_lim)

####################################################

# task 15 - plano-convex lens

# first, convex surface facing the input
convex_surface = elems.SphericalRefraction(10, 0.02, 1, 1.5168, 40)
plane_surface = elems.PlaneRefraction(15, 1.5168, 1, 40)
output = elems.OutputPlane(200)

ax = rt.make_3d_axis()  # uncomment to create set of 3D axis

# estimate position of paraxial focus
bundle = rt.paraxial_bundle(11, 0.1)
for ray in bundle:
    convex_surface.propagate_ray(ray)
    plane_surface.propagate_ray(ray)
    output.propagate_ray(ray)
    ray.three_d_plot(ax)  # (uncomment to plot in 3D)
    # ray.plot(2, 0) # (uncomment to plot in 2D)
plt.show()

# paraxial focus is at z=108.5
# centre of lens is 12.5
# therefore paraxial focus of lens is 108.45-12.5 = 95.95
print("Paraxial focus is estimated to be:", 95.95)

# propagate bundle of rays (diameter 10mm) through lens
ax = rt.make_3d_axis()  # uncomment to create set of 3D axis

large_bundle = rt.make_bundle(5)
output = elems.OutputPlane(108.45)
for ray in large_bundle:
    convex_surface.propagate_ray(ray)
    plane_surface.propagate_ray(ray)
    output.propagate_ray(ray)
    ray.three_d_plot(ax)  # (uncomment to plot in 3D)
    # ray.plot(2, 0) # (uncomment to plot in 2D)
plt.show()

# spot diagram at paraxial focus (108.45mm)

for ray in large_bundle:
    ray.spot_diag(3)
plt.show()

# calculate RMS spot radius
rms = rt.rms_radius(large_bundle)
print("Geometric spot size, convex facing ray:", rms)

# compare to diffraction limit
d = 10  # diameter of input beam in mm
f = 95.95  # paraxial focal length of plano-convex lens
wavelength = 588e-6
theta = 0.051874518253259796
NA = np.sin(theta)  # numerical aperture
d_lim = (1.22 * wavelength) / (2 * NA)  # radius of airy disk
print("Diffraction limit:", d_lim)

############### - now, plane facing input - #######################

plane_surface = elems.PlaneRefraction(10, 1, 1.5168, 40)
convex_surface = elems.SphericalRefraction(15, -0.02, 1.5168, 1, 40)
output = elems.OutputPlane(200)

# ax = rt.make_3d_axis() # uncomment to create set of 3D axis

# estimate position of paraxial focus
bundle = rt.paraxial_bundle(11, 0.1)
for ray in bundle:
    plane_surface.propagate_ray(ray)
    convex_surface.propagate_ray(ray)
    output.propagate_ray(ray)
    # ray.three_d_plot(ax) # (uncomment to plot in 3D)
    ray.plot(2, 0)  # (uncomment to plot in 2D)
plt.show()

# paraxial focus is at z=111.75
# centre of lens is 12.5
# therefore paraxial focus of lens is 111.75-12.5 = 99.25
print("Paraxial focus is estimated to be:", 99.25)

# propagate bundle of rays (diameter 10mm) through lens
ax = rt.make_3d_axis()  # uncomment to create set of 3D axis

large_bundle = rt.make_bundle(5)
output = elems.OutputPlane(111.75)
for ray in large_bundle:
    plane_surface.propagate_ray(ray)
    convex_surface.propagate_ray(ray)
    output.propagate_ray(ray)
    ray.three_d_plot(ax)  # (uncomment to plot in 3D)
    # ray.plot(2, 0) # (uncomment to plot in 2D)
plt.show()

# spot diagram at paraxial focus (111.75mm)

for ray in large_bundle:
    ray.spot_diag(3)
plt.show()

# calculate RMS spot radius
rms = rt.rms_radius(large_bundle)
print("Geometric spot size, plane facing ray:", rms)

# compare to diffraction limit
d = 10  # diameter of input beam in mm
f = 99.25  # paraxial focal length of plano-convex lens
wavelength = 588e-6
theta = 0.1522677177196473
NA = np.sin(theta)  # numerical aperture
d_lim = (1.22 * wavelength) / (2 * NA)  # radius of airy disk
print("Diffraction limit:", d_lim)
