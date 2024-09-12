import numpy as np
import pandas as pd
import networkx as nx
from sklearn.ensemble import GradientBoostingRegressor
from dowhy.gcm.falsify import FalsifyConst, falsify_graph, plot_local_insights, run_validations, apply_suggestions
from dowhy.gcm.independence_test.generalised_cov_measure import generalised_cov_based
from dowhy.gcm.util import plot
from dowhy.gcm.util.general import set_random_seed
from dowhy.gcm.ml import SklearnRegressionModel

def create_gradient_boost_regressor(**kwargs) -> SklearnRegressionModel:
    return SklearnRegressionModel(GradientBoostingRegressor(**kwargs))

def Gfalsify(data_path, graph_path, to_plot=True) -> str:
    set_random_seed(1332)
    data = pd.read_csv(data_path)
    g = nx.read_gml(graph_path)
    def gcm(X, Y, Z=None):
        return generalised_cov_based(X, Y, Z=Z, prediction_model_X=create_gradient_boost_regressor,
                                        prediction_model_Y=create_gradient_boost_regressor)
    result = falsify_graph(g, data, n_permutations=100,
                                    independence_test=gcm,
                                    conditional_independence_test=gcm,
                                    plot_histogram=to_plot)

    return result