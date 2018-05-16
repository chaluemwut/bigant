import pickle
documents = ["A computer is a device that",
             "Amazon sells many things",
             "Microsoft announces Nokia acquisition"] 

pickle.dump(documents, open('document.obj', 'wb'))			 