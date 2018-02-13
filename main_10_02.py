class HashTable():
    def __init__(self):
        self.H = []
    def insert(self,i,l,h):
        self.H.append((i,l,h))
    def contains(self,i,l,h):
        if (i,l,h) in self.H:
            return True
        else:
            return False
    def lookup(self,i,l,h):
        return (i,l,h)

class ROBDD():
    def __init__(self,expr):
        self.H = HashTable()
        self.expr = expr
    def make(self,i,l,h):
        if l == h:
            return l
        elif self.H.contains(i,l,h):
            return self.H.lookup(i,l,h)
        else:
            self.H.insert(i,l,h)
            return self.H.lookup(i,l,h)
    def build(self):
        self.build_(self.expr[0],1)

    '''
    TODO: Fix this
    '''
    def build_(self,term,i):
        if i>len(self.expr):
            if self.expr[-1] == 0:
                return 0
            else:
                return 1
        else:
            return make(i,build_())
