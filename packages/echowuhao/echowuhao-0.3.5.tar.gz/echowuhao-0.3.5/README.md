# README

```sh
➜  ~ uv tool install echowuhao==0.3.4
Resolved 6 packages in 2.13s
Prepared 1 package in 192ms
Uninstalled 1 package in 7ms
Installed 1 package in 8ms
 - echowuhao==0.2.0 (from file:///Users/hwu/dev/py_lib/echowuhao)
 + echowuhao==0.3.4
Installed 2 executables: auto_commit, hello

➜  ~ uv tool list
echowuhao v0.3.4
- auto_commit
- hello
ruff v0.6.4
- ruff

➜  ~ hello
Hello from echowuhao!
```

## dev

uv develop and build using uv is good

```sh
uv sync
uv lock
uv build
```

## uploading

```sh
uvx twine upload dist/*
```

## install

### using uv

```sh
uv tool install echowuhao=0.3.4
```

or

### using pipx

```sh
pipx install echowuhao==0.3.4
```
