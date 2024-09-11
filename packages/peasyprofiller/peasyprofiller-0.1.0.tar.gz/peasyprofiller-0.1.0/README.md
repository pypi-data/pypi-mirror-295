# Peasy Profiller

This is a simple and easy-to-use profiller for Python applications that will generate CSV files that indicate the amount of time your application spent in different contexts

## Quickstart

To install, run

```bash
pip install --upgrade pip
pip install peasyprofiller
```

To use it in a program, import it, call the start function at the start of the section you want to profile and stop at the end of that section. Time of sections with the same context will be added.

To save the data collected, call the save_csv function with the desired save path.


```python
from peasyprofiller.profiller import profiller as pprof

pprof.start("Name of my activity")

# Some processing happens here

pprof.stop("Name of my activity")
pprof.save_csv("path_to_save.csv")
```

## Example

You can run the example at `peasyprofiller/tests/fibonacci.py` with the following command:

```
python -m peasyprofiller.tests.fibonacci <N> <SAVE_PATH>.csv
```

The generated CSV should look like this:

```csv
Profiller,Fibonacci
6.87e-05,6.7745289
```