# \R
 A module for printing messages using /r

## Installation
```bash
pip install slashr
```

## Usage

### Using with
```python
from slashr import SlashR

with SlashR() as sr:
    for i in range(10):
        sr.print(i)
```

### Using object
```python
from slashr import SlashR

sr = SlashR()

sr.init()

for i in range(10):
    sr.print(i)

sr.exit()  # Optional if you want to stop slashr entirely

```