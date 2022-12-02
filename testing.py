"""
script to test behaviour of classes, including method functions and initialisation of objects
"""
import raytracer as rt
import opticalelements as elems
import numpy as np


# testing initialization of class object
# test_ray = rt.Ray()  
# print(test_ray)  # str method func
# print(test_ray.p(), test_ray.k(), test_ray.vertices())  # return pos, dir, list of points
# print(test_ray.append([1, 1, 1], [5, 6, 3]))
# new_pos = [2, 2, 2]
# new_dir = [8, 5, 4]
# print(test_ray.append(new_pos, new_dir))  # append variables in the form [x,y,z]
# print(test_ray.vertices())  # ensure list of points updates correctly

# testing raised exceptions when p and k are incorrectly-sized lists
# my_pos = [5, 5, 4, 3]
# my_dir = [4, 8, 9]
# my_ray = rt.Ray(my_pos, my_dir)  
# print(f"my ray:{my_ray}")

# # testing notimplemented error for "propagate ray" method
# test_element = elems.OpticalElement()
# #print(test_element.propagate_ray(test_ray)) 

# new_ray = rt.Ray([1, 1, 0], [0, 0, 3])
# test_spherical = elems.SphericalRefraction(3, 0.5, 1, 1, 2)
# #print(test_spherical.propagate_ray(new_ray))  # testing inheritance of base class opticalelement
# print(
#     f"Intercept points of ray and spherical element:\n{test_spherical.intercept(new_ray)}"
# )  # testing intercept function

# # testing snell's law function
# incident_dir = [0, 1, 4]
# surface_norm = [0, 2, 1]
# unit_incident_dir = elems.normalise_vector(incident_dir)
# unit_surface_norm = elems.normalise_vector(surface_norm)
# print(f"Refraction direction: {test_spherical.snell(unit_incident_dir, unit_surface_norm)}")

# testing propagate function for spherical element
pos = [1, 1, 1]
dir = [0, 0, 1]
test_ray = rt.Ray(pos, dir)
test_spherical = elems.SphericalRefraction(3, 0.5, 1, 1, 2)
test_spherical.intercept(test_ray)
test_spherical.propagate_ray(test_ray)

print(test_spherical.intercept(test_ray))
print(test_spherical.propagate_ray(test_ray))

test_output_plane = elems.OutputPlane(100)
print(test_output_plane.propagate_ray(test_ray))