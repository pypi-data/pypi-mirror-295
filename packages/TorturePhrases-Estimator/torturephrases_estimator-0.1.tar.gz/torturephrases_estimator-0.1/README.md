# TorturePhrases_Estimator

TorturePhrases_Estimator is a Python package that identifies tortured phrases in text using a pre-defined list of awkward or over-complicated phrases.

## Installation

You can install the package using pip:

```bash
pip install TorturePhrases_Estimator
```

## Usage

```python
from TorturePhrases_Estimator import identify_tortured_phrases

text = "We need to commence the project subsequent to our meeting."
tortured_phrases = identify_tortured_phrases(text)

print(tortured_phrases)
```
