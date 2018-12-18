import attr


@attr.s
class Vector(object):
    x = attr.ib()
    y = attr.ib()
    z = attr.ib()

    def get_tuple(self):
        return self.x, self.y, self.z
