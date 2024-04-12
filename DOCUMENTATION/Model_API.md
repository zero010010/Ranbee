# Model API Documentation

This API provides endpoints for setting up data, training models, evaluating metrics, and making predictions.

## Endpoints

### Setup

**URL:** `/setupv0`


**Parameters:**

- `red` (str): Specify `yes` to apply dimensionality reduction using SelectKBest, or `no` to skip dimensionality reduction.

**Description:**

This endpoint performs the setup from the historical data, separating it into train and test sets. The `red` parameter determines whether dimensionality reduction is applied using SelectKBest or not.

**Response:**

If successful, returns a string confirming that the CSV files for `x_train`, `x_test`, `y_train`, and `y_test` have been downloaded.

### Train Model

**URL:** `/v1/train`


**Parameters:**

- `model` (str): Specify the model to train (`random`, `xgboost`, or `lstm`).
- `red` (str): Specify `yes` if dimensionality reduction was applied during setup, or `no` if it was not.

**Description:**

This endpoint trains the specified model (`random`, `xgboost`, or `lstm`) using the data prepared during the setup phase. The `red` parameter determines whether dimensionality reduction was applied or not.

**Input:**

- `model` (str): The model to be trained (`random`, `xgboost`, or `lstm`).
- `red` (str): Specify `yes` if dimensionality reduction was applied during setup, or `no` if it was not.

**Output:**

- A dictionary (JSON) with the model metrics and the path where the trained model has been saved.

**Response:**

If successful, returns a message indicating that the model has been trained and saved.

### Metrics

**URL:** `/v1/metrics`


**Parameters:**

- `model` (str): Specify the model to evaluate (`random`, `xgboost`, or `lstm`).
- `red` (str): Specify `yes` if dimensionality reduction was applied during setup, or `no` if it was not.

**Description:**

This endpoint evaluates the performance metrics of the specified model (`random`, `xgboost`, or `lstm`) on the test data. The `red` parameter determines whether dimensionality reduction was applied or not.

**Input:**

- `model` (str): The model to evaluate (`random`, `xgboost`, or `lstm`).
- `red` (str): Specify `yes` if dimensionality reduction was applied during setup, or `no` if it was not.

**Output:**

- A dictionary (JSON) with the classification report of the model, including metrics like mean squared error and R-squared.

**Response:**

Returns the performance metrics (e.g., mean squared error, R-squared) for the specified model.

### Predict

**URL:** `/v1/predict`


**Parameters:**

- `model` (str): Specify the model to use for prediction (`random`, `xgboost`, or `lstm`).
- `red` (str): Specify `yes` if dimensionality reduction was applied during setup, or `no` if it was not.
- `data` (list): A list containing the data to be predicted.

**Description:**

This endpoint is used to make predictions using the specified model and data. The `model` parameter specifies the model to use (`random`, `xgboost`, or `lstm`), the `red` parameter determines whether dimensionality reduction was applied during setup, and the `data` parameter contains the data to be predicted as a list.

**Input:**

- `model` (str): The model to use for prediction (`random`, `xgboost`, or `lstm`).
- `red` (str): Specify `yes` if dimensionality reduction was applied during setup, or `no` if it was not.
- `data` (list): A list containing the data to be predicted.

**Output:**

- A dictionary (JSON) with the predicted value.

**Response:**

Returns the predicted value(s) based on the provided data and specified model.





## Example Usage

Here's an example of how to use the API:

1. Set up the data by sending a GET request to `/setupv0?red=yes` or `/setupv0?red=no`.
2. Train a model by sending a GET request to `/v1/train?model=random&red=yes` or `/v1/train?model=xgboost&red=no`, etc.
3. Evaluate the model's performance by sending a GET request to `/v1/metrics?model=random&red=yes` or `/v1/metrics?model=xgboost&red=no`, etc.
4. Make predictions by sending a POST request to `/v1/predict?model=random&red=yes&data=0,0.1,0.2,...` or `/v1/predict?model=xgboost&red=no&data=0.3,0.4,0.5,...`, etc.

Note: Replace the values for `model`, `red`, and `data` with the appropriate values for your use case.
