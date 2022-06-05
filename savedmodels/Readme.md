This folder contains a saved keras NN and saved XGBoost model. 

- The NN was saved using `model.save()`, and can be loaded into a python workspace using `keras.models.load_model("LoadNN.ann")`
- The XGBoost model was saved using pickle, and can be loaded from disk with `pickle.load(open("filename", rb))`
