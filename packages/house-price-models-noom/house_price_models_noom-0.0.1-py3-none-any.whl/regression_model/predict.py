import typing as t

import numpy as np
import pandas as pd

from regression_model import __version__ as _version
from regression_model.config.core import DATASET_DIR, config
from regression_model.processing.data_manager import load_pipeline, load_dataset
from regression_model.processing.validation import validate_inputs

pipeline_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
_price_pipe = load_pipeline(file_name=pipeline_file_name)


def make_predictions(*, input_data: t.Union[pd.DataFrame, dict]) -> dict:

    """Maeke a prediction using a save model pipeline"""

    data = pd.DataFrame(input_data)
    validated_data, error = validate_inputs(input_data=data)

    results = {"prediction": None, "version": _version, "errors": error}

    if not error:
        prediction = _price_pipe.predict(validated_data[config.model_conf.features])
        results = {
            "predictions": [np.exp(pred) for pred in prediction],
            "version": _version,
            "error": error
        }

    return results

data = load_dataset(filename=config.app_config.training_data_file)
print(make_predictions(input_data=data.sample(1)), data.sample(1)["SalePrice"].values)