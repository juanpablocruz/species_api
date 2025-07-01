from IPython.display import display
from IPython.display import JSON

from speciesnet import DEFAULT_MODEL
from speciesnet import SpeciesNet

from typing import Union, Tuple, Optional

def print_predictions(predictions_dict: dict) -> None:
    print("Predictions:")
    for prediction in predictions_dict["predictions"]:
        print(prediction["filepath"], "=>", prediction["prediction"])

model = SpeciesNet(DEFAULT_MODEL)
def predict(filepath: str, location: Union[str, Tuple[float, float]], verbose: Optional[bool] = False):
    if isinstance(location, str):
        country = location
        lat, lon = None, None
    else:
        country = None
        lat, lon = location
    predictions_dict = model.predict(
        instances_dict={
            "instances": [ {
                "filepath":  filepath,
                "country": country,
                "lat": lat,
                "lon": lon
            }]
        }
    )
    if predictions_dict and verbose:
        print_predictions(predictions_dict)
        display(JSON(predictions_dict))

    return predictions_dict if predictions_dict else []
