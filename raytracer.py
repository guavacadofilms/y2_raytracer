"""
Module containing Ray class, with methods such as updating its postion and direction,
as well as plotting in both 2D and 3D space
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d


class Ray:
    """Ray object constructed as a line in 3D euclidian space.
        
    Attributes
    ----------
    point : array-like
        Position of ray as 3D vector
    direction : array-like
        Direction of ray as 3D vector
    
    Methods
    -------
    p
        Returns current position
    k
        Returns current direction
    append
        Updates current position and direction of ray
    vertices
        Returns all points comprising ray
    terminate
        Mark the ray as terminated
    is_terminated
        Check whether ray is terminated
    plot
        Plot all points in a ray in two specified dimensions
    three_d_plot
        Plot all points in a ray in three dimensions
    """

    def __init__(self, point=[0, 0, 0], direction=[0, 0, 1]):
        """Initialise a ray object

        Parameters
        ----------
        point : array-like, default=[0,0,0]
            Sets current position of ray
        direction : array-like, default=[0,0,1]
            Sets current direction of ray

        Raises
        ------
        Exception
            If input point is not a 3-element array
        Exception
            If input direction is not a 3-element array
        """

        if len(point) != 3:
            raise Exception("point must have 3 elements (x,y,z co-ordinates")
        if len(direction) != 3:
            raise Exception("direction must have 3 elements (x,y,z co-ordinates")

        self.__pos = point
        self.__dir = direction / np.linalg.norm(direction)  # normalise direction vector
        self.__allpos = [np.array(point)]
        self.__terminated = False

    def __repr__(self):
        return f"Ray(point=array{self.__pos}, direction=array({self.__dir}))"

    def __str__(self):
        return f"{self.__pos},{self.__dir}"

    def p(self):
        """Returns current position of ray"""
        return self.__pos

    def k(self):
        """Returns current direction of ray"""
        return self.__dir

    def append(self, new_p, new_k):
        """Update ray with new values for position + direction

        Parameters
        ----------
        new_p : array-like
            New position as 3-element array
        new_k : array-like
            New direction as 3-element array
        
        Returns
        -------
        self.__pos : array-like
            New point
        self.__dir : array-like
            New Direction

        Raises
        ------
        Exception
            If new point is not a 3-element array
        Exception
            If new direction is not a 3-element array
        """

        if len(new_p) != 3:
            raise Exception("new point must have 3 elements (x,y,z co-ordinates)")
        if len(new_k) != 3:
            raise Exception("new direction must have 3 elements (x,y,z co-ordinates)")

        self.__pos = new_p
        self.__dir = new_k / np.linalg.norm(new_k)
        self.__allpos = np.append(self.__allpos, [self.__pos], axis=0)

        return f"New point: {self.__pos}; new direction: {self.__dir}"

    def vertices(self):
        """Return array of all points comprising a ray"""
        return self.__allpos

    def terminate(self):
        self.__terminated = True

    def is_terminated(self):
        return self.__terminated

    def plot(self, axis_one, axis_two, colour = "cadetblue"):
        points = self.vertices()
        coords = ["x/mm", "y/mm", "z/mm"]
        array_one = points[:, axis_one]
        array_two = points[:, axis_two]
        plt.plot(array_one, array_two, colour)
        plt.xlabel(coords[axis_one])
        plt.ylabel(coords[axis_two])

    def three_d_plot(self, ax, colour = "cadetblue"):
        points = self.vertices()
        x = points[:, 2]
        y = points[:, 0]
        z = points[:, 1]
        ax.plot(x, y, z, colour)

    def spot_diag(self, index, colour = "cadetblue"):
        points = self.vertices()
        x = points[index, 0]
        y = points[index, 1]
        plt.scatter(x, y, c = colour)
        plt.xlabel("x/mm")
        plt.ylabel("y/mm")

def make_bundle(max_rad):
    """Function to create evenly-spaced points on concentric circles.

    Parameters
    ----------
    max_rad : int
        Radius of bundle

    Returns
    -------
    rays : array-like
        Set of rays initialised by the points generated on the circles
        
    """

    rays = []
    spread = max_rad # set max. radius of collimated beam
    integers = range(1, spread + 1)
    rings = 6 * np.array(integers) # number of evenly-spaced points to create for each circle
    spread_range = np.linspace(0, spread, len(rings) + 1)[1:] # array for the radii of each ring
    
    for a in range(len(spread_range)): # for each ring...
        spread = spread_range[a] # set radius
        ring = rings[a] # set no. of points on the ring
        angles = np.linspace(0, np.pi * 2, ring) # create list of evenly-spaced angles
        
        # create x and y position for each point on the ring
        for b in angles: 
            x = spread * np.cos(b)
            y = spread * np.sin(b)
            pos = [x, y, 0]
            dir = [0, 0, 1]
            ray = Ray(pos, dir)
            rays.append(ray)

    rays.append(Ray([0, 0, 0], [0, 0, 1])) # add central ray at origin
    return rays

def rms_radius(array):
    radii_sq = []
    for ray in array:
        ray_pos = ray.p()
        x = ray_pos[0]
        y = ray_pos[1]
        rad_sq = (x ** 2) + (y ** 2)
        radii_sq.append(rad_sq)
    mean_sq = np.mean(radii_sq)
    rms = np.sqrt(mean_sq)
    return rms

def paraxial_bundle(n, rad):
    rays = []
    circle = np.linspace(0, np.pi * 2, n)
    spread = rad 
    z = 0

    for i in circle:
        x = spread * np.cos(i)
        y = spread * np.sin(i)

        pos = [x, y, z]
        dir = [0, 0, 1]
        ray = Ray(pos, dir)
        rays.append(ray)
    return rays

def make_3d_axis():
    ax = plt.axes(projection="3d")
    ax.set_xlabel("z/mm")
    ax.set_ylabel("x/mm")
    ax.set_zlabel("y/mm")
    return ax