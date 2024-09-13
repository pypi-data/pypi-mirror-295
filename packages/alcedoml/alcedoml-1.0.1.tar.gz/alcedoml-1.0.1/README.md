A small example package


## 打包


```python
python3 -m pip install --user --upgrade setuptools wheel


python setup.py bdist_wheel --universal

python setup.py sdist bdist_wheel  

pip install twine    

py -m twine upload dist/*

```


## pip安装

```python
pip install -i https://pypi.Python.org/simple/ alcedoml
```