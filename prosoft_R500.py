import math

cabinet_rail = 6100
space_backup = 0.2
controller_reserve = True
chanel_backup = 0.2
controller_chanel_backup = 0.2

module_dict = {'AI': ['R500 AI 16 081-000-AAA', 16, 1010, 1, 'R500 CH 02 011-000-AAA', 'R500 CL 20 001'], #модель, кол-во каналов, стоимость, занимаемые слоты, модуль шасси, клеммная колодка
               'AO': ['R500 AO 08 021-000-AAA', 8, 1010, 1, 'R500 CH 02 011-000-AAA', 'R500 CL 20 001' ],
               'DI': ['R500 DI 32 011-000-AAA', 32, 1010, 1, 'R500 CH 02 011-000-AAA', 'R500 CL 36 001'], 
               'DO': ['R500 DO 32 012-000-AAA', 32, 1010, 1, 'R500 CH 02 011-000-AAA', 'R500 CL 36 001'], 
               'CPU': ['R500 CU 00 051-000-AAA', None, 1010000, 2, 'R500 CH 02 022-000-AAA', None],
               'PP': ['R500 PP 00 011-000-AAA', None, 101, 1, 'R500 CH 02 011-000-AAA', None], 
               'ProfiBus': ['R500 CP 01 031-AAA', 1, 101, 1, 'R500 CH 02 011-000-AAA', None],
               'RS-485': ['R500 CP 04 011-AAA', 2, 101, 1, 'R500 CH 02 011-000-AAA', None],
              } 
end_module_dict = {1: ['R500 ST 00 001', 101, 'R500 ST 00 001', 101], #Первый оконечный модуль, цена, последный оконечный модуль, цена
                   8: ['R500 ST 02 013-000-AAA', 101, 'R500 ST 02 023-000-AAA', 101],
                   9: ['R500 ST 02 113-000-AAA', 101, 'R500 ST 02 123-000-AAA', 101]
                   }
barriers_dict = {'NPEXA-KM31': [1, 100, 12.8], 
                 'NPEXA-K5D11': [2, 100, 12.8]} #кол-во каналов, стоимость, ширина.
relay_dict = {'KPR-SCE-24VDC-1C': [1, 101, 6.2]}
sfp_dict = {'MM': ['GLC-FE-100FX=', 101]} # тип модуля, цена

input_chanels = [
                ['AI', '4-20 mA', 'IS', 'NPEXA-KM31', 125],  # последняя цифра-колчество каналов
                ['DI', 'сухой контакт', 'IS', 'NPEXA-K5D11', 222],
                ['ProfiBus', None, None, None, 5],
                ['RS-485', None, None, None, 10]
                ]
output_chanels = [
                ['AO', '4-20 mA', 'IS', 'NPEXA-KM31', 100], 
                ['DO', 'сухой контакт', 'IS', 'NPEXA-K5D11', 60]
                 ]

chanel_counter = {'AI': 0, 'AO': 0, 'DI': 0, 'DO': 0, 'RS-485': 0, 'ProfiBus': 0}
cabinet_complect = {'КАН-Д500С24Н': 4, 'КАН-МД40': 2, 'шкаф': 1}

cross_cabinet_number = 0
controller_cabinet_number = 0
signals_total = 0
filled_space = 0
specification = {}
module_counter = 0
crete_counter = 0


terminal_weigh = 5 + 8  #ширина клеммной сборки

# input_flags = {'4-20 mA': False, '4-20 mA HART': False, 'RTD': False, 'сухой контакт': False; /
#                'импульс': False}
# output_flags = {'4-20 mA': False, '4-20 mA HART': False, 'сухой контакт': False}


def add_to_spec(elem, count, specification):
    if elem in specification.keys():
        specification[elem] += count
    else:
        specification[elem] = count

def add_module_to_spec(module, count, specification):
    add_to_spec(module_dict[module][0], count, specification)
    if module_dict[module][4]:
        add_to_spec(module_dict[module][4], count, specification)


# Основной блок
for ch in input_chanels:
    capacity = math.ceil(ch[4] * (1+chanel_backup))
    if ch[2] == 'IS':
        if barriers_dict[ch[3]][0] == 1:
            filled_space += barriers_dict[ch[3]][2] * capacity
            add_to_spec(ch[3], capacity, specification)
            chanel_counter[ch[0]] += capacity
        else:
            filled_space += barriers_dict[ch[3]][2] * math.ceil(capacity/2)
            add_to_spec(ch[3], math.ceil(capacity/2), specification)
            chanel_counter[ch[0]] += capacity
    elif ch[1] in ['RTD', 'импульс']:
        if barriers_dict[ch[3]][0] == 1:
            filled_space += barriers_dict[ch[3]][2] * capacity
            add_to_spec(ch[3], capacity, specification)
            chanel_counter[ch[0]] += capacity
        else:
            filled_space += barriers_dict[ch[3]][2] * math.ceil(capacity/2)
            add_to_spec(ch[3], math.ceil(capacity/2), specification)      
            chanel_counter[ch[0]] += capacity    
    elif ch[1] == 'Namur':
        filled_space += barriers_dict[ch[3]][2] * capacity
        add_to_spec(ch[3], capacity, specification)         
        chanel_counter[ch[0]] += capacity
    else:
        if ch[0] == 'DI':
            filled_space += terminal_weigh/2 * capacity
            add_to_spec('KPR-SCE-24VDC-1C', * capacity,  specification)
            chanel_counter[ch[0]] += capacity
        elif ch[0] == 'AI':
            filled_space += terminal_weigh/2 * capacity
            chanel_counter[ch[0]] += capacity
        else:
            chanel_counter[ch[0]] += capacity
 

