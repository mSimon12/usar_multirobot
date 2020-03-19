from graphviz import Digraph
import pandas as pd

# graph = Digraph(comment='My supervisor', filename='teste.gv', format='pdf')

# graph.node('A','A', shape='circle')
# graph.node('B','B', shape= 'circle', color='red')

# # graph.attr('node', shape='doublecircle')
# graph.node('C','C',shape='doublecircle')

# graph.node('D','D',shape='circle')

# graph.edge('A','B','t1')
# graph.edge('B','C','t2')
# graph.edge('C','A','t3')

# print(graph.source)

# graph.view()

df1 = pd.DataFrame([['t1','S1'],['t2','S2'],['t3','S3']],columns=['transition','output'])
df2 = pd.DataFrame([['t4','S1'],['t5','S2'],['t6','S3']],columns=['transition','output'])

dic = {'a':df1,'b':df2}

for s in dic:
    for i in dic[s].index:
        print(dic[s].loc[i]['transition'])