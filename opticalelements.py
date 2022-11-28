"""
module for optical elements
"""

import numpy as np


class OpticalElement:
    def propagate_ray(self, ray):
        """Propagate a ray through the optical element
    
        Raises
        ------
        NotImplementedError : if called.
        """
        return 2

    # raise NotImplementedError()


class SphericalRefraction(OpticalElement):
    def __init__(self, z0, curve, n1, n2, rad):
        """Initialise a spherical optical element with radius and centre point

        Parameters
        ----------
        z0 : float
            Intercept point of surface with the z-axis
        curve : float
            Curvature of surface
        n1 : int
            Refractive index outside surface
        n2 : int
            Refractive index inside surface
        rad : float
            Maximum extent of surface from optical axis
        """

        self.__zintercept = z0
        self.__curvature = curve
        self.__n1 = n1
        self.__n2 = n2
        self.__aperturerad = rad
        # caculate radius with 1/curvature
        # calculate centre point of element as z0 + radius in z-direction
        if self.__curvature == 0:
            self.__radius = np.infty
            self.__centre = [0, 0, self.__zintercept]
        else:
            self.__radius = 1 / self.__curvature
            self.__centre = [0, 0, self.__zintercept + self.__radius]

    def intercept(self, ray):
        """Calcuate point of intercept between optical element and input ray

        Parameters
        ----------
        ray : array-like
            Ray object which is intercepting with element

        Returns
        -------
        intercept : array-like
            First valid position at which the ray and element intercept
        None :
            If there are no valid intercepts

        Raises
        ------
        Exception
            If input is not a ray object
        """

        rad = self.__radius
        centre = self.__centre
        ray_p = ray.p()
        ray_k = ray.k()

        # distance between origin and point (r), dist = np.sqrt((ax-bx)^2 + (ay-by)^2 + (az-bz)^2)
        centre_to_ray = np.array(
            [(ray_p[0] - centre[0]), (ray_p[1] - centre[1]), (ray_p[2] - centre[2])]
        )
        print(f"Vector from centre to ray: {centre_to_ray}")

        # dot product between r and k
        r_dot_k = np.dot(centre_to_ray, ray_k)
        print(f"Dot product of r and k: {r_dot_k}")

        # absolute value of r vector
        abs_centre_to_ray = np.sqrt(
            centre_to_ray[0] ** 2 + centre_to_ray[1] ** 2 + centre_to_ray[2] ** 2
        )
        print(np.absolute(centre_to_ray))
        print(abs_centre_to_ray)

        # use (-r vector * direction of ray) plus or minus sqrt(    (r*k)**2    -    (rx + ry + rz) - radius**2    )
        length_one = -r_dot_k + np.sqrt(
            r_dot_k ** 2 - (abs_centre_to_ray ** 2 - rad ** 2)
        )
        length_two = -r_dot_k - np.sqrt(
            r_dot_k ** 2 - (abs_centre_to_ray ** 2 - rad ** 2)
        )
        print(f"length one, {length_one} and length two: {length_two}")

        # intercept = ray position + (length * ray direction)
        intercept_one = np.add(ray_p, (length_one * np.array(ray_k)))
        intercept_two = np.add(ray_p, (length_two * np.array(ray_k)))

        dist_one = np.linalg.norm(intercept_one - centre)
        dist_two = np.linalg.norm(intercept_two - centre)
        print(f"distance one: {dist_one}, distance two: {dist_two}")

        # check which intercept is valid (within aperture radius)
        # if neither, return "None"
        for i in (intercept_one, intercept_two):
            if i[0] <= self.__aperturerad and i[1] <= self.__aperturerad:
                return i
        return None
