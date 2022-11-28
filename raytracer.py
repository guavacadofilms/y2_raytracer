"""
module containing Ray class
"""

import numpy as np


class Ray:
    """class for a Ray object"""

    def __init__(self, point=[0,0,0], direction=[0,0,0]): #initialises a Ray object with a point and direction at the origin
        """Initialise a ray object

        Parameters
        ----------
        point : array-like, default=[0,0,0]
            Sets current position of ray in 3D cartesian co-ordinate space
        direction : array-like, default=[0,0,0]
            Sets current direction of ray in 3D cartesian co-ordinate space

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
        self.__dir = direction
        self.__allpos = [np.array(point)]
      

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

    def append(self,new_p,new_k):
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
            raise Exception("new point must have 3 elements (x,y,z co-ordinates")
        if len(new_k) != 3:
            raise Exception("new direction must have 3 elements (x,y,z co-ordinates")
        self.__pos = new_p
        self.__dir = new_k
        self.__allpos = np.append(self.__allpos,[self.__pos],axis=0)
        return f"New point: {self.__pos}; new direction: {self.__dir}"
        

    def vertices(self): 
        """Return array of all points comprising a ray"""
        return f"Array of all points: {self.__allpos}"


        
        