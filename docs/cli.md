```{include} _templates/nav.html
```

# Command-line usage

The Python library is also installed as a command-line interface. You can run it from your terminal like so:

The command has the same options as the Python API.

```{eval-rst}
.. click:: savepagenow.api:cli
   :prog: savepagenow
   :nested: full
```

## Developing the CLI

The command-line interface is implemented using Click and setuptools. To install it locally for development inside your virtual environment, run the following installation command, as [prescribed by the Click documentation](https://click.palletsprojects.com/en/7.x/setuptools/#setuptools-integration).

```bash
pip install --editable .
```
