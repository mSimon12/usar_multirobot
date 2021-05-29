from numpy.core.numeric import NaN
import pandas as pd

df = pd.DataFrame({'a':[1,2,3,4,5],'b':[10,20,NaN,40,50]})

print(df[df['b'].notnull()]['a'].values)

x = [1,3]

df.append(x, ignore_index=True)

print(df)