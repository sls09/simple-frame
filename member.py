class Member:
    """An generic object of frame member. It can be a beam, a column or a beam-column,
    A member class represents an isolated member in equilibrium"""


    inc = 0 #Increment at which the ordinates of SFD and BMD will be calculated
    sections = [] #List of all the section for SFD and BMD from 0 to s
    s = 0 #Span length
    p = 0 #Point load
    x = 0 #Location of point-load from member's origin
    w1 = 0 #Load intensity, it should be zero for UVL and equal to w2 for UDL
    w2 = 0 #Load intensity, it should be zero for UVL and equal to w1 for UDL
    l = 0 #Length of load intensity

    '''In order to keep the program simple the point load can move from [0-s]. However, the 
    load intensity "if present" must start from origin and cannot be entirely moved.
    Only the w2 part of the load intensity can be moved toward or away from the w1'''

    A1 = 0 #Axial reaction at bottom, +ve if pointing upward
    A2 = 0 #Axial reaction at tob, +ve if pointing downward
    T1 = 0 #Transverse reaction at bottom, +ve if pointing right
    T2 = 0 #Transverse reaction at top, +ve if pointing left
    M1 = 0 #Moment at bottom, +ve if clockwise
    M2 = 0 #Moment at top, +ve if counter clockwise

    '''The sign conventions are just for the sake of consistency,
    and has no effects on the final results''' 

    def __init__(self, s: float, p: float, x: float, w1: float, w2: float, l: float):
        """Default constructor for initializing member's data i.e. s, p, x, w1, w2, l"""
        self.s = s
        self.p = p
        self.x = x
        self.w1 = w1
        self.w2 = w2
        self.l = l

        if s <= 0:
            raise Exception("Sorry, member span cannot be less than or equal to zero")

        self.sections = [0.0]
        inc = 0.001 * self.s
        while self.sections[-1] < self.s:
            self.sections.append(round(self.sections[-1]+inc, 2))

    def end_reactions(self, end_actions):
        """This methods takes a list as an argument containing the one end reactions i.e. [A1, T1, M1]
        and calculates the other end reactions of the member in the form of list i.e. [A2, T2, M2]"""

        self.A1 = A1 = end_actions[0]
        self.T1 = T1 = end_actions[1]
        self.M1 = M1 = end_actions[2]

        self.A2 = A1
        self.T2 = -T1 + self.p + self.res(self.l, self.w1, self.w2)
        self.M2 = M1 + (T1 * self.s) - (self.p * (self.s - self.x)) - (self.res(self.l, self.w1, self.w2) * (self.s - self.cp(self.l, self.w1, self.w2)))

        return [round(self.A2, 3), round(self.T2, 3), round(self.M2, 3)]

    @staticmethod
    def res(l, w1, w2):
        """Returns a resultant of load intensity, takes l, w1, w2 as arguments"""
        if w1 == 0 and w2 == 0:
            return 0
        else:
            return l * (w1 + w2) / 2

    @staticmethod
    def cp(l :float, w1, w2):
        """Returns a point of application of load intensity resultant, takes l, w1, w2 as arguments"""
        if w1 == 0 and w2 == 0:
            return 0
        else:
            return (l / 3) * (2 * w2 + w1) / (w2 + w1)

    def sf_ordinates(self):
        """This method returns the ordinates for shear force at each section of the member
        for simplicity and speed the sections are taken at each hundredth part of the member. 
        It can be altered by changing the inc variable in __init__"""

        def wx(section):
            """Returns the linearly interpolated ordinate (at any distance from w1) of load intensity between w1 and w2"""
            return self.w1 + ((self.w2 - self.w1) * section / self.l)

        def sf_p(section):
            """Returns the shear force due to force p at any section "y units" away from the origin of the member"""
            if section < self.x:
                return 0
            else:
                return self.p

        def sf_w(section):
            """Returns the shear force due to force W at any section "y units" away from the origin of the member"""
            if section < self.l:
                return self.res(section, self.w1, wx(section))
            else:
                return self.res(self.l, self.w1, self.w2)

        sf = []
        for y in self.sections:
            sf.append(round(-sf_p(y) - sf_w(y) + self.T1, 2))
        return sf

    def bm_ordinates(self):
        """This method returns the ordinates for bending moment at each section of the member
        for simplicity and speed the sections are taken at each hundredth part of the member.
        It can be altered by changing the inc variable in __init__"""

        def wx(section):
            """Returns the linearly interpolated ordinate (at any distance from w1) of load intensity between w1 and w2"""
            return self.w1 + ((self.w2 - self.w1) * section / self.l)

        def bm_p(section):
            """Returns the bending moment due to force p at any section "y units" away from the origin of the member"""
            if section < self.x:
                return 0
            else:
                return self.p * (section - self.x)
        
        def bm_w(section):
            """Returns the bending moment due to force W at any section "y units" away from the origin of the member"""
            if section < self.l:
                return self.res(section, self.w1, wx(section)) * (section - self.cp(section, self.w1, wx(section)))
            else:
                return self.res(self.l, self.w1, self.w2) * (section - self.cp(self.l, self.w1, self.w2))

        bm = []
        for y in self.sections:
            bm.append(round(-bm_p(y) - bm_w(y) + self.T1 * y + self.M1, 2))
        return bm



