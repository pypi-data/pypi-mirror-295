# mcpath

[![PyPI](https://img.shields.io/pypi/v/mcpath)](https://pypi.org/project/mcpath/)
[![Python](https://img.shields.io/pypi/pyversions/mcpath)](https://www.python.org/downloads//)
![Downloads](https://img.shields.io/pypi/dm/mcpath)
![Status](https://img.shields.io/pypi/status/mcpath)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Issues](https://img.shields.io/github/issues/legopitstop/mcpath)](https://github.com/legopitstop/mcpath/issues)

Get paths to Minecraft Java, Bedrock, Preview, and Education Edition folders.

## Supported Platforms

|             | Java | Bedrock | Preview/Beta | Education |
| ----------- | ---- | ------- | ------------ | --------- |
| **Android** | ❌   | ✅      | ❌           | ❌        |
| **Darwin**  | ✅   | ❌      | ❌           | ❌        |
| **iOS**     | ❌   | ❌      | ❌           | ❌        |
| **Linux**   | ✅   | ❌      | ❌           | ❌        |
| **Windows** | ✅   | ✅      | ✅           | ✅        |

## Installation

Install the module with pip:

```bat
pip3 install mcpath
```

Update existing installation: `pip3 install mcpath --upgrade`

## Examples

```Python
from mcpath import java

print(java.worlds)
```
