import pandas as pd
from datetime import time

global df
df = pd.DataFrame(data=[[None, None],
                        [None, None],
                        ['700', '1945'],
                        [None, None],
                        ['1300', '1400'],
                        [None, None],
                        ['2000', '100']],
               index=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
               columns=['Start', 'Finish'], dtype=str)

print(df)