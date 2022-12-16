import pandas as pd
import numpy as np
import csv
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

def truncatecsv():
    cpt = 100000
    with open('./intrusion_dataset_trunc.csv', newline='\n', mode='w+', encoding='UTF8') as f:
        f = csv.writer(f,delimiter=',')
        with open('./intrusion_dataset.csv', newline='\n', encoding='UTF8') as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            #get the header
            header = next(reader)
            id_la = header.index('Label')
            id_src = header.index('Src_IP')
            id_dst = header.index('Dst_IP')
            f.writerow([header[id_src], header[id_dst], header[id_la]])
            for row in reader:
                cpt -= 1
                if row[id_la] == 'Anomaly':
                    f.writerow([row[id_src], header[id_dst], row[id_la]])
                if cpt <= 0:.2
                    return

def AssocRulesUtilities():
    truncatecsv()
    df = pd.read_csv("./intrusion_dataset_trunc.csv", sep = ',')
    df.head()
    print(df.shape)
    a = TransactionEncoder()
    
    # Create an empty list
    data =[]
    
    # Iterate over each row
    for index, rows in df.iterrows():
        # Create list for the current row
        my_list = [str(el) for el in rows]
        # append the list to the final list
        data.append(my_list)

    a_data = a.fit(data).transform(data)
    df = pd.DataFrame(a_data,columns=a.columns_)
    df = df.replace(False,0)
    print(df)

AssocRulesUtilities()


    