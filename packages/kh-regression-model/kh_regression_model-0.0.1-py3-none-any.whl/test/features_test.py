from regression_model.processing.feaures import (
    Mapper,
    RareCategoricalEncoder,
    CategoricalEnocder,
    TemporalVariableTransformation
)
from regression_model.config.core import config
import unittest

class TestTemporalVariableTransformation(unittest.TestCase):

    def test_variables_not_list(self):
        """Test case where variables is not in list - should raise a error"""
        with self.assertRaises(ValueError):
            TemporalVariableTransformation(variables="not a list", reference_variable="variable")

    def test_variables_is_list(self):
        "Test case where variables in list - should not raise a error"
        
        try:
            TemporalVariableTransformation(variables=["var1", "var2"], reference_variable="varable")
        except ValueError:
            self.fail("CategoricalEncoder raised value error unexpectedly")

    def test_transformation(self):
        "Test case to check transformation"
        transformer = TemporalVariableTransformation(
            variables=config.model_conf.temporal_vars,
            reference_variable=config.model_conf.ref_var
        )

        sample_input_data = {
            "YrSold": 2010,
            "YearRemodAdd": 1961
        }

        self.assertEqual(sample_input_data["YearRemodAdd"],1961)

        # when 

        subject = transformer.transform(sample_input_data)

        # then 
        self.assertEqual(subject["YearRemodAdd"], 49)



if __name__ == "__main__":
    unittest.main()

    



