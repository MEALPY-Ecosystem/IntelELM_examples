#!/usr/bin/env python
# Created by "Thieu" at 3:08 PM, 14/10/2024 -------%                                                                               
#       Email: nguyenthieu2102@gmail.com            %                                                    
#       Github: https://github.com/thieu1995        %                         
# --------------------------------------------------%

from data.data_loader import load_credit_score
from intelelm import MhaElmClassifier
from utils.visualizer import draw_confusion_matrix
from pathlib import Path
import pandas as pd
import time


EPOCH = 750
POP_SIZE = 20
TEST_SIZE = 0.2
dataset_name = "credit_score"
PATH_SAVE = f"history_new/{dataset_name}"
Path(PATH_SAVE).mkdir(parents=True, exist_ok=True)

## Load data object
data, scaler_X, scaler_y = load_credit_score(f"data/{dataset_name}.csv", scaling_method="standard")
#### 100000 x 28 x 3 labels (0, 1, 2)

list_optimizers = ("OriginalAGTO", "OriginalAVOA", "OriginalARO", "OriginalHGSO", "OriginalEVO", "OriginalTLO")
list_paras = [
    {"name": "AGTO-ELM", "epoch": EPOCH, "pop_size": POP_SIZE},
    {"name": "AVOA-ELM", "epoch": EPOCH, "pop_size": POP_SIZE},
    {"name": "ARO-ELM", "epoch": EPOCH, "pop_size": POP_SIZE},
    {"name": "HGSO-ELM", "epoch": EPOCH, "pop_size": POP_SIZE},
    {"name": "EVO-ELM", "epoch": EPOCH, "pop_size": POP_SIZE},
    {"name": "TLO-ELM", "epoch": EPOCH, "pop_size": POP_SIZE},
]

t_dict = {}
for idx, opt in enumerate(list_optimizers):
    t_start = time.perf_counter()

    ## Create model
    model = MhaElmClassifier(layer_sizes=(20, 10), act_name="elu", obj_name="CEL",
                             optim=opt, optim_paras=list_paras[idx], verbose=False)

    ## Train the model
    model.fit(X=data.X_train, y=data.y_train)

    ## Test the model
    y_pred_train = model.predict(data.X_train)
    y_pred_test = model.predict(data.X_test)

    ## Save metrics
    model.save_metrics(data.y_train, y_pred_train, list_metrics=("AS", "PS", "NPV", "RS", "F1S"),
                       save_path=PATH_SAVE, filename=f"{model.optimizer.name}-train-metrics.csv")
    model.save_metrics(data.y_test, y_pred_test, list_metrics=("AS", "PS", "NPV", "RS", "F1S"),
                       save_path=PATH_SAVE, filename=f"{model.optimizer.name}-test-metrics.csv")
    ## Save loss train
    model.save_loss_train(save_path=PATH_SAVE, filename=f"{model.optimizer.name}-loss.csv")

    ## Save confusion matrix
    draw_confusion_matrix(data.y_train, y_pred_train, title=f"Confusion Matrix of {model.optimizer.name} on training set",
                          pathsave=f"{PATH_SAVE}/{model.optimizer.name}-train-cm.png")
    draw_confusion_matrix(data.y_test, y_pred_test, title=f"Confusion Matrix of {model.optimizer.name} on testing set",
                          pathsave=f"{PATH_SAVE}/{model.optimizer.name}-test-cm.png")
    ## Save model
    model.save_model(save_path=PATH_SAVE, filename=f"{model.optimizer.name}-model.pkl")

    t_end = time.perf_counter() - t_start
    t_dict[list_paras[idx]["name"]] = t_end

df = pd.DataFrame.from_dict(t_dict, orient="index")
df.to_csv(f"{PATH_SAVE}/time-mha-elm.csv")
