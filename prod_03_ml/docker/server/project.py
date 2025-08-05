import pandas as pd
import numpy as np
import xgboost
import os
import pickle

from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score,\
    StratifiedKFold
from prometheus_client import Gauge, start_http_server, Histogram, Counter


base_dir = Path(__file__).resolve().parent
data_path = os.path.join(base_dir, 'data/winequality-red.zip')


start_http_server(8000)

data = pd.read_csv(data_path, sep=';')

data['target'] = data['quality'].apply(lambda x: 'bad wine' if x<6.5 else 'good wine').astype('category')
data['target'] = data['target'].apply(lambda x: 0 if x=='bad wine' else 1).astype('int')

s_scaler = StandardScaler()

# кодируем исходный датасет
X = pd.DataFrame(s_scaler.fit_transform(data.drop(['target','quality'], axis=1)), columns=data.drop(['target','quality'], axis=1).columns)


y = data['target']

xgboost_model = xgboost.XGBClassifier(n_estimators=128, eval_metric="logloss")

cv = StratifiedKFold(n_splits=3)

xgboost_model.fit(X, y)

with open('./model.pkl', "wb") as fd:
    pickle.dump(xgboost_model, fd)
    
class Collector:
    def __init__(self, ):
        self.metric_accuracy = Gauge('accuracy', 'accuracy score for model')
        self.metric_f1 = Gauge('f1', 'f1 score for model')
        self.metric_precision = Gauge('precision', 'precision score for model')
        self.metric_recall = Gauge('recall', 'recall score for model')
        self.metric_request_time = Histogram('request_processing_seconds',
                       'Time spent processing request')
        self.metric_sample_count = Counter('sample_count',
                       'counter for processed samples')

    def collect_info(self, accuracy, f1, precision, recall, sample_count):
        self.metric_accuracy.set(accuracy)
        self.metric_f1.set(f1)
        self.metric_precision.set(precision)
        self.metric_recall.set(recall)
        self.metric_sample_count.inc(sample_count)


collector = Collector()

# request_time = Summary('request_processing_seconds',
#                        'Time spent processing request')

# g = Gauge('accuracy', 'accuracy score for model')


@collector.metric_request_time.time()
def continue_learning():
    with open('./model.pkl', "rb") as fd:
            loaded  = pickle.load(fd)
            
    sample_count = np.random.randint(100, 400, 1)
    indexes = np.random.randint(0, len(data.index), sample_count)
    
    iteration_data = data.iloc[indexes]
    X = pd.DataFrame(s_scaler.fit_transform(iteration_data.drop(['target','quality'], axis=1)), columns=iteration_data.drop(['target','quality'], axis=1).columns)
    y = iteration_data['target']
    
    
    xgboost_model = xgboost.XGBClassifier(n_estimators=16, eval_metric="logloss")
    xgboost_model.fit(X, y, eval_set=[(X, y)], xgb_model=loaded)
    
    cv_score_accuracy = cross_val_score(xgboost_model, X, y, cv=cv, scoring='accuracy')
    cv_score_f1 = cross_val_score(xgboost_model, X, y, cv=cv, scoring='f1')
    cv_score_precision = cross_val_score(xgboost_model, X, y, cv=cv, scoring='precision')
    cv_score_recall = cross_val_score(xgboost_model, X, y, cv=cv, scoring='recall')
    
    collector.collect_info(cv_score_accuracy.mean(), cv_score_f1.mean(), cv_score_precision.mean(), cv_score_recall.mean(), sample_count)
    
    # print('accuracy score on cross validation: ', cv_score.mean())
    
    # collector.collect_info(cv_score.mean())
    
    with open('./model.pkl', "wb") as fd:
        pickle.dump(xgboost_model, fd)    
        

for i in range(1000):
    continue_learning()