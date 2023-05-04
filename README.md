# kektris

4-quarter tetris created by [Pyxel](https://github.com/kitao/pyxel)

Typicaly: `pip install -e .[dev]`

## Pyxel cli

- `pyxel run PYTHON_SCRIPT_FILE(.py)`
- `pyxel watch WATCH_DIR PYTHON_SCRIPT_FILE(.py)`
- `pyxel play PYXEL_APP_FILE(.pyxapp)`
- `pyxel edit [PYXEL_RESOURCE_FILE(.pyxres)]`
- `pyxel package APP_DIR STARTUP_SCRIPT_FILE(.py)`
- `pyxel app2exe PYXEL_APP_FILE(.pyxapp)`
- `pyxel app2html PYXEL_APP_FILE(.pyxapp)`

## Destribution

Create the Pyxel application file (.pyxapp) with the following command:

```sh
pyxel package APP_DIR STARTUP_SCRIPT_FILE
```

If the application should include resources or additional modules, place them in the application directory.

The created application file can be executed with the following command:

```sh
pyxel play PYXEL_APP_FILE
```

Pyxel application file also can be converted to an executable or an HTML file with the pyxel `app2exe` or pyxel `app2html` commands.

## Play the game

[wasm launcher](https://kitao.github.io/pyxel/wasm/launcher/?play=KonstantinKlepikov.kektris.example.kektris)
