from pprint import pprint
import csv
import re
# from itertools import groupby

with open("phonebook_raw.csv", encoding='utf-8') as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
# pprint(contacts_list)

def name(list):
    for i in range(1, len(list)):
        l=[]
        l.append(list[i][0])
        l.append(list[i][1])
        l.append(list[i][2])
        if '' in l:
            l.remove('')
        if '' in l:
            l.remove('')
        if len(l)>1:
            s = ' '.join(l)
            l=s.split(' ')
        else:
            f=l[0].split(' ')
            l=f
        if len(l)<3:
            l.append('')
        list[i][0]=l[0]
        list[i][1]=l[1]
        list[i][2]=l[2]
    return list

def phone(list):
    for i in range(1, len(list)):
        if list[i][5] != '':
            p=r'(\+7|8)\s*(\(\d+\))\s*(\d+)[\s-]+(\d+)[\s-]+(\d+)'
            g=r'(\+7|8)\s*(\d+)[\s-]+(\d+)[\s-]+(\d{2})+(\d{2})'
            k=r'(\+7|8)\s*(\d{3})\s*(\d{3})\s*(\d{2})\s*(\d{2})'
            n=r'((\(доб\.)\s*(\d+)\))|((доб\.)\s*(\d+))'

            result1=re.search(p, list[i][5])
            result2=re.search(g, list[i][5])
            result3=re.search(k, list[i][5])
            result4=re.search(n, list[i][5])
            if result1!=None and result4!=None:
                results1 = re.sub(p, r"+7\2\3-\4-\5", list[i][5])
                result = re.sub(n, r"доб.\3\6", results1)
            elif result1!=None:
                result = re.sub(p, r"+7\2\3-\4-\5", list[i][5])
            elif result2!=None:
                result = re.sub(g, r"+7(\2)\3-\4-\5", list[i][5])
            elif result3!=None:
                result = re.sub(k, r"+7(\2)\3-\4-\5", list[i][5])
            list[i][5]=result
    return list

def contact(list):
    w=list
    for j in range(0, len(w)):       
        if len(w[j])>7:
            del w[j][7]

    for j in range(0, len(w)):       
        for i in range(2, len(list)):
            if w[j]!=list[i]:
                if w[j][0]==list[i][0] and w[j][1]==list[i][1]:
                    if w[j][2]=='' and list[i][2]!='':
                        w[j][2]=list[i][2]
                    if w[j][3]=='' and list[i][3]!='':
                        w[j][3]=list[i][3]
                    if w[j][4]=='' and list[i][4]!='': 
                        w[j][4]=list[i][4]
                    if w[j][5]=='' and list[i][5]!='':
                        w[j][5]=list[i][5]
                    if w[j][6]=='' and list[i][6]!='':
                        w[j][6]=list[i][6]
    
    list2 = []
    for i in w:
        if i not in list2:
            list2.append(i)
    return list2

# list2 = [el for el, _ in groupby(w)]
       
contacts_list2 = contact(phone(name(contacts_list)))    
# pprint(contacts_list2)

## Код для записи файла в формате CSV:
with open("phonebook.csv", "w", encoding='utf-8') as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(contacts_list2)