from catboost import CatBoostClassifier
import glob
import pandas as pd
import numpy as np

def jitter(d):
    """
    Calculate jitter.
    """
    
    return pd.Series(np.mean(np.abs(d.values[1:] - d.values[:-1]), axis=0),
                     index=["_".join([cl, "jitter"]) for cl in d.columns])

def get_trend(d):
    """
    Calcuate trend for a frame `d`.
    """

    dv = d.reset_index(drop=True)
    dv["minutes"] = np.arange(dv.shape[0], dtype=np.float64)
    covariance = dv.cov()
    return (((covariance["minutes"])/covariance.loc["minutes", "minutes"])[d.columns]
            .rename(lambda cl: "_".join([cl, "trend"])))

def get_features(frame):
    """
    Calculate simple features for dataframe.
    """
    
    average_sensors = frame.mean(axis=1)
    average_temp = average_sensors.mean()
    std_temp = average_sensors.std()
    min_temp = average_sensors.min()
    max_temp = average_sensors.max()

    features = []
    features.append(frame.mean().rename(lambda cl: "_".join([cl, "mean"])))
    features.append(frame.std().rename(lambda cl: "_".join([cl, "std"])))
    features.append(frame.min().rename(lambda cl: "_".join([cl, "min"])))
    features.append(frame.max().rename(lambda cl: "_".join([cl, "max"])))

    features.append(frame.mean().rename(lambda cl: "_".join([cl, "mean_norm"]))/average_temp)
    features.append(frame.std().rename(lambda cl: "_".join([cl, "std_norm"]))/std_temp)
    features.append(frame.min().rename(lambda cl: "_".join([cl, "min_norm"]))/min_temp)
    features.append(frame.max().rename(lambda cl: "_".join([cl, "max_norm"]))/max_temp)

    features.append(jitter(frame))
    features.append(get_trend(frame))
    features.append(jitter(frame).rename(lambda cl: "_".join([cl, "norm"]))/(max_temp-min_temp))

    features.append(average_sensors.apply(["mean", "std", "min", "max"]))
    return pd.concat(features)



text_file = open("SIM_COLS.txt", "r")
lines = text_file.read().split('\n')
SIM_COLS = lines[:-1]

models_files = glob.glob("C:\_sibur\\data\\models\\*")

test_preds = pd.DataFrame()
test_features = {}
f = "frame_0.csv"
frame_data = pd.read_csv(f)
test_features = get_features(frame_data)
test_features = pd.DataFrame(test_features)
test_features = test_features.T
for file_name in models_files:
	model = CatBoostClassifier()
	model.load_model(file_name) 
	sensor = file_name[22:-4]
	local_preds = model.predict_proba(test_features[SIM_COLS].values)[:, 1]
	test_preds[sensor] = pd.Series(local_preds.astype(np.float), index=test_features.index)
print(test_preds)