import math

cabinet_rail = 6100
space_backup = 0.2

barriers_dict = {'NPEXA-KM31': [1, 100, 12.8], 'NPEXA-K5D11': [2, 100, 12.8]}
relay_dict = {'KPR-SCE-24VDC-1C': [1, 101, 6.2]}
input_chanels =[['AI', '4-20 mA', 'IS', 'NPEXA-KM31', 15], 
          ['DI', 'сухой контакт', 'IS', 'NPEXA-K5D11', 222]]

output_chanels =[['AO', '4-20 mA', 'IS', 'NPEXA-KM31', 156], 
          ['DO', 'сухой контакт', 'IS', 'NPEXA-K5D11', 54]]

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
    
    
for ch in input_chanels:
    if ch[2] == 'IS':
        if barriers_dict[ch[3]][0] == 1:
            filled_space += barriers_dict[ch[3]][2] * ch[4]
            add_to_spec(ch[3], ch[4], specification)
        else:
            filled_space += barriers_dict[ch[3]][2] * math.ceil(ch[4]/2)
            add_to_spec(ch[3], math.ceil(ch[4]/2), specification)
    elif ch[1] in ['RTD', 'импульс']:
        if barriers_dict[ch[3]][0] == 1:
            filled_space += barriers_dict[ch[3]][2] * ch[4]
            add_to_spec(ch[3], ch[4], specification)
        else:
            filled_space += barriers_dict[ch[3]][2] * math.ceil(ch[4]/2)
            add_to_spec(ch[3], math.ceil(ch[4]/2), specification)          
    elif ch[1] == 'Namur':
        filled_space += barriers_dict[ch[3]][2] * ch[4]
        add_to_spec(ch[3], ch[4], specification)         
    else:
        if ch[0] == 'DI':
            filled_space += terminal_weigh/2 * ch[4]
            add_to_spec('KPR-SCE-24VDC-1C', * ch[4],  specification)
        elif ch[0] == 'AI':
            filled_space += terminal_weigh/2 * ch[4]
        else:
            raise TypeError()
 

for ch in output_chanels:
    if ch[2] == 'IS':
        if barriers_dict[ch[3]][0] == 1:
            filled_space += barriers_dict[ch[3]][2] * ch[4]
            add_to_spec(ch[3], ch[4], specification)
        else:
            filled_space += barriers_dict[ch[3]][2] * math.ceil(ch[4]/2)
            add_to_spec(ch[3], math.ceil(ch[4]/2), specification)   
    else:
        if ch[0] == 'DI':
            filled_space += terminal_weigh/2 * ch[4]
            add_to_spec('KPR-SCE-24VDC-1C', * ch[4],  specification)
        elif ch[0] == 'AI':
            filled_space += terminal_weigh/2 * ch[4]
        else:
            raise TypeError()

cross_cabinet_number = math.ceil(filled_space / (cabinet_rail*(1-space_backup)))

for i in range(cross_cabinet_number):
    for elem, count in cabinet_complect.items():
        add_to_spec(elem, count,  specification)
            
print(specification, cross_cabinet_number)



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