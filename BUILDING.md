### Pyinstaller build

* `git pull`
* Activate virtualenv (on Windows `.venv\Scripts\activate.bat`)
* Remove `bcompiler-engine` and `datamaps` (`pip uninstall bcompiler-engine
    datamaps`)
* `pip install -e .` to reinstall in developer mode
* `pyinstaller cli.py --name "dm" --onefile` to create the executible in `dist`
    directory.
* Upload to target download site

