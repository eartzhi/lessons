import pandas as pd
import numpy as np

def check(df):
    first = df['Инфраструктура'].sum()<df['Ромашка 1'].sum()
    second = df['Инфраструктура'].sum()<df['Ромашка 2'].sum()
    return first and second

calc = pd.read_excel('data/calc.xlsx')

if calc['Требуется'].isna().any():
    print('Вычисляем "Требуется"')
    calc['Требуется'] = round(calc['Инфраструктура']*np.random.uniform(1.01, 1.05), 2)
else:
    print('Не вычисляем "Требуется"')
    
chamomile=np.random.randint(1, 3)
n_iter = 0
while True:
    n_iter += 1
    rand=pd.DataFrame(np.random.uniform(0.70, 1.30, size=calc.shape))
    calc['Ромашка '+str(chamomile)] = round(calc['Требуется']*rand[0], 2)
    calc['Ромашка '+str(3-chamomile)] = round(3*calc['Требуется']
                                              -calc['Ромашка '+str(chamomile)]
                                              -calc['Инфраструктура'], 2)
    # result=(calc['Ромашка 1'].sum()+calc['Ромашка 2'].sum()+calc['Инфраструктура'].sum())/3
    if check(calc):
        break

print(f'{n_iter} итераций')
print(calc['Требуется'].sum(), '- сумма по "Требуется"')

calc.loc[-1] = ['Итого', 0, 0, 0, 0]

for i in calc.columns[1:]:
    calc.loc[-1, i] = calc[i].sum()


calc.to_excel('data/result.xlsx', index=False)
