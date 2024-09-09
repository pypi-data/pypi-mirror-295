https://pypi.org/project/fast-knifes/

## 包升级
修改版本号
rm -r dist && python -m build && python -m twine upload dist/*

## 项目更新包
pip install fast-knifes --index-url https://pypi.python.org/simple -U

## 额外需要安装三方包

### ase
- cryptography

