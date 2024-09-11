import os
import argparse
import numpy as np
import pandas as pd
from datetime import datetime
from scipy.stats import pearsonr
from exgep.model import RegEXGEP
from exgep.preprocess import datautils
from sklearn.metrics import (r2_score, median_absolute_error, 
                             mean_squared_error)

jobnum = datetime.now().strftime('%Y%m%d%H%M%S')
print('Job number: ', jobnum)

def pearson_correlation(y, y_pred):
    corr, _ = pearsonr(y, y_pred)
    return corr

def root_mean_squared_error(y_true, y_pred):
    return np.sqrt(mean_squared_error(y_true, y_pred))

def parse_args():
    parser = argparse.ArgumentParser(description='EXGEP: Explainable Genotype-by-Environment Interactions Prediction')
    parser.add_argument('--Geno', type=str, default='./data/genotype.csv', help='Path to genotype CSV file')
    parser.add_argument('--Phen', type=str, default='./data/pheno.csv', help='Path to phenotype CSV file')
    parser.add_argument('--Soil', type=str, required=False, help='Path to soil CSV file')
    parser.add_argument('--Weather', type=str, required=False, help='Path to weather CSV file')
    parser.add_argument('--Test_frac', type=float, default=0.1, help='Fraction of the data to be used for testing')
    parser.add_argument('--N_splits', type=int, default=10, help='Number of splits for cross-validation')
    parser.add_argument('--N_trial', type=int, default=5, help='Number of optimization trials')
    parser.add_argument('--models_optimize', nargs='+', 
                        choices=['Dummy', 'LightGBM', 'XGBoost', 'CatBoost', 'BayesianRidge',
                                 'LassoLARS', 'AdaBoost', 'GBDT', 'HistGradientBoosting',
                                 'KNN', 'SGD', 'Bagging', 'SVR', 'ElasticNet', 'RF'], 
                        default=['XGBoost'],
                        help='Select models (Options: Dummy, LightGBM, XGBoost, CatBoost, BayesianRidge, LassoLARS,AdaBoost, GBDT, HistGradientBoosting, KNN, SGD, Bagging, SVR,ElasticNet,RF)'
    )
    parser.add_argument('--models_assess', nargs='+', 
                        choices=['Dummy', 'LightGBM', 'XGBoost', 'CatBoost', 'BayesianRidge',
                                 'LassoLARS', 'AdaBoost', 'GBDT', 'HistGradientBoosting',
                                 'KNN', 'SGD', 'Bagging', 'SVR', 'ElasticNet', 'RF'],
                        default=['XGBoost'],
                        help='Select models (Options: Dummy, LightGBM, XGBoost, CatBoost, BayesianRidge, LassoLARS,AdaBoost, GBDT, HistGradientBoosting, KNN, SGD, Bagging, SVR,ElasticNet,RF)'
                        
    )

    return parser.parse_args()

def main():
    args = parse_args()
    data = datautils.merge_data(
        args.Geno, args.Phen, args.Soil, args.Weather)
    X = pd.DataFrame(data.iloc[:, 3:])
    y = data['Yield']
    y = pd.core.series.Series(y)
    models_optimize = args.models_optimize
    models_assess = args.models_assess

    reg = RegEXGEP(
        y=y,
        X=X,
        test_size=args.Test_frac,
        n_splits=args.N_splits,
        n_trial=args.N_trial,  
        reload_study=True,
        reload_trial=True,
        write_folder=f'{os.getcwd()}/{jobnum}/result/',
        metric_optimise=r2_score,
        metric_assess=[median_absolute_error, mean_squared_error, r2_score,
                       pearson_correlation,root_mean_squared_error],
        optimization_objective='maximize',
        models_optimize=models_optimize,  
        models_assess=models_assess, 
        early_stopping_rounds=5,
        random_state=2024  
    )

    reg.train()
    print('Job ID: ', jobnum)

if __name__ == '__main__':
    main()
