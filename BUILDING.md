### Pyinstaller build

* `git pull`
* Activate virtualenv (on Windows `.venv\Scripts\activate.bat`)
    * (MAKE SURE YOU HAVE A PYTHON 3.7 virtualenv to hand!)
* Remove `bcompiler-engine` and `datamaps` (`pip uninstall bcompiler-engine
    datamaps`)
* `pip install -e .` to reinstall in developer mode
* `pyinstaller cli.py --name "dm" --onefile` to create the executible in `dist`
    directory.
* Upload to target download site

### Building on Windows 10 (using PowerShell)

* Activate a Python 3.7 virtualenv
    * If needed, do so with:
    * `C:\Users\lemon\AppData\Local\Programs\Python\Python37\python.exe -m venv /tmp/datamaps-build`
    * `C:\tmp\datamaps-build\Scripts\Activate.ps1`
    * Ensure `pefile` and `pywin32-ctypes` are installed
    * `pyinstaller cli.py --name "dm" --onefile`
    * `dm.exe` is built inside `dist/`