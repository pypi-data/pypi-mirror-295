from typing import List

import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class Mapper(BaseEstimator, TransformerMixin):
    """Mapping Quality Variables"""

    def __init__(self, variables, mappings):
        if not isinstance(variables, list):
            raise ValueError("variable should be in list")
        
        self.variables = variables
        self.mappings = mappings

    def fit(self, x, y=None):
        return self

    def transform(self, x):
        x = x.copy()
        for feature in self.variables:
            x[feature] = x[feature].map(self.mappings)
        return x


class RareCategoricalEncoder(BaseEstimator, TransformerMixin):
    """Encoder Rare Category Label"""

    def __init__(self, variables, tol=0.05):
        if not isinstance(variables, list):
            raise ValueError("Variales should be in list")
        self.tol = tol
        self.variables = variables

    def fit(self, X, y=None):
        # persist frequent labels in dictionary
        self.encoder_dict_ = {}

        for var in self.variables:
            # the encoder will learn the most frequent categories
            t = pd.Series(X[var].value_counts(normalize=True)) 
            # frequent labels:
            self.encoder_dict_[var] = list(t[t >= self.tol].index)

        return self

    def transform(self, X):
        X = X.copy()
        for feature in self.variables:
            X[feature] = np.where(
                X[feature].isin(self.encoder_dict_[feature]),
                                X[feature], "Rare")

        return X        


class CategoricalEnocder(BaseEstimator, TransformerMixin):
    """Encode Categorical Variable"""

    def __init__(self, variables):
        if not isinstance(variables, list):
            raise ValueError("variable should be in list")
        
        self.variables = variables
        self.encoder_dict_ = {}

    def fit(self, x, y):
        temp = pd.concat([x, y], axis=1)
        temp.columns = list(x.columns) + ["target"]

        for feature in self.variables:
            x = temp.groupby([feature])["target"].mean().sort_values(ascending=True).index
            self.encoder_dict_[feature] = {j: i for i, j in enumerate(x)}

        return self

    def transform(self, x):
        x = x.copy()
        for feature in self.variables:
            x[feature] = x[feature].map(self.encoder_dict_[feature])
        return x



class TemporalVariableTransformation(BaseEstimator, TransformerMixin):
    "elapsed Temporal Variable"

    def __init__(self, variables, reference_variable):
        if not isinstance(variables, list):
            raise ValueError("Variables should be in list")
        
        self.variables = variables
        self.reference_variable = reference_variable

    def fit(self, x, y):
        return self

    def transform(self, x):
        x = x.copy()
        for feature in self.variables:
            x[feature] = x[self.reference_variable] - x[feature]
        return x