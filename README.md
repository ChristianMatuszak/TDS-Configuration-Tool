# TSD-Configuration-Tool
Edit a jsonfile by inspecting its json schema.

It's mostly designed around TDS. It queries the TDS executable for a configuration path and the respective schema.

From that it sets up a GUI that allows editing and saving the configuration values.

Updating the schema in TDS will automatically create new sections / fields in the configuration tool.

![grafik](https://github.com/tessonics/json-configurator/assets/75343504/bcf964e3-e4db-41ee-95b8-b0a73e44757e)

## How to run

Install the prerequesites:
```
pip install -r requirements.txt
```

Run the executable:
```
python src/file_gui.py
```


## Package the executable

```
pyinstaller --onefile -n "tds_configuration_tool" --add-data "resources/favicon.png;resources" --add-data "resources/azure.tcl;resources" --add-data "resources/theme;resources/theme" --noconsole src/file_gui.py
```

## CI/CD

There is a [github action](.github/workflows/python-test-deploy.yml) that is run on a small runnner in Germany. It builds and packages the executable on every push to main/pr or version tag push.


