import math
#service clas Vector2D


"""
There won't be any functions for planeStatic class in first beta version
There won't be any differences beetwen "static" and "dinamic" spheres (static a also will update)

"""


class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def norm(self):
        self.x = self.x / abs(self)
        self.y = self.y / abs(self)
        return Vector2D(self.x, self.y)

    def cross(self):
        return Vector2D(-self.y, self.x)

    def rotate(self, angle):
        a0 = math.atan2(self.x, self.y)
        xx = self.x * math.cos(angle) - self.y * math.sin(angle)
        yy = self.y * math.cos(angle) + self.x * math.sin(angle)
        return Vector2D(xx, yy)

    def сross_product(self, other):
        return self.x * other.y - self.y * other.x

    def __repr__(self):
        return 'Vector2D({}, {})'.format(self.x, self.y)

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __ne__(self, other):
        return (self.x, self.y) != (other.x, other.y)

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __rsub__(self, other):
        return other - self

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        return self.x != 0 or self.y != 0

    def __neg__(self):
        return Vector2D(-self.x, -self.y)

    def __mul__(self, other):
        if type(other) is Vector2D:
            return self.x*other.x + self.y*other.y
        return Vector2D(self.x * other, self.y * other)

    def __rmul__(self, other):
        if type(other) is Vector2D:
            return self.x * other.x + self.y * other.y
        return Vector2D(self.x * other, self.y * other)

    def __truediv__(self, other ):
        return Vector2D(self.x / other, self.y / other)

    def __call__(self, x, y):
        self.x, self.y = x, y

    #@property
    def len(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def intpair(self):
        return (int(self.x), int(self.y))
    """
    def __setattr__(self, key, value):
        #print(key, value)
        object.__setattr__(self, key, value)
    """

class PlaneStatic2D:
    """
    point1 and point2 have to be an instance of Vector2D
    """
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        self.direction_vector = self.point1 - self.point2
        self.normal = Vector2D(self.direction_vector.y, -self.direction_vector.x)

    def __repr__(self):
        return 'PlaneStatic2D({}, {}, {})'.format(self.point1, self.point2, self.normal)

    def __str__(self):
        return '({}, {}, {})'.format(self.point1, self.point2, self.normal)

"""
    Base class. Argument pos [position] have to be setted
    pos, vel, acc have to be a specimen of Vector2D class
    pos - position
    vel - velocity
    acc - acceleration
"""
class RigidBody:
    def __init__(self, pos, vel=Vector2D(0, 0), acc=Vector2D(0, 0), mass=1):
        self.pos, self.vel, self.acc = pos, vel, acc
        self.mass = mass
        self.imass = 1/mass


class Sphere(RigidBody):
    def __init__(self,  pos, vel=Vector2D(0, 0), acc=Vector2D(0, 0), mass=1, radius=10):
        super(Sphere, self).__init__(pos, vel, acc, mass)
        self.radius = radius
        self.volume = (4 / 3) * math.pi * self.radius ** 3
        self.dencity = self.mass/self.volume

    def set_volume (self):
        self.volume = (4 / 3) * math.pi * self.radius ** 3

    def set_radius(self, new_radius, const_dencity=True):
        self.radius = new_radius
        self.set_volume()
        if const_dencity is True:
            self.mass = self.dencity * self.volume
            self.imass = 1/self.mass
        else:
            self.dencity = self.mass / self.volume


    def set_mass(self, new_mass, const_dencity=False):
        if new_mass <= 0:
            new_mass = 0.1
        self.mass = new_mass
        self.imass = 1/self.mass
        if const_dencity is False:
            self.dencity = self.mass / self.volume
        else:
            self.volume = self.mass / self.dencity
            self.radius = ((3 / 4) * self.volume / math.pi) ** (1 / 3)

    """@param: new_vel - abs of Vector2D"""
    def set_vel_abs (self, new_vel):
        self.vel = self.vel * (new_vel/abs(self.vel))


    def set_acc_abs(self, new_acc):
        self.acc = self.acc * (new_acc / abs(self.acc))

    def set_dencity(self):
        pass


    def get_kinetic_energy(self):
        return (0.5) * self.mass * abs(self.vel)**2

    """Returns Vector2D impulse"""
    def get_momentum(self):
        return self.mass * self.vel

    def get_potencial_energy(self):
        pass

    def set_pos (self, new_pos):
        if type(new_pos) is Vector2D:
            self.pos.x = new_pos.x
            self.pos.y = new_pos.y
        if type(new_pos) is tuple:
            self.pos.x, self.pos.y = new_pos

    #self < other
    def __lt__(self, other):
        return self.radius < other.radius

    # self <= other
    def __le__(self, other):
        return self.radius <= other.radius

    # self == other
    def __eq__(self, other):
        return self.radius == other.radius

    # self != other
    def __ne__(self, other):
        return self.radius != other.radius

    # self > other
    def __gt__(self, other):
        return self.radius > other.radius

    # self != other
    def __ge__(self, other):
        return self.radius >= other.radius

    def __repr__(self):
        return 'Shere2D({}, {}, {}, {}, {} )'.format(self.pos, self.vel, self.acc, self.mass, self.radius)

    def __str__(self):
        return '(pos{},\n vel{},\n acc{},\n mass: {},\n radius: {},\n dencity: {})\n\n'.format(self.pos, self.vel, self.acc, self.mass, self.radius, self.dencity)

    def __call__(self, pos, vel, acc):
        self.pos, self.vel, self.acc = pos, vel, acc

    def __iter__(self):
        pass

    def apply_impulse(self, contact, normal, impulse):
        self.vel += impulse * normal * self.imass

    def update_vel(self, dt):
        self.vel += self.acc * dt

    def update_pos (self, dt):
        self.pos += self.vel * dt

    def update_acc(self, forse):
        self.acc += forse * self.imass
    """
    update position and velocity
    """


    def update(self, dt, forse=0):
        self.update_acc(forse)
        self.update_vel(dt)
        self.update_pos(dt)


"""
This class contains containers of objects of the class. It used for set physical scene.
You have to create only one intanse of class Scene.
"""
class Scene:

    def __init__(self ):
        self.n_planes = 0
        self.n_spheres = 0
        self.sphere = {}

        self.depth = []
        self.momentum = Vector2D(0, 0)


        self.forse = Vector2D(0, 0)

        self.energy = 0
        # array of index
        # self.l_sphere = []

    def __str__(self):
        str_out = ''
        for i in self.sphere:
            str_out +=  i.__repr__() +' ' + self.sphere[i].__repr__() + '\n'
        return str_out


    def add_sphere(self, pos, vel=Vector2D(0, 0), acc=Vector2D(0, 0), mass=1, radius=10):
        self.sphere[self.n_spheres] = Sphere(pos, vel, acc, mass, radius)
        self.n_spheres += 1
    """Delete the sphere from a dictionary by key"""

    def delete_sphere(self, i):
        self.sphere.pop(i)
        self.n_spheres -= 1

    def vel_relative(self, normal, contact, i, j):
        return   (normal.x * (self.sphere[i].vel.x - self.sphere[j].vel.x) +
                  normal.y * (self.sphere[i].vel.y - self.sphere[j].vel.y))


    # TODO: добавить position_based подход


    #На вход принимает массив индексов сфер из дереве всех сфер
    #То есть те которые будем обрабатывать
    #На выходе список из кортежей пар индексов
    #(пока что проходит просто по дереву)

    """
    self.sphere[col_spheres[i][0]] - second sphere in collision number i
    self.sphere[col_spheres[i][0]] - first sphere in collision number i
    принимает лист из пар индексов
    """
#
    def collision_detection_spheres(self, dt):
        col_spheres = []
        l_i_s = list(self.sphere.keys()) # list_i_)spheres
        d_i_s = {i:l_i_s[i] for i in range(len(l_i_s))}# dict_i_spheres
        
        for i in d_i_s:
            for j in l_i_s[i+1:]:
                depth = ((self.sphere[d_i_s[i]].radius + self.sphere[j].radius) - abs(self.sphere[d_i_s[i]].pos - self.sphere[j].pos))
                if ( depth >= 0 ):
                    """Then collision"""
                    normal = self.calculate_normal(d_i_s[i],j)
                    self.sphere[j].pos += abs(depth + 2)*normal
                    col_spheres.append((d_i_s[i], j))
        return col_spheres

    def calculate_normal(self, i, j):
        n = self.sphere[j].pos - self.sphere[i].pos

        n = n/abs(n)
        return n

    def calculate_contact(self, i, j):
        r1, r2 = self.sphere[i].radius, self.sphere[j].radius

        if (self.sphere[i].pos.x < self.sphere[j].pos.x):
            return self.sphere[i].pos + (r1 / (r1 + r2)) * (self.sphere[j].pos - self.sphere[i].pos)
        else:
            return self.sphere[j].pos + (r2 / (r1 + r2)) * (self.sphere[i].pos - self.sphere[j].pos)


    def calculate_impulse(self, normal, contact, i, j ):
        R1 = contact - self.sphere[i].pos
        R2 = contact - self.sphere[j].pos
        MIN_V = 0
        E = 1

        J = (   normal.x * (normal.x * self.sphere[i].imass + normal.x * self.sphere[j].imass)
              + normal.y * (normal.y * self.sphere[i].imass + normal.y * self.sphere[j].imass) )


        return ( MIN_V - (1 + E) * self.vel_relative(normal,contact, i, j) ) / J

    def collision_response_spheres(self, col_spheres, dt):
        for i in range(0, len(col_spheres)):
            m1 = self.sphere[col_spheres[i][0]].mass
            m2 = self.sphere[col_spheres[i][1]].mass

            contact = self.calculate_contact(col_spheres[i][0], col_spheres[i][1])
            normal =  self.calculate_normal(col_spheres[i][0], col_spheres[i][1])
            impulse = self.calculate_impulse(normal, contact, col_spheres[i][0], col_spheres[i][1])
            self.sphere[col_spheres[i][0]].apply_impulse(contact, normal, impulse)
            self.sphere[col_spheres[i][1]].apply_impulse(contact, normal, -impulse)

    def set_forse(self, forse=0):
        self.forse = forse

    """forse - vector of forse field in scene"""
    def update(self, dt):
        for i in self.sphere:
            self.sphere[i].update(dt, self.forse)

    """Returns Vector2D sum momentum of system"""
    def calculate_momentum (self):
        sum = Vector2D(0,0)
        for i in self.sphere:
            sum += self.sphere[i].get_momentum()
        self.momentum = sum
        return sum

    def calculate_energy(self):
        sum = 0
        for i in self.sphere:
            sum += self.sphere[i].get_kinetic_energy()
        self.energy = sum
        return sum



    #def
    #if (self.collision_detection() != False):

    def set_plane(self):
        pass
