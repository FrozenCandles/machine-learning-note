
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


dataset_list = [f for f in os.listdir(os.path.dirname(__file__)) if f.endswith('.csv')]

fig = plt.figure()

axes = fig.subplots(len(dataset_list) // 3, 3).flatten()


for dataset, ax in zip(dataset_list, axes):
    data = pd.read_csv(os.path.join(os.path.dirname(__file__), dataset))
    if len(data.columns) == 2 :
        x, y = data.values[:, 0], data.values[:, 1]
        ax.scatter(x, y)
        ax.set_title(dataset)
    if not (set(['x', 'y', 'label']) - set(data.columns)):
        x, y, label = data['x'], data['y'], data['label']
        
        ax.scatter(x, y, c=label)
        ax.set_title(dataset)
    
plt.show()