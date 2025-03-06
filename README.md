# rust-ffi
An example of wrapping a Rust module with python package

## How to build?
Create a virtual environment:
```bash
virtualenv .venv
```

Instantiate virtual environment:
```bash
source .venv/bin/activate
```

Install requirements:
```bash
pip install -r requirements.txt
```

Generate the python wrapper for the rust library
```bash
maturin develop
```

Run the code
```bash
python rust-ffi.py
```