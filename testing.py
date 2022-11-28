"""
script to test behaviour of classes, including method functions and initialisation of objects
"""
import raytracer as rt
import opticalelements as elems

test_ray = rt.Ray()  # testing initialization of class object
print(test_ray)  # str method func
print(
    test_ray.p(), test_ray.k(), test_ray.vertices()
)  # return pos, dir, list of points
print(test_ray.append([1, 1, 1], [5, 6, 3]))
new_pos = [2, 2, 2]
new_dir = [8, 5, 4]
print(test_ray.append(new_pos, new_dir))  # append variables in the form [x,y,z]
print(test_ray.vertices())  # ensure list of points updates correctly

my_pos = [5, 5, 4]
my_dir = [4, 8, 9]
my_ray = rt.Ray(
    my_pos, my_dir
)  # testing raised exceptions when p and k are incorrectly-sized lists
print(f"my ray:{my_ray}")

test_element = elems.OpticalElement()
print(
    test_element.propagate_ray(test_ray)
)  # testing notimplemented error for "propagate ray" method

new_ray = rt.Ray([1, 2, 2], [-1, -3, 4])
test_spherical = elems.SphericalRefraction(3, 0.5, 1, 1, 2)
print(
    test_spherical.propagate_ray(new_ray)
)  # testing inheritance of base class opticalelement
print(
    f"Intercept points of ray and spherical element:\n{test_spherical.intercept(new_ray)}"
)  # testing intercept function