for ch in output_chanels:
    capacity = math.ceil(ch[4] * (1+chanel_backup))
    if ch[2] == 'IS':
        if barriers_dict[ch[3]][0] == 1:
            filled_space += barriers_dict[ch[3]][2] * capacity
            add_to_spec(ch[3], capacity, specification)
            chanel_counter[ch[0]] += capacity
        else:
            filled_space += barriers_dict[ch[3]][2] * math.ceil(capacity/2)
            add_to_spec(ch[3], math.ceil(capacity/2), specification)   
            chanel_counter[ch[0]] += capacity
    else:
        if ch[0] == 'DO':
            filled_space += terminal_weigh/2 * capacity
            add_to_spec('KPR-SCE-24VDC-1C', * capacity,  specification)
            chanel_counter[ch[0]] += capacity
        elif ch[0] == 'AO':
            filled_space += terminal_weigh/2 * capacity
            chanel_counter[ch[0]] += capacity
        else:
            raise TypeError()

# Расчет количества шкафов
cross_cabinet_number = math.ceil(filled_space / (cabinet_rail*(1-space_backup)))
      
# Учет резерва каналов контроллера
for signal in chanel_counter.keys():
    chanel_counter[signal] = math.ceil(chanel_counter[signal] * (1+controller_chanel_backup))
    
# Подсчет модулей процессора
for signal in chanel_counter.keys():
    signals_total +=  chanel_counter[signal]

if controller_reserve:
    add_module_to_spec('CPU', math.ceil(signals_total/2000)*2, specification)
    module_counter += module_dict['CPU'][3]*2
else:
    add_module_to_spec('CPU', math.ceil(signals_total/2000), specification)
    module_counter += module_dict['CPU'][3]

# Модули входов-выходов   
for signal in chanel_counter.keys():
    if signal in module_dict.keys():
        modules = math.ceil(chanel_counter[signal] / module_dict[signal][1])
        add_module_to_spec(signal, modules, specification)
        module_counter += module_dict[signal][3] * modules
    else:
        raise TypeError()

# Количество крейтов и шкафов
crete_counter = math.ceil(module_counter/8)
controller_cabinet_number = math.ceil(crete_counter/8)

# Модули питания
add_module_to_spec('PP', crete_counter*2, specification)
module_counter += module_dict['PP'][3]*2             

# Оконечные модули
if crete_counter == 1:
    add_to_spec(end_module_dict[1][0], 1, specification)
    add_to_spec(end_module_dict[1][2], 1, specification)
elif crete_counter > 8:
    inner_module = crete_counter - controller_cabinet_number
    add_to_spec(end_module_dict[8][0], inner_module, specification)
    add_to_spec(end_module_dict[8][2], inner_module, specification)
    add_to_spec(end_module_dict[9][0], controller_cabinet_number, specification)
    add_to_spec(end_module_dict[9][2], controller_cabinet_number, specification)
    add_to_spec(sfp_dict['MM'][0], controller_cabinet_number*4, specification)
else:
    add_to_spec(end_module_dict[8][0], crete_counter, specification)
    add_to_spec(end_module_dict[8][2], crete_counter, specification)    
    
# Дополнительно еоборудование в шкафы
for i in range(cross_cabinet_number + controller_cabinet_number):
    for elem, count in cabinet_complect.items():
        add_to_spec(elem, count,  specification)        
    


print(specification, '\n', cross_cabinet_number, '\n', chanel_counter, '\n', signals_total, '\n', module_counter)



# for ch in output_chanels:
#     if ch[2] == 'IS':
#         if barriers_dict[ch[3]][0] == 1:
#             filled_space += barriers_dict[ch[3]][2]
#             add_to_spec(ch[3], specification)
#         else:
#             if input_flags[ch[1]]:
#                 input_flags[ch[1]] = False
#             else:
#                 filled_space += barriers_dict[ch[3]][2]
#                 add_to_spec(ch[3], specification)
#                 input_flags[ch[1]] = True
                
#     elif ch[1] in  ['RTD', 'импульс']:
#         if barriers_dict[ch[3]][0] == 1:
#             filled_space += barriers_dict[ch[3]][2]
#             add_to_spec(ch[3], specification)
#         else:
#             if input_flags[ch[1]]:
#                 input_flags[ch[1]] = False
#             else:
#                 filled_space += barriers_dict[ch[3]][2]
#                 add_to_spec(ch[3], specification)
#                 input_flags[ch[1]] = True
                
#     elif ch[1] == 'Namur':
#         filled_space += barriers_dict[ch[3]][2]
#         add_to_spec(ch[3], specification)
           
#     else:
#         if ch[0] == 'DI':
#             filled_space += terminal_weigh/2
#             add_to_spec('KPR-SCE-24VDC-1C', specification)
#         elif ch[0] == 'AI':
#             filled_space += terminal_weigh/2
#         else:
#             raise TypeError