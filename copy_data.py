import pickle
import matplotlib.pyplot as plt
import random as rd

# with open("features.txt","rb") as file:
# 	features=pickle.load(file)

# with open("labels.txt","rb") as file:
# 	labels=pickle.load(file)

# features=features[:-24]
# labels=labels[:-24]

# with open("features.txt","wb") as file:
# 	pickle.dump(features,file)

# with open("labels.txt","wb") as file:
	# pickle.dump(labels,file)

with open("features.txt","rb") as file:
	features=pickle.load(file)

with open("labels.txt","rb") as file:
	labels=pickle.load(file)



print(len(labels))
print(labels[-1])
