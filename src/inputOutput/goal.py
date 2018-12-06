import numpy
import math
from algo.geometry import segmentLineIntersection


class Goal(object):
    def __init__(self, data, field_limits):
        mandatory_keys = ["posts", "direction"]
        self.field_limits = field_limits
        for key in mandatory_keys:
            if key not in data:
                raise ValueError("Cannot find '" + key + "'")
        self.posts = numpy.array(data["posts"]).transpose()
        self.direction = numpy.array(data["direction"])
        if self.posts.shape != (2, 2):
            raise ValueError("Invalid shape for 'posts': "
                             + str(self.field_limits.shape) + " expecting (2, 2)")
        if self.direction.shape != (2,):
            raise ValueError("Invalid shape for 'direction': "
                             + str(self.direction.shape) + " expecting (2,)")

    """ Return None if kick cannot score a goal, otherwise return intersection with the goal """

    def kickResult(self, pos, theta):
        # Checking that ball is not coming from behind the goal
        kickDir = numpy.array([math.cos(theta), math.sin(theta)])
        if kickDir.dot(self.direction) <= 0:
            return None
        return segmentLineIntersection(self.posts[:, 0], self.posts[:, 1],
                                       pos, pos + kickDir)
