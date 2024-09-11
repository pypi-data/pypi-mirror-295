https://pypi.org/project/knifes/

## 包升级
1. 修改版本号
rm -r dist && python -m build && python -m twine upload dist/*

## 项目更新包
pip install knifes --index-url https://pypi.python.org/simple -U

## 额外需要安装三方包

### ase
- cryptography

### sms
- tencentcloud-sdk-python==3.0.600

### luban
- Pillow
- pillow-heif

### alarm、auth、decorators、envconfig、misc、results、sms
- django

### 注意
谨慎使用 `validators.url` , 该方法较严格, 如会判断 `https://m.toutiao.com/is/iNmDd2SG/?=` 为非法url