# Expense Analysis Notebook

Import from src modules:

```python
import sys
sys.path.insert(0, '../')
from src.analysis import load_and_clean, category_summary, key_metrics
df = load_and_clean('../data/expenses.csv')
```
