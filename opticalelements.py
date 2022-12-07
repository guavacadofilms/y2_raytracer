"""
Module containing Optical Element base class, with extended classes
for different types of elements such as spherical surfaces and output planes.
All elements have methods to propagate a ray object through them
"""

import numpy as np


def normalise_vector(vector):
    """Normalise an input vector"""

    if len(vector) != 3:
        raise Exception("Enter 3-D vector as a 3-element array")
    return vector / np.linalg.norm(vector)


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
    """Spherical surface which inherents base class OpticalElemant.
        
    Attributes
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
    
    Methods
    -------
    intercept
        Return point of intercept between optical element and input ray
    snell
        Return direction of refracted ray using Snell's law
    propagate_ray
        Propagate ray through spherical element
    """

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
        """

        rad = self.__radius
        centre = self.__centre

        ray_p = ray.p()
        ray_k_unit = ray.k()

        centre_to_ray = np.subtract(ray_p, centre)  # distance between centre of element and ray (r)
        r_dot_k = np.dot(centre_to_ray, ray_k_unit)  # dot product between r and k
        abs_centre_to_ray = np.linalg.norm(centre_to_ray)  # absolute value of r vector

        # use (-r vector * direction of ray) plus or minus sqrt( (r*k)**2 - (rx + ry + rz) - radius**2 )
        length_one = -r_dot_k + np.sqrt(r_dot_k ** 2 - (abs_centre_to_ray ** 2 - rad ** 2))
        length_two = -r_dot_k - np.sqrt(r_dot_k ** 2 - (abs_centre_to_ray ** 2 - rad ** 2))

        # intercept = ray position + (length * ray direction)
        intercept_one = np.add(ray_p, (length_one * np.array(ray_k_unit)))
        intercept_two = np.add(ray_p, (length_two * np.array(ray_k_unit)))

        dist_one = np.linalg.norm(intercept_one - centre)
        dist_two = np.linalg.norm(intercept_two - centre)

        # check which intercept is valid (within aperture radius and within z0 to centre of element in z-axis)
        # if neither, return None
        for i in (intercept_one, intercept_two):
            x_sqr_plus_y_sqr = i[0] ** 2 + i[1] ** 2
            if x_sqr_plus_y_sqr <= self.__aperturerad ** 2 and self.__zintercept <= i[2] <= centre[2]:
                return i
        return None

    def snell(self, incident_dir, surface_normal):
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
        cross_incident_normal = np.cross(incident_dir, surface_normal)

        # set the normal of the plane which the ray is confined to, as a unit vector
        # if ray is going through centre, set unit axis to 1 to avoid division by 0 error
        # when normalising [0, 0, 0]
        if np.linalg.norm(cross_incident_normal) == 0:
            unit_axis = [0, 0, 1]
        else:
            unit_axis = normalise_vector(cross_incident_normal)

        # use sin^2(x) + cos^2(x) = 1 to calculate sin(x)
        sin_theta_i = np.sqrt(1 - (dot_incident_normal ** 2))
        theta_i = np.arcsin(sin_theta_i)

        # return none if total internal reflection occurs
        if sin_theta_i > (self.__n1 / self.__n2):
            return None

        # calculate angle of refracted ray using Snell's law
        sin_theta_r = (sin_theta_i * self.__n1) / self.__n2
        theta_r = np.arcsin(sin_theta_r)

        # apply rotational matrix to normal unit vector to rotate by the angle of refraction
        # in the plane of the incident angle and normal
        refracted_dir = np.dot(rotation_matrix(-theta_r, unit_axis), (surface_normal))

        return refracted_dir

    def propagate_ray(self, ray):
        """Propagate ray through spherical element

        Parameters
        ----------
        ray :
            Incident ray

        Returns
        -------
        points : array-like
            Set of points which comprise the propagated ray
        """

        intercept_point = self.intercept(ray)

        if intercept_point is None:
            ray.terminate()
            raise NoInterceptError("Ray has no intercept with element")

        # apply snell's law to incident ray
        intercept_to_centre = np.subtract(self.__centre, intercept_point)
        unit_inter_to_centre = normalise_vector(intercept_to_centre)
        refracted_dir = self.snell(ray.k(), unit_inter_to_centre)

        if refracted_dir is None:
            ray.terminate()
            new_k = ray.k()
            ray.append(intercept_point, new_k)
            points = ray.vertices()
            return points

        # update ray position to surface intercept point if refraction occurs
        new_k = refracted_dir
        ray.append(intercept_point, new_k)
        points = ray.vertices()
        return points


class NoInterceptError(Exception):
    pass


class OutputPlane(OpticalElement):
    """Output place at specified z-value which inherents base class OpticalElemant.
        
    Attributes
    ----------
    z0 : float
        Intercept point of surface with the z-axis
    
    Methods
    -------
    intercept
        Calcuate point of intercept between output plane and ray
    propagate_ray
        Update ray position to intercept with output plane
    """

    def __init__(self, z0):
        """Initialise an output plane at a speficied value on z-axis

        Parameters
        ----------
        z0 : float
            Intercept point of surface with the z-axis
        """

        self.__zintercept = z0

    def intercept(self, ray):
        """Calcuate point of intercept between output plane and ray

        Parameters
        ----------
        ray : array-like
            Ray object which is propagated to output plane

        Returns
        -------
        self.__intercept : array-like
            Position at which the ray and plane intercept
        """

        ray_pos = ray.p()
        ray_k = ray.k()

        # use [start position] + n * [direction] = [end position] line equation to find n
        # find end position by using calculated n value
        n = (self.__zintercept - ray_pos[2]) / ray_k[2]
        self.__interceptpoint = np.add(ray_pos, (n * ray_k))
        return self.__interceptpoint

    def propagate_ray(self, ray):
        """Update ray position to intercept with output plane"""

        if ray.is_terminated():
            return ray
        ray.append(self.intercept(ray), ray.k())
        return ray
