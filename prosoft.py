import math

cabinet_rail = 6100
space_backup = 0.2
chanel_backup = 0.2
controller_chanel_backup = 0.2

module_dict = {'AI': ['R500 AI 16 081-000-AAA', 16], 
               'AO': ['R500 AO 08 021-000-AAA', 16],
               'DI': ['R500 DI 32 011-000-AAA', 32], 
               'DO': ['R500 DO 32 012-000-AAA', 32]
              } 
barriers_dict = {'NPEXA-KM31': [1, 100, 12.8], 
                 'NPEXA-K5D11': [2, 100, 12.8]} #кол-во каналов, стоимость, ширина.
relay_dict = {'KPR-SCE-24VDC-1C': [1, 101, 6.2]}

input_chanels = [
                ['AI', '4-20 mA', 'IS', 'NPEXA-KM31', 15],  # последняя цифра-колчество каналов
                ['DI', 'сухой контакт', 'IS', 'NPEXA-K5D11', 222]
                ]
output_chanels = [
                ['AO', '4-20 mA', 'IS', 'NPEXA-KM31', 156], 
                ['DO', 'сухой контакт', 'IS', 'NPEXA-K5D11', 60]
                 ]

chanel_counter = {'AI': 0, 'AO': 0, 'DI': 0, 'DO': 0, 'ModBus': 0, 'ProfiBus': 0}
cabinet_complect = {'КАН-Д500С24Н': 4, 'КАН-МД40': 2, 'шкаф': 1}

cross_cabinet_number = 0
filled_space = 0
specification = {}

terminal_weigh = 5 + 8  #ширина клеммной сборки

# input_flags = {'4-20 mA': False, '4-20 mA HART': False, 'RTD': False, 'сухой контакт': False; /
#                'импульс': False}
# output_flags = {'4-20 mA': False, '4-20 mA HART': False, 'сухой контакт': False}


def add_to_spec(elem, count, specification):
    if elem in specification.keys():
        specification[elem] += count
    else:
        specification[elem] = count
    

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
            raise TypeError()
 

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

for i in range(cross_cabinet_number):
    for elem, count in cabinet_complect.items():
        add_to_spec(elem, count,  specification)
        
# Учет резерва каналов контроллера
for signal in chanel_counter.keys():
    chanel_counter[signal] = math.ceil(chanel_counter[signal] * (1+controller_chanel_backup))
    

            

print(specification, '\n', cross_cabinet_number, '\n', chanel_counter)



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