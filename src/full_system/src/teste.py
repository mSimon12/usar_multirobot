import matplotlib.pyplot as plt
from numpy.core.records import array
import pandas as pd

fig = plt.figure()

ax = fig.add_subplot(constrained_layout=True)
ax plot_wireframe([1,2,3],[1,2,3],[1,2,3])
# ax.set_xlabel('f [Hz]')
# ax.set_ylabel('PSD')
# ax.set_title('Random spectrum')

secax = ax.secondary_xaxis('top', [10,3,4])
secax.set_xlabel('period [s]')

plt.show()
# df = pd.DataFrame(columns=['a','b','c'])

# df.loc[1] = [1,2,3]
# df.loc[2] = [4,5,None]
# df.loc[3] = [7,8,9]

# print(df)

# print(list(df.columns.values).index('b'))
