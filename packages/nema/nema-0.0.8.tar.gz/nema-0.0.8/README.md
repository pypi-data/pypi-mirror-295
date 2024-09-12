# Nema Python Extension

This library provides a set of classes and functions to work with Nema artifacts.

It provides both the `nema` library, as well as the `nema-python` CLI.

## Installation

To install the Nema Python extension, run the following command:

```bash
pip install nema
```

This installs both the `nema` python package and the `nema-python` CLI tool.

Nema works for Python 3.8 and above.

## Usage

To login into Nema, run `nema-python login` from the command line. This will prompt you to enter your Nema credentials.

Then run `nema-python init` which will prompt you for your Nema project URL and create a `nema.toml` file in your current directory.

`nema-python workflow init` will then create this workflow in Nema.

You can then create the actual code that you want to run, for example:

```python
from nema.data.data_properties import IntegerValue, ArbitraryFile
from nema.data.tabular.tabular_data_properties import CSVData
from nema.data.plots.figure_data_properties import Image
from nema.data import Data, FileData, DataCollection
from nema.analysis import run

import pandas as pd


def run_workflow():

    collection = DataCollection(
        { # note these need to exist in Nema and the global_id needs to match
            "test_data_1": Data.init_from_cloud(global_id=1, data_class=IntegerValue),
            "test_data_2": Data.init_from_cloud(global_id=2, data_class=IntegerValue),
            "result_data": Data.init_from_cloud(global_id=3, data_class=IntegerValue),
            "result_table": FileData.init_from_cloud(global_id=4, data_class=CSVData),
            "image_result": FileData.init_from_cloud(global_id=5, data_class=Image),
            "an_arbitrary_file": FileData.init_from_cloud(global_id=6, data_class=ArbitraryFile),
        }
    )

    @run(data_collection=collection, enable_API_calls=True)
    def simple_analysis():
        result_value = IntegerValue(
            collection.test_data_1.value * collection.test_data_2.value
        )

        collection.result_data.update_data(result_value)

        # output a table
        resulting_table = pd.DataFrame(
            {
                "test_data_1": [collection.test_data_1.value],
                "test_data_2": [collection.test_data_2.value],
                "result": [result_value.value],
            }
        )
        collection.result_table.update_data(CSVData(data=resulting_table))
        collection.result_data.update_data(result_value)

        # Create a simple plot
        x = np.linspace(0, 10, 100)
        y = np.sin(x)

        plt.plot(x, y, label="Sine Wave")
        plt.title("Simple Sine Wave")
        plt.xlabel("x-axis")
        plt.ylabel("y-axis")
        plt.legend()

        plt.savefig(collection.image_result.get_file_name_to_save())

        # Read in an arbitrary file
        with collection.an_arbitrary_file("r") as f:
            print(f.read())

    result = simple_analysis()


if __name__ == "__main__":
    run_workflow()
```

To run this workflow locally and upload the results to Nema, run `nema-python workflow run`.
