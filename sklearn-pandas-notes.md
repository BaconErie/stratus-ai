# Sklearn and Pandas Notes

# Read dataframe from CSV

```python
df = pd.read_csv("new_data.csv")
```

# Test and train dataset splitting

```python
from sklearn.model_selection import train_test_split

train_set, test_set = train_test_split(BIG_DATASET, test_size=0.2, random_state=42)
```

# Removing columns with `pd.DataFrame.drop`

By default makes a copy, use `inplace=True` to not make a copy

`axis=1` means to drop columns, `axis=0` means to drop rows

```python
from pd import DataFrame

new_dataframe = dataframe.drop(labels=['COLUMN NAMES'], axis=1)
```

# Getting columns from DataFrame

```python
from pd import DataFrame

dataframe['COLUMN NAME']
```

# LabelEncoder

Turns label in words into numbers

```python
from sklearn.preprocessing import LabelEncoder
```

## Fitting

Pass in your y dataframe

```python
label_encoder = LabelEncoder()
label_encoder.fit(y_dataframe)
```

## Transform

Turn all the labels into numbers

```python
label_encoder.transform(y_dataframe)
```

# Accuracy score

```python
sklearn.metrics.accuracy_score(y_true, y_pred, *, normalize=True, sample_weight=None)
```

# Confusion matrix

```python
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt

ConfusionMatrixDisplay.from_predictions(y_actual, y_pred, normalize='true')
plt.show()
```

# Precision and Recall

Precision: What percent of positives are actually positives; Doesn't care about 
false negatives

Calculated with TP / (TP + FP)

PROBLEM: Model can just make everything false negative, except to accurately
predict one, this results in very high precision

To solve this use recall:

Recall: How many positives does the thing actually identify, TP/ (TP+FN)

```python
from sklearn.metrics import precision_score, recall_score

precision = precision_score(y_actual, y_predicted)
recall = recall_score(y_actual, y_predicted)
```

# F1 score

Harmonic mean of precision and recall, high F1 means similar precision and recall
and both are good

Good for comparing classifiers

```python
from sklearn.metrics import f1_score
f1_score(actual, predicted)
```

# Precision-Recall tradeoff

At least for SGD classifiers (which by default use SVMs) higher precision
means a lower recall, and vice versa

You can be more correct about your positives (higher precision) but only if you
are more careful, and say negative to more things (lower recall)