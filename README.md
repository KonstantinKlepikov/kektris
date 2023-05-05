# kektris

4-quarter tetris created by [Pyxel](https://github.com/kitao/pyxel)

## Development and destribution

Typicaly: `pip install -e .[dev]`

Available make cli:

```sh
make test
make run
make pypi-test
make pypi
make build-example
```

When `build-example` - result is propogated to folder example - here is html-launcher and application file (.pyxapp).

Pyxel cli:

```sh
pyxel run PYTHON_SCRIPT_FILE(.py)
pyxel watch WATCH_DIR PYTHON_SCRIPT_FILE(.py)
pyxel play PYXEL_APP_FILE(.pyxapp)
pyxel edit [PYXEL_RESOURCE_FILE(.pyxres)]
pyxel package APP_DIR STARTUP_SCRIPT_FILE(.py)
pyxel app2exe PYXEL_APP_FILE(.pyxapp)
pyxel app2html PYXEL_APP_FILE(.pyxapp)
```

## Play the game in web

[wasm launcher](https://kitao.github.io/pyxel/wasm/launcher/?play=KonstantinKlepikov.kektris.example.kektris)
