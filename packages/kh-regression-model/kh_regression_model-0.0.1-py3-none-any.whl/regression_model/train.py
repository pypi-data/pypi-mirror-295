import numpy as np
from config.core import config
from sklearn.model_selection import train_test_split
from processing.data_manager import load_dataset, save_pipeline
from pipeline import price_pipeline

def run_training() -> None:
    """Train the model"""

    # reading taining data

    data = load_dataset(filename=config.app_config.training_data_file)
    x_train, x_test, y_train, y_test = train_test_split(data[config.model_conf.features], 
                     data[config.model_conf.target], 
                     test_size=config.model_conf.test_size,
                     random_state=config.model_conf.random_state)
    
    y_train = np.log(y_train)

    # fit the model
    price_pipeline.fit(x_train, y_train)
    save_pipeline(pipeline_to_persist=price_pipeline)

if __name__ == "__main__":
    run_training()
