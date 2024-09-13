import math
import unittest

import numpy as np
import pandas as pd

from regression_model.config.core import config, DATASET_DIR
from regression_model.predict import make_predictions
from regression_model.processing.data_manager import load_dataset

class Testprediction(unittest.TestCase):

    def test_make_prediction(self):

        # given
        expected_first_prediction_value = 113422
        expected_no_prediction = 1449
        sample_input_data = load_dataset(filename=config.app_config.test_data_file)
        # when 
        result = make_predictions(input_data=sample_input_data)

        # then
        predictions = result.get("predictions")
        print(len(predictions))
        self.assertIsInstance(predictions, list)
        self.assertIsInstance(predictions[0], np.float64)
        self.assertEqual(len(predictions), expected_no_prediction)
        self.assertAlmostEqual(predictions[0], expected_first_prediction_value, delta=10000)

if __name__ == "__main__":
    unittest.main()