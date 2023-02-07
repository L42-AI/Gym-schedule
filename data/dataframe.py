import pandas as pd

global df
df = pd.DataFrame(data=[None, None, '700-1945', None, '1300-1400', None, '2000-100'],
               index=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
               columns=['Schedule'], dtype=str)