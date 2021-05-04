import pandas as pd
import time

import os


path = os.path.dirname(os.path.abspath(__file__))
filename = path + '/missions_sequences/{}.csv'.format(time.strftime("%b-%d-%Y  %H:%M:%S"))

print(filename)

time.sleep(1)

df = pd.DataFrame(columns=['time', 'c1', 'c2', 'c3'])
df.index.name="Time"

df = df.append({ 'time': time.strftime("%H:%M:%S"),'c1': 1.0, 'c2': 'b','c3': 'carro'}, ignore_index=True)
time.sleep(1)

# df.loc[time.strftime("%H:%M:%S")] = [5.5, 'k', 'moto']
# time.sleep(1)

# df.loc[time.strftime("%H:%M:%S")] = [10.5, 'x', 'onibus']
# time.sleep(1)



print(df.iloc[0]['c1'])


# df.to_csv(filename,)