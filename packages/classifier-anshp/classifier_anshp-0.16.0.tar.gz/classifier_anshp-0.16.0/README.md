# classifier-anshp

`classifier-anshp` is a simple linear classifier built using TensorFlow. This package includes a customizable linear model for binary classification and provides sample datasets for quick testing. The classifier is designed for flexibility and can be applied to custom datasets or pre-defined datasets, such as logical operations (AND, OR, XOR, XNOR).

## Features

- **Customizable Linear Classifier**: Modify input features, learning rate, and number of steps to train a linear model for binary classification.
- **Predefined Datasets**: Two sample datasets are included:
  - **Dataset 1**: Generates a synthetic dataset using multivariate Gaussian distributions.
  - **Dataset 2**: Logical operations (AND, OR, XOR, XNOR) for testing the classifier.
- **TensorFlow Backend**: Leverages TensorFlow for handling large-scale computations and efficient gradient-based optimization.

## Installation

You can install the package directly from PyPI:

```bash
pip install classifier-anshp
```

## Usage

### 1. Training a Custom Linear Classifier

The `clsfr` function allows you to train a linear classifier on your own dataset.

```python
from classifier_anshp import clsfr
import numpy as np

# Example dataset
inputs = np.array([[1.0, 2.0], [1.5, 1.8], [5.0, 8.0], [8.0, 8.0]])
val_true = np.array([0, 0, 1, 1])

# Train classifier with learning rate of 0.01 for 50 steps
val_pred, weights, bias = clsfr(inputs, val_true, lrn_rt=0.01, steps=50)

# Predicted output
print(f'Predictions: {val_pred}')
print(f'Weights: {weights}')
print(f'Bias: {bias}')
```

### 2. Using Sample Datasets

You can quickly test the classifier using the predefined datasets. The package provides two functions for generating data:

- **Dataset 1**: Generates a random binary classification dataset using multivariate normal distribution.
- **Dataset 2**: Logical operations like AND, OR, XOR, and XNOR.

```python
from classifier_anshp import dataset_1, dataset_2

# Example 1: Generate random dataset
inputs, val_true = dataset_1(sample_size=100)

# Example 2: Logical OR operation
inputs, val_true = dataset_2(num=2)  # 1 for AND, 2 for OR, 3 for XOR, 4 for XNOR
```

### 3. Running from Command Line

After installing the package, you can run the classifier or dataset generation directly from the command line.

#### Run Classifier:
```bash
classifier-anshp --inputs [[1,2],[3,4]] --val_true [0,1] --lrn_rt 0.01 --steps 50
```

#### Generate Dataset 1:
```bash
dataset-1 --sample_size 100
```

#### Generate Dataset 2 (Logical Operations):
```bash
dataset-2 --num 2
```

## Advantages Over scikit-learn

1. **TensorFlow-Based**: While `scikit-learn` provides efficient linear models, `classifier-anshp` is built using TensorFlow, which allows for more customization and seamless integration with larger deep learning frameworks.
  
2. **Gradient-Based Optimization**: The package uses TensorFlow’s gradient-based optimization, making it easy to modify and extend for more complex models beyond linear classifiers.

3. **Dataset Flexibility**: In addition to custom datasets, `classifier-anshp` comes with logical operation datasets, making it easier to test and experiment with common machine learning tasks.

4. **Custom Training Intervals**: The classifier provides detailed control over training steps, ensuring outputs are printed every 10 intervals, unlike scikit-learn, where training steps aren’t typically exposed.

## Limitations

- Primarily designed for binary classification tasks.
- Requires basic knowledge of TensorFlow to fully customize the model.

## License

This project is licensed under the MIT License. See the [LICENSE](license.txt) file for more details.

## Author

Anshuman Pattnaik  
Email: helloanshu04@gmail.com

For more details, visit the [GitHub Repository](https://github.com/ANSHPG/pypi-pkg-clsfr).
