"""
module for optical elements
"""

import numpy as np

def normalise_vector(vector):
    if len(vector) != 3:
        raise Exception("Enter 3-D vector as a 3-element array")
    return vector/np.linalg.norm(vector)

def rotation_matrix(theta, unit_axis):
    """Calculate rotation matrix from angle and axis
    
    Parameters
        ----------
        theta : float
            Angle which vector is rotated by
        unit_axis : array-like
            Direction of axis which vector rotates around, as a unit vector

        Returns
        -------
        rot_matrix :
            Rotational matrix by angle theta around unit_axis
    """
    cos = np.cos(theta)
    sin = np.sin(theta)

    # equation to find rotational matrix from angle and axis, derived from Rodrigues' rotation formula
    identity_matrix = np.identity(3)
    outer_matrix = np.outer(unit_axis, unit_axis)
    cross_prod_matrix = np.cross(unit_axis, identity_matrix * -1)
    rot_matrix = (cos * identity_matrix) + (sin * cross_prod_matrix) + ((1 - cos) * outer_matrix)
    return rot_matrix

class OpticalElement:
    def propagate_ray(self, ray):
        """Propagate a ray through the optical element
    
        Raises
        ------
        NotImplementedError : if called within this class
        """
        raise NotImplementedError()

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

        # calculate radius with 1/curvature
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
        print(f"Radius: {rad}, centre: {centre}")

        ray_p = ray.p()
        ray_k_unit = ray.k() / np.linalg.norm(ray.k())

        # distance between centre of element and ray (r), dist = np.sqrt((ax-bx)^2 + (ay-by)^2 + (az-bz)^2)
        centre_to_ray = np.subtract(ray_p, centre)
        print(f"Vector from centre to ray: {centre_to_ray}")

        # dot product between r and k
        r_dot_k = np.dot(centre_to_ray, ray_k_unit)
        print(f"Dot product of r and k: {r_dot_k}")

        # absolute value of r vector
        abs_centre_to_ray = np.linalg.norm(centre_to_ray)
        print(f"|r|: {abs_centre_to_ray}")

        # use (-r vector * direction of ray) plus or minus sqrt(    (r*k)**2    -    (rx + ry + rz) - radius**2    )
        length_one = -r_dot_k + np.sqrt(r_dot_k ** 2 - (abs_centre_to_ray ** 2 - rad ** 2))
        length_two = -r_dot_k - np.sqrt(r_dot_k ** 2 - (abs_centre_to_ray ** 2 - rad ** 2))
        print(f"length one, {length_one} and length two: {length_two}")

        # intercept = ray position + (length * ray direction)
        intercept_one = np.add(ray_p, (length_one * np.array(ray_k_unit)))
        intercept_two = np.add(ray_p, (length_two * np.array(ray_k_unit)))
        print(f"intercept one: {intercept_one}, intercept two: {intercept_two}")
        print(f"norm of intercept one: {np.linalg.norm(intercept_one)}, norm of intercept two: {np.linalg.norm(intercept_two)}")

        dist_one = np.linalg.norm(intercept_one - centre)
        dist_two = np.linalg.norm(intercept_two - centre)
        print(f"distance one: {dist_one}, distance two: {dist_two}")

        # check which intercept is valid (within aperture radius and within z0 to centre of element in z-axis)
        # if neither, return None
        for i in (intercept_one, intercept_two):
            x_sqr_plus_y_sqr = (i[0] ** 2 + i[1] ** 2)
            print(f"x squared + y squared: {x_sqr_plus_y_sqr}")
            if x_sqr_plus_y_sqr <= self.__aperturerad ** 2 and self.__zintercept <= i[2] <= centre[2]:
                return i
        return None
   
    def snell(self,incident_dir,surface_normal):
        """Calcuate direction of refracted ray using Snell's law

        Parameters
        ----------
        incident_dir : array-like
            Direction of incident ray as unit vector
        surface_normal : array-like
            Surface normal as unit vector

        Returns
        -------
        refracted_dir : array-like
            Direction of refracted ray as a unit vector
        None :
            If ray is subject to total internal reflection
        """

        # dot product of a and b = |a| * |b| * cos(theta)
        # since |a| and |b| are both 1, dot product of a and b = cos(theta)
        # using 1 = sin^2 + cos^2, can rearrange to sin(theta) = sqrt(1 - cos^2(theta))
        dot_incident_normal = np.dot(incident_dir, surface_normal)
        print(f"{dot_incident_normal = }")
        cross_incident_normal = np.cross(incident_dir, surface_normal)
        print(f"{cross_incident_normal = }")

        # set the normal of the plane which the ray is confined to, as a unit vector
        if np.linalg.norm(cross_incident_normal) == 0:
            unit_axis = [0, 0, 1]
        else:
            unit_axis = normalise_vector(cross_incident_normal)
        print(f"{unit_axis = }")

        # use sin^2(x) + cos^2(x) = 1 to calculate sin(x)
        sin_theta_i = np.sqrt(1 - (dot_incident_normal ** 2))
        theta_i = np.arcsin(sin_theta_i)
        print(f"sin of incident theta: {sin_theta_i}")
        print(f"incident angle: {theta_i}")

        # return none if total internal reflection occurs
        if sin_theta_i > (self.__n1 / self.__n2):
            return None
        
        # calculate angle of refracted ray using Snell's law
        sin_theta_r = (sin_theta_i * self.__n1) / self.__n2
        theta_r = np.arcsin(sin_theta_r)
        print(f"sin of refracted theta: {sin_theta_r}")
        print(f"refracted angle: {theta_r}")
        
        # apply rotational matrix to normal unit vector to rotate by the angle of refraction
        # in the plane of the incident angle and normal
        refracted_dir = np.dot(rotation_matrix(-theta_r, unit_axis), (surface_normal))
        print(rotation_matrix(theta_r, surface_normal))

        return refracted_dir
        
    def propagate_ray(self, ray):
        """Propagate ray through spherical element

        Parameters
        ----------
        ray :
            Incident ray

        Returns
        -------
        ray.vertices() : array-like
            Set of points which comprise the propagated ray
        terminate_msg :
            If ray has no valid intercept or is subject to total internal reflection
        """

        intercept_point = self.intercept(ray)
        print(intercept_point)

        if intercept_point is None:
            ray.terminate()
            raise NoInterceptError("Ray has no intercept with element")

        intercept_to_centre = np.subtract(intercept_point, self.__centre)
        unit_inter_to_centre = normalise_vector(intercept_to_centre)
        refracted_dir = self.snell(ray.k(), unit_inter_to_centre)

        if refracted_dir is None:
            ray.terminate()
            raise NoInterceptError("Ray is subject to total internal refraction")

        ray.append(intercept_point, refracted_dir)
        points = ray.vertices()
        return points

class NoInterceptError(Exception):
    pass

class OutputPlane(OpticalElement):
    def __init__(self, z0):
        self.__zintercept = z0

    def intercept(self, ray):
        ray_pos = ray.p()
        ray_k = ray.k()
        idk = (self.__zintercept - ray_pos[2]) / ray_k[2]
        print(f"{ray_k = }")
        print(f"{idk = }")
        self.__interceptpoint = np.add(ray_pos, (idk * ray_k))
        return self.__interceptpoint

    def propagate_ray(self, ray):
        ray.append(self.intercept(ray), ray.k())
        return ray
        

