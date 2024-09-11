

This is the private github of pycsp3 (including it as a submodule):

To clone this project including the submodule pycsp3:
```
git clone --recurse-submodules https://github.com/xcsp3team/ppycsp3.git
```

Do not forget to export the PYTHONPATH: launch this command in the directory ppycsp3:
```
export PYTHONPATH=$PYTHONPATH:/.
```
or something like:
```
export PYTHONPATH=$PYTHONPATH:.:/home/lecoutre/workspace
```

To pull, while taking into account the submodule:
```
git pull --recurse-submodules
```

To push a new version on pypi:
```
pip3 install wheel
pip3 install twine
python3 update_pypi_version.py
```

If you have a problem: 
```
pip3 install -U pip
pip3 install -U twine wheel setuptools
pip3 install --upgrade keyrings.alt
python3 update_pypi_version.py
```

