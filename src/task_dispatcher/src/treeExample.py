import tree as t

tree = t.Tree('root',10)
tree.insertNode('root','v2', 5)
tree.insertNode('root','v3', 15)
tree.insertNode('v2','v4', 150)
tree.insertNode('v2','v5', 250)
tree.insertNode('v4','v7', 250)
tree.insertNode('v3','v10', 250)
tree.printTree()

tree.deleteNode('v4')
print()
tree.printTree()



