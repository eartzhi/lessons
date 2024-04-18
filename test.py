import pandas as pd
import numpy as np

calc = pd.read_excel('data/calc.xlsx')

# print(calc.shape)

rand=pd.DataFrame(np.random.uniform(0.85, 1.15, size=calc.shape))
chamomile=np.random.randint(1, 3)
print(chamomile)
calc['chamomile_'+str(chamomile)] = calc['needs']*rand[0]
calc['chamomile_'+str(3-chamomile)] = 3*calc['needs']-calc['chamomile_'+str(chamomile)]-calc['Itk']
result=(calc['chamomile_1'].sum()+calc['chamomile_2'].sum()+calc['Itk'].sum())/3
print(calc)
print(calc['needs'].sum())
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