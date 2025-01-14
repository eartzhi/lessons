import datetime
import pickle
import os
from pathlib import Path

now = datetime.datetime.now()

print(now.hour)
parent = Path(__file__).resolve().parent.parent

parent = os.path.join(parent, 'model.pkl')
print(parent)
with open(parent, 'rb') as pkl_file:
    model = pickle.load(pkl_file)