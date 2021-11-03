import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_excel('1-2020test.xlsx')

print(data)
models = set()
for model in data['Model No.'].str.lower():
    models.add(model)
print(models)



