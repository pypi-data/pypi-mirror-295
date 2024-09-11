# example-code

This example code is simply to demonstrate how Open Source Python code should be written, documented and structured.   
The file structure should be organized as of the following:

```
src/
├─ requirements.txt
├─ simple_service/
│  ├─ __init__.py
│  ├─ simple_service.py
README.md
LICENSE
```

### How the code should be written and documented
The code should include comments and proper documentation. **Use Docstrings**   

Please refer to the documentation in the `simple_service.py` file of this package and to [Documenting Python Code: A Complete Guide](https://realpython.com/documenting-python-code).

To write proper and understandable code, for you and for others to read, you may also refer to [How to Write Beautiful Python Code With PEP 8](https://realpython.com/python-pep8/)


### How to build and distribute the code
Please refer to the [ops-py-generate-pyproject](https://pypi.org/project/ops-py-generate-pyproject) documentation.