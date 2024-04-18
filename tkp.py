import pandas as pd
import numpy as np

calc = pd.read_excel('data/calc.xlsx')

# print(calc.shape)

rand=pd.DataFrame(np.random.uniform(0.85, 1.15, size=calc.shape))
chamomile=np.random.randint(1, 3)
# print(chamomile)
calc['Ромашка '+str(chamomile)] = round(calc['Требуется']*rand[0], 2)
calc['Ромашка '+str(3-chamomile)] = round(3*calc['Требуется']-calc['Ромашка '+str(chamomile)]-calc['Инфраструктура'], 2)
result=(calc['Ромашка 1'].sum()+calc['Ромашка 2'].sum()+calc['Инфраструктура'].sum())/3
# print(calc)
print(calc['Требуется'].sum())
print(result)
calc.to_excel('data/result.xlsx')
# calc.drop(['chamomile_2', 'chamomile_1'], axis=1, inplace=True)
# print(calc)
# calc['chamomile_1'] = calc['needs']*np.random.randint(0.85, 1.15)
# while True:
#     calc['chamomile_1'] = calc['needs']*np.random.randint(0.85, 1.15)
#     calc['chamomile_2'] = calc['needs']*np.random.uniform(0.85, 1.15)
#     result=(calc['chamomile_1'].sum()+calc['chamomile_2'].sum()+calc['Itk'].sum())/3
#     print(round(result), round(calc['needs'].sum()))
#     if round(result)==round(calc['needs'].sum()):
#         print(calc)
#         break
#     else:
#         calc.drop(['chamomile_2', 'chamomile_1'], axis=1, inplace=True)