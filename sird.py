import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import product

# Lecture des données
data = pd.read_csv("sird_dataset.csv")
print(data)