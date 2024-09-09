# common_fn_chunk

[![PyPI - Version](https://img.shields.io/pypi/v/common-fn-chunk.svg)](https://pypi.org/project/common-fn-chunk)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/common-fn-chunk.svg)](https://pypi.org/project/common-fn-chunk)

-----

## Table of Contents

- [common\_fn\_chunk](#common_fn_chunk)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [License](#license)

## Installation

```console
pip install common-fn-chunk
```

## Usage
```python
from common_fn_chunk import chunk
r = range(1000)
print(len(chunk(r)))
print(len(chunk(r, 100)))
```

## License
`common-fn-chunk` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
