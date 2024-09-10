# levenshtein_rs
Given `x: list[str]` and `y: list[str]`, this package calculates the Levenshtein distance between `a` and `b`.

This is a fork of https://github.com/wooorm/levenshtein-rs with additional tests.

## Usage
```python
from levenshtein_rs import levenshtein_list
a = "Testing one two three"
b = "one two three four"
print(levenshtein_list(a.split(), b.split()))
# 2
```

This project uses the MIT license.

## Building from source

This is a Rust project wrapped with maturin.

`nix develop` will install dependencies (direnv is supported). Alternatively, you can install cargo using rustup and install maturin using pip.

`maturin develop` will compile the project and install it into the current Python environment.

`maturin publish` will publish to PyPi.

To upload an additional wheel for a specific Python version, use:
```
maturin publish --skip-existing -i 3.10
```
