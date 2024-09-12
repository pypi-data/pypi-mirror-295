# cypkgdemo

cypkgdemo 是一个用于演示对 Cython 模块的编译、测试、打包和安装的包。

## 使用方法

可以通过 `pip install cypkgdemo` 将 cypkgdemo 安装至 "root" package 下（建议使用虚拟环境），安装好后通过 `import cypkgdemo` 或者 `from cypkgdemo import ...` 即可调用包中函数。

若通过源文件安装，则在 pyproject.toml 所在目录运行 `pip install .` 命令即可。

若进行二次开发，可增加 `-e` 选项以便调试。若要进行单元测试，则需要附加安装 dev 依赖，即运行如下命令：
```shell
pip install -e ".[dev]"
```
之后使用如下命令可运行单元测试：
```shell
python -m unittest discover -p "*test.py"
```
> 上述两条命令使用引号包裹 `.[test]` 和 `*test.py` 是为了避免 zsh 将它们当作正则表达式从而导致意外的错误。若在其他 shell 下，或已在 .zshrc 中配置了 `setopt no_nomatch`，则无须使用引号包裹。

> 注意，本包不再支持使用 `python setup.py build_ext --inplace` 命令生成链接库。

## 说明

根据 [PEP 518](https://peps.python.org/pep-0518/)，项目中包的基本信息、依赖关系等均在 pyproject.toml 中说明。而为了支持构建 Cython Extension，仍旧保留了 setup.py 文件，其中包含了如何为每一个 .pyx 文件构造 Extension 的方法，你可以根据自己的需求对其进行修改。

## 开发的一般步骤

### 编写源代码

参照[官方教程](https://packaging.python.org/en/latest/tutorials/packaging-projects/)，开发的 Python 包的源代码放在 src/cypkgdemo 目录下。

一般而言，对于一个包含了多个 Python 和 Cython 源文件的项目，每个模块（无论是纯 Python 还是 Cython 模块）在导入同一项目下的其他模块时，都应当采用相对于最顶层包的绝对路径（例如，在这里就是 `from cypkgdemo.some_module import / cimport ...`）。

每个 Cython .pyx 源文件可编译出一个 Cython 扩展模块，该模块可通过如下方式暴露接口给其他 Python/Cython 模块使用：

| 暴露的接口 | 其他哪些模块可以使用 | 使用方式 |
| :------: | :-------  | :------- |
| Python 对象（包括 `cpdef` 函数） | 所有模块 | 通过 `import` 命令 |
| 在 .pxd 文件声明的 `cdef`/`cpdef` 函数 | Cython 模块 | 通过 `cimport` 命令 |
| 未在 .pxd 文件声明的 `cdef` 函数 | 无 | —

因此，若要让编写的 C/C++ 函数能被第三方库访问，除了要在 .pyx 文件中给出实现外，还要在同名的 .pxd 文件中声明函数接口，并确保该 .pxd 文件会被打包到安装包中。

> 当前默认所有 .pxd 文件都会被安装，参见 pyproject.toml `[tool.setuptools.package-data]` 部分。若要指定某些 .pxd 文件不被安装，则可通过类似如下代码实现：
> ```toml
> [tool.setuptools.exclude-package-data]
> cypkgdemo = ["sa.pxd"]
> ```

Cython 要求，Cython 扩展库的名称必须与源文件的无后缀名称全同（含路径），即对于目录 src/cypkgdemo/some/parent/subpackage 下名为 extmod1.pyx 的 Cython 源文件，可编译出的 Cython 扩展库必须名为 `cypkgdemo.some.parent.subpackage.extmod1`，否则模块中的内容无法被导入。本包通过 setup.py 中的 `make_extension` 函数实现该要求。

### 编译与测试

正如[使用方法](#使用方法)部分所述，可以通过如下命令完成可编辑安装和单元测试：
```shell
pip install -e ".[test]"
python -m unittest discover -p "*test.py"
```
你可以按需在 tests 文件夹下增加更多的单元测试内容。

### 打包

使用 build 包完成分发前的打包工作。对此，首先需要安装 build：
```shell
pip install build -i https://pypi.tuna.tsinghua.edu.cn/simple
```

然后在 pyproject.toml 所在目录下运行：
```shell
export PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple  # 可选
python -m build
```
此时会在 dist/ 目录下生成发行包。

### 上传

首先，安装工具包 twine：
```shell
pip install twine
```

运行 twine check，检查发行包完整性：
```shell
twine check dist/*
```

上述检查通过后，可采用以下步骤上传至 PyPI:
```python
# Upload to Test PyPI
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
# To PyPI
twine upload dist/*
```

注意，如果是发布源文件（`python setup.py sdist`），开发者应当安装有 Cython，以便从 Cython 源文件生成 C/C++ 文件，进而将 C/C++ 文件包含进源发行包中（这样用户可以不用安装有 Cython）。

采用以下方式安装之前上传的包：
```python
# From Test PyPI
pip install --index-url https://test.pypi.org/simple/ cypkgdemo
# From PyPI 
pip install cypkgdemo
```
