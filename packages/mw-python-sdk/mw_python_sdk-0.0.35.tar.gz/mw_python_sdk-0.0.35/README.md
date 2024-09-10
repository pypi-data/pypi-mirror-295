# mw-sdk-python

## 简介
`mw-sdk-python` 是一个用于与 Heywhale 平台交互的 Python SDK，旨在简化数据集的获取和管理。

## 安装

```bash
pip install mw-sdk-python
```

## 示例代码

以下是一个示例代码，展示了如何使用 `mw-sdk-python` 获取数据集的详细信息。

```python
from mw_python_sdk import download_dir
download_dir("66b08ec9898e74a8232bb2d1")
```

## 环境变量

- `MW_TOKEN`: 用于身份验证的令牌。如果未提供 token 参数，SDK 将使用此环境变量。
- `HEYWHALE_HOST`: Heywhale 平台的主机地址（可选）。默认值为 `https://www.heywhale.com`。

## 开发者

本地可编辑安装
```bash
pip install -e .
# 如果需要安装llm相关的功能，需要安装可选依赖。
pip install -e '.[llm]'
```
构建方式，如果是 0.1.0版本。

```python
python -m build
python -m twine upload dist/mw_python_sdk-0.1.0*
```

### 兼容问题

目前支持python3.7，注意一下几点：

1. `dataclass`在3.7引入，3.6用不了。
2. `|` 操作符Union的语法糖在3.9中不支持，3.10支持，所以不要使用这个语法糖。
3. `/` 切分位置参数和关键字参数是3.8的，也不要用。


管理于类型的问题，Python的计划是：

PEP 585—Type Hinting Generics In Standard Collections started a multiyear process to improve the usability of generic type hints. We can summarize that process in four steps:
1. Introduce from __future__ import annotations in Python 3.7 to enable the use of standard library classes as generics with list[str] notation.
2. Make that behavior the default in Python 3.9: list[str] now works without the future import.
3. Deprecate all the redundant generic types from the typing module.10 Depreca‐ tion warnings will not be issued by the Python interpreter because type checkers should flag the deprecated types when the checked program targets Python 3.9 or newer.
4. Remove those redundant generic types in the first version of Python released five years after Python 3.9. At the current cadence, that could be Python 3.14, a.k.a Python Pi.

所以从3.14开始是没有这些类型的module了，这个在之后是要考虑的东西。
## 许可证
MIT
