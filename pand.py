import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


date_list = []
price_list = []

data = pd.read_csv("p_p.csv") 
price = data["prices"]
date = data["posting_date"]

for v in price:
    price_list.append(v)

for d in date:
    date_list.append(d)

plt.plot(date_list, price_list, color='green', marker='o')
plt.title ("График изменения цен")
plt.ylabel("Цена ₽")
plt.xlabel("Дата")
plt.show()
print(date_list)