
class Tree(object):

    def __init__(self, rootKey = 'root', val = None):
        '''
            Creates a tree with the value 'val' associated to the root
        '''
        self.root = Node(None,rootKey)
        self.root.setValue(val)

    def findTreeNode(self,key):
        '''
            Return the pointer to a node according its key
        '''
        if self.root.key == key:
            return self.root
        else:
            node = self.__findNode(self.root,key)
            if node != None:
                return node
            print('No node with key \'',key,'\' found.')
            return None

    def __findNode(self, node, key):
        '''
            Recurssive implementation of Find
        '''
        # Verify if the current node is the one being serched
        if node.key == key:
            return node

        # Look for the desired node in the childrens of current node
        if node.children != None:
            for ch in node.children:
                n = self.__findNode(ch,key)
                if n != None:
                    return n
        return None

    def insertNode(self, p, key, val):
        '''
            Insert a new node in the three with the specified parent:
                p - parant key;
                key - key of the new node;
                val - value of the new node.
        '''
        try:
            p = self.findTreeNode(p)            # Get the parent node according its key

            node = Node(p,key)                  # Creates a new node
            node.setValue(val)                  # Set a value to this node
            p.insertChild(node)                 # Insert the created node in the parents children set
            return node                         # Return the node
        except:
            print("Parent inexistent!")

    def deleteNode(self, node_key):
        '''
            Delete the node with the specified key
        '''
        try:
            n = self.findTreeNode(node_key)            # Get the node according its key

            n.parent.children.remove(n)
            for ch in n.children:
                n.parent.children.add(ch)
                ch.parent = n.parent
            del n
        except:
            print("Node does not exist!")

    def printTree(self):
        '''
            Print the tree
        '''
        print('\t',self.root.key,end='')
        self.printSubTree(self.root,1)
    
    def printSubTree(self, node, level):
        print()
        for ch in node.children:
            for l in range(level):
                print('\t',' |', end='')
            print('------',ch.key,'-',ch.getValue(),end='')
            self.printSubTree(ch, level+1)

    def getNodeDepth(self, key, count = 0):
        '''
            Function call that returns the depth of the node.
        '''
        if key == self.root.key:
            return count
        else:
            n = self.findTreeNode(key)
            return self.getNodeDepth(n.parent.key, count + 1)


class Node(object):
    '''
        Class that represents a Node as a part of a Tree. Each node is composed of:
            - parent;
            - set of children;
            - key;
            - value.
    '''

    def __init__(self,p,k):
        '''
            Initialize a node:
                p - parent node key;
                k - key of the new node.
        '''
        self.parent = p                 # Parent node
        self.children = set()           # Set of children nodes
        self.key = k                    # Key to find this node
        self.__value = None               # Value assigned to the node
        self.__flag = None                # Optional flag (Applied for search algorithms)
    
    def setValue(self,v):
        '''
            Associate a value to the current node
        '''
        self.__value = v
    
    def getValue(self):
        '''
            Return the Node value
        '''
        return self.__value

    def setFlag(self, flag):
        '''
            Associate a flag to the current node
        '''
        self.__flag = flag
    
    def getFlag(self):
        '''
            Return the Node flag
        '''
        return self.__flag

    def insertChild(self,c):
        '''
            Add a children for the current node
        '''
        self.children.add(c)
