import pandas as pd
import numpy as np
import math

data = {
    'Row Labels': ['NPEXA-HM31', 'NPEXA-H01', 'NPEXA-H511', 'NPEXB-HM31', 'NPEXB-CM35', 'KB429S'],
    'Sum of Колво': [1, 2, 3, 4],
    'По спецификации': [1, 2, 3, 4]
}
df = pd.DataFrame(data)

df.set_index('Raw Labels', inplace = True)
df.index = pd.to_datetime(df.index)
df.columns = ['Sum of Колво', 'По спецификации']

trebIO = float(input("Введите значение:"))
RezervIO = math.ceil(trebIO * 0.2)
Vsego = RezervIO + trebIO

Kanalnie = float(input("Введите значение:"))
Kolvo = math.ceil(Vsego/Kanalnie)
PredlIO = math.ceil(Kolvo * Kanalnie)

print(df)


