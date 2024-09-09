# susi-lib

Python library for [SuŠi](https://susi.trojsten.sk) organizers.

## Overview

Provides classes and functions to more easily convert between
encodings used in puzzle hunting, to encapsulate regular expressions and to
find words that pass given criteria.

## Install

```bash
pip install susi-lib
```

## Usage

```python
# import everything, access in code susi_lib.[whatever]
import susi_lib
```

```python
from susi_lib import Finder, RegEx, create_regex, Selection
# types
from susi_lib.types import Braille, Morse, NumberSystems, Symbols, Semaphore
# functions
from susi_lib.functions import decode, encode, Encoding, is_palindrome
```
