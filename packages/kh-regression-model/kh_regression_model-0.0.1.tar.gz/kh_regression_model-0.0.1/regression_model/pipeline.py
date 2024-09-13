"""
Model Pipeline
""" 
from sklearn.preprocessing import MinMaxScaler, Binarizer
from sklearn.linear_model import Lasso
from sklearn.preprocessing import MinMaxScaler, Binarizer
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectFromModel
from feature_engine.transformation import LogTransformer, YeoJohnsonTransformer
from feature_engine.imputation import AddMissingIndicator, MeanMedianImputer, CategoricalImputer
from feature_engine.wrappers import SklearnTransformerWrapper
from feature_engine.selection import DropFeatures
from sklearn.svm import SVR
from regression_model.config.core import config
from regression_model.processing.feaures import *




price_pipeline = Pipeline([
    # Missing Imputation
    ('missing_imputation', CategoricalImputer(
        imputation_method="missing", variables=config.model_conf.categorical_vars_with_na_missing)),

    # Frequent Imputation
    ('frequent_imputation', CategoricalImputer(
        imputation_method="frequent", variables=config.model_conf.categorical_vars_with_na_frequent)),

    # Missing Indicator
    ('missing_indicator', AddMissingIndicator(variables=config.model_conf.numerical_vars_with_na)),

    # Mean Imputation
    ('mean_imputation', MeanMedianImputer(
        imputation_method="median", variables=config.model_conf.numerical_vars_with_na)),

    # Elapsed Time
    ('elapsed_time', TemporalVariableTransformation(
        variables=config.model_conf.temporal_vars, reference_variable=config.model_conf.ref_var)),

    # Drop Feature
    ('drop_feature', DropFeatures(features_to_drop=[config.model_conf.ref_var])),

    # Log Transformation 
    ('log', LogTransformer(variables=config.model_conf.numericals_log_vars)),

    # Binarizer Transformation
    ('binarizer', SklearnTransformerWrapper(
        transformer=Binarizer(threshold=0), variables=config.model_conf.binarize_vars)),

    # Qaulity Mapping
    ('mapper_qual', Mapper(
        variables=config.model_conf.qual_vars, mappings=config.model_conf.qual_mappings)),

    # Exposer Mapping
    ('mapper_exposure', Mapper(
        variables=config.model_conf.exposure_vars, mappings=config.model_conf.exposure_mappings)),

     # Finish Mapping
    ('mapper_finish', Mapper(
        variables=config.model_conf.finish_vars, mappings=config.model_conf.finish_mappings)),

    # Garage Mapping
    ('mapper_garage', Mapper(
        variables=config.model_conf.garage_vars, mappings=config.model_conf.garage_mappings)),


    # Rare Label Encoder
    ('rare_label_enocder', RareCategoricalEncoder(variables=config.model_conf.categorical_vars)),

    # Categorical Encoder'
    ('categorical_enocder', CategoricalEnocder(variables=config.model_conf.categorical_vars)), 

    # Scaler
    ('scaler', MinMaxScaler()),
    
    # Model
    ('Lasso', SVR())
])

