import math


class ROBDD:
    # Init the ROBDD with nVars = number of variables in the expression
    def __init__(self,nVars,switch = 0):
        self.nVars = nVars
        self.switch = switch
        self.nNodes = 0
        self.nNodes_ = 0
        self.x = []
        self.anySatX = []
        for item in range(nVars):
            self.x.append(0)
            self.anySatX.append(-1)
        self.initT(self)
        self.initH(self)
        self.initH_(self)
        self.initT_(self)
        self.build(0)



    # Init the Table with 0,1 entries
    @staticmethod
    def initT(self):
        self.T = 2*[3*[None]]
        self.T[0] = [self.nVars + 1,-1,-1]
        self.T[1] = [self.nVars + 1,-2,-2]  # Using a different dummy entry -2, to ensure correct hashing
        self.nNodes = 2


    # Init the HashTable with hashes for 0 and 1
    @staticmethod
    def initH(self):
        self.H = 2 * [None]
        self.H[0] = self.hashH(self,0)
        self.H[1] = self.hashH(self,1)


    # Create Hashes for 0 and 1
    @staticmethod
    def hashH(self,nodeNum):
        return hash(str(self.T[nodeNum][0])+str(self.T[nodeNum][1])+str(self.T[nodeNum][2]))


    # Check if an entry exists in H
    def member(self, i, l, h):
        if hash(str(i) + str(l) + str(h)) in self.H:
            return True
        else:
            return False


    # Return the index of item with a given (i,l,h) from H
    def lookup(self,i,l,h):
        return self.H.index(hash(str(i) + str(l) + str(h)))


    # Add an entry to the table T, with values(i,l,h)
    def add(self,i,l,h):
        self.T.append([i,l,h])
        self.nNodes = self.nNodes + 1
        return self.nNodes - 1


    # Add an entry to H, with (i,l,h)
    def insert(self,i,l,h):
        self.H.append(hash(str(i) + str(l) + str(h)))


    # Add an entry to the T table.
    def make(self,i,l,h):
        if l == h:
            return l
        elif self.member(i,l,h):
            return self.lookup(i,l,h)
        else:
            u = self.add(i,l,h)
            self.insert(i,l,h)
            return u


    # Create the Table and the Inverse Hash Table.
    def build(self,i=0):
        if i>=self.nVars:
            return self.eval()
        else:
            self.x[i] = 0
            l = self.build(i+1)
            self.x[i] = 1
            h = self.build(i+1)
            return self.make(i,l,h)


    # Returns the number of satisfying combinations for a given equation.
    def satCount(self):
        node = self.T[-1]
        count = self.satCount_(node)
        return math.pow(2,node[0]-1)*count


    # Inner SatCount_ function
    def satCount_(self,node = None):
        if node[1] == -1:
            return 0
        elif node[1] == -2:
            return 1
        else:
            low = math.pow(2,self.T[node[1]][0] - node[0] -1) * self.satCount_(self.T[node[1]])
            high = math.pow(2,self.T[node[2]][0] - node[0] -1) * self.satCount_(self.T[node[2]])
            return low+high


    # Returns a Satisfying set of constants for a given equation.
    def anySat(self,node = None):
        if node == None:
            node = self.T[-1]
        if node[1] == -1:
            print('Error! :(')
        elif node [1] == -2:
            pass
        elif node[1] == 0:
            self.anySatX[node[0]] = 1
            self.anySat(self.T[node[2]])
        else:
            self.anySatX[node[0]] = 0
            self.anySat(self.T[node[1]])
        return self.anySatX


    # Restrict
    def restrict(self,node=None,j=0,b=0):
        #newROBDD = ROBDD(self.nVars)
        #self.restrict_(newROBDD.T[-1],j,b)
        #self.restrict_(self.T[-1],j,b)
        for item in range(2,self.nNodes):
            if self.T[item][0] != j:
                self.restrict_(self.T[item],j,b)


    # Inner Function for Restrict
    def restrict_(self,node,j,b):
        if node[0] > j:
            #self.build(self.lookup(node[0],node[1],node[2]))
            if self.member_(node[0],node[1],node[2]):
                return self.lookup(node[0],node[1],node[2])
            else:
                self.make_(node[0],node[1],node[2])
                return self.lookup(node[0],node[1],node[2])
        elif node[0] < j:
            return self.make_(node[0],self.restrict_(self.T[node[1]],j,b),self.restrict_(self.T[node[2]],j,b))
        elif node[0] == j:
            if b == 0:
                return self.restrict_(self.T[node[1]],j,b)
            else:
                return self.restrict_(self.T[node[2]],j,b)

    #################################################
    #   Helper Functions for Restrict Method        #
    #################################################

    # adds an entry to the T_ table
    def make_(self,i,l,h):
        if l == h:
            return l
        elif self.member_(i,l,h):
            return self.lookup_(i,l,h)
        else:
            u = self.add_(i,l,h)
            self.insert_(i,l,h)
            return u


    # Add an entry to H_ with (i,l,h)
    def insert_(self,i,l,h):
        self.H_.append(hash(str(i) + str(l) + str(h)))


    # Add an entry to the table T_, with values(i,l,h)
    def add_(self,i,l,h):
        self.T_.append([i,l,h])
        self.nNodes_ = self.nNodes_ + 1
        return self.nNodes_ - 1


    # Check if an entry exists in H_
    def member_(self, i, l, h):
        if hash(str(i) + str(l) + str(h)) in self.H_:
            return True
        else:
            return False


    # Return the index of item with a given (i,l,h) from H_
    def lookup_(self, i, l, h):
        return self.H_.index(hash(str(i) + str(l) + str(h)))


    # Init T_
    @staticmethod
    def initT_(self):
        self.T_ = 2*[3*[None]]
        self.T_[0] = [self.nVars + 1,-1,-1]
        self.T_[1] = [self.nVars + 1,-2,-2]  # Using a different dummy entry -2, to ensure correct hashing
        self.nNodes_ = 2


    # Init H_
    @staticmethod
    def initH_(self):
        self.H_ = 2 * [None]
        self.H_[0] = self.hashH(self,0)
        self.H_[1] = self.hashH(self,1)


    #################################################
    #   Helper Functions used instead of a parser   #
    #################################################

    def and_(self, a,b):
        return int(a and b)


    def or_(self, a,b):
        return int(a or b)


    def implies_(self,a,b):
        if a == 1 and b == 0:
            return 0
        else:
            return 1


    def equiv_(self,a,b):
        if a == b:
            return 1
        else:
            return 0


    def not_(self,a):
        return int(not a)

    # Hardcoding the expression for now!
    # TODO : Integrate the parser with the exisiting ROBDD code.
    def eval(self):
        if self.switch:
            return self.equiv_(self.and_(self.x[0],self.x[1]),self.x[2])
        # Test Case 3
        #return self.and_(self.and_(self.and_(self.x[0],self.x[1]),self.and_(self.x[2],self.x[3])),self.and_(self.and_(self.x[4],self.x[5]),self.and_(self.x[6],self.x[7])))
        # Test Case 2
        #return (self.and_(self.implies_(self.not_(self.x[0]),self.equiv_(1,self.x[1])),self.not_(self.x[2])))
        # Test Case 1
        return self.or_(self.equiv_(self.x[0],self.x[1]),self.x[2])

        # Negative Test Case for SatCount
        #return self.and_(0,self.x[0])

######### Class Apply_ROBDD inherits from class ROBDD#######

class Apply_ROBDD(ROBDD):
    def __init__(self,nVars):
        self.nVars = nVars
        self.nNodes = 0
        self.x = []
        self.anySatX = []
        for item in range(nVars):
            self.x.append(0)
            self.anySatX.append(-1)
        self.initT(self)
        self.initH(self)
        self.initH_(self)
        self.initT_(self)
        #self.build(0)
        self.G = {}

    def apply(self,op,r1,r2):
        self.op = op
        self.T1 = r1.T
        self.T2 = r2.T
        self.apply_(r1.nNodes - 1,r2.nNodes - 1)

    def apply_(self,u1,u2):
        if (u1,u2) in self.G:
            return self.G[(u1,u2)]
        if (self.T1[u1][1] < 0) and (self.T2[u2][1] < 0):
            u = self.evalOp(u1,u2)
        elif self.T1[u1][0] == self.T2[u2][0]:
            u = self.make(self.T1[u1][0],self.apply_(self.T1[u1][1],self.T2[u2][1]),self.apply_(self.T1[u1][2],self.T2[u2][2]))
        elif self.T1[u1][0] < self.T2[u2][0]:
            u = self.make(self.T1[u1][0],self.apply_(self.T1[u1][1],u2),self.apply_(self.T1[u1][2],u2))
        elif self.T1[u1][0] > self.T2[u2][0]:
            u = self.make(self.T2[u2][0], self.apply_(u1, self.T2[u2][1]),self.apply_(u1, self.T2[u2][2]))

        self.G[(self.T1[u1][0])] = u
        return u


    def evalOp(self,u1,u2):
        if self.T1[u1][1] == -1:
            eval1 = 0
        else:
            eval1 = 1

        if self.T2[u2][1] == -1:
            eval2 = 0
        else:
            eval2 = 1

        if self.op == 'and':
            return self.and_(eval1,eval2)
        elif self.op == 'or':
            return self.or_(eval1,eval2)
        elif self.op == 'equal':
            return self.equiv_(eval1,eval2)
        elif self.op == 'implies':
            return self.implies_(eval1,eval2)