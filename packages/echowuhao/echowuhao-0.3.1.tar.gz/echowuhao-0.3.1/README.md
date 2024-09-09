
## dev and build

uv develop and build using uv is good

## uploading

uvx twine upload dist/*

### install

using pipx

uvx does not work with package with mutiple scripts(?)

```sh
➜  ✗ pipx install echowuhao
⚠️  File exists at /Users/hwu/.local/bin/auto_commit and points to
    /Users/hwu/.local/share/uv/tools/echowuhao/bin/auto_commit, not /Users/hwu/.local/pipx/venvs/echowuhao/bin/auto_commit.
    Not modifying.
⚠️  File exists at /Users/hwu/.local/bin/hello and points to /Users/hwu/.local/share/uv/tools/echowuhao/bin/hello, not
    /Users/hwu/.local/pipx/venvs/echowuhao/bin/hello. Not modifying.
  installed package echowuhao 0.2.0, installed using Python 3.12.5
  These apps are now globally available
    - auto_commit (symlink missing or pointing to unexpected location)
    - hello (symlink missing or pointing to unexpected location)
done! ✨ 🌟 ✨
```

## develop tool

uv build


## TODO:

a full tutorial on how to create script and dist using pypi and install using uvx
