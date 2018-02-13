class Tree:
    def __init__(self,data = -1):
        self.right = None
        self.left = None
        self.data = data
    def insertRight(self,data):
        self.right = Tree(data)
    def insertLeft(self,data):
        self.left = Tree(data)
    def insertData(self,data):
        self.data = data


class Parser:
    '''
    def __init__(self,exprStr):
        nChar = len(exprStr)
        i = nChar
        tempStr = ''
        parseTree = Tree()
        root = parseTree
        while i>=0:
            tempChar = str(exprStr[nChar-i])
            tempStr = tempStr + tempChar
            if tempChar == '(':
                root.insertData(tempStr)
            elif tempChar == ',':
                root.insertLeft(tempStr)
                root = root.left
            elif tempChar == ')':

            i = i - 1
    '''
    def __init__(self,strExpr):
        tree = parse(strExpr)
    def parse(self):
        pass

def getparts(string):
    temp1 = ''
    temp2 = ''
    flag = True
    count = 0
    countStr = 0
    for item in string:
        temp1 = temp1 + item
        countStr = countStr + 1
        if item == '(':
            count = count + 1
            flag = False
        if item == ')':
            count = count - 1
        if count == 0:
            flag = True
        if flag == True and item == ',':
            temp2 = string[countStr:]
            break
    return temp1[0:-1],temp2

def splitNode(node):
    lister = node.split('(')
    node0 = lister[0]
    stringer = ''
    for i in range(1,len(lister)-1):
        stringer = stringer + lister[i] + '('
    stringer = stringer + lister[len(lister)-1][0:-1]
    node1,node2 = getparts(stringer)
    return node0,node1,node2

def insertNode(tree,node0,node1,node2):
    tree.insertData(node0)
    if '(' in node1:
        tree.left = Tree()
        lNode0,lNode1,lNode2 = splitNode(node1)
        insertNode(tree.left,lNode0,lNode1,lNode2)
    else:
        tree.insertLeft(node1)

    if '(' in node2:
        tree.right = Tree()
        rNode0, rNode1, rNode2 = splitNode(node2)
        insertNode(tree.right, rNode0, rNode1, rNode2)
    else:
        tree.insertRight(node2)

    return tree

def preorder(tree):
    if tree == None:
        return
    print(tree.data)
    preorder(tree.left)
    preorder(tree.right)
'''
test = 'and(and(1,2),and(3,4))'
lister = test.split('(')
node0 = lister[0]
nodeBig = lister[1] + '('+lister[2] + '(' +lister[3][0:-1]
node1,node2 = getparts(nodeBig)
'''
test = 'and(and(1,2),and(3,4))'
node0,node1,node2 = splitNode(test)
parseTree = Tree()
jhaad = insertNode(parseTree,node0,node1,node2)
preorder(jhaad)
'''
lister = test.split('(')
node = lister[0]
for item in lister[0:-1]:
    pass
    
'''

getparts('and(x1,x2),and(x3,x4)')
#syntax = Parser('and(and(1,2),and(3,4))')