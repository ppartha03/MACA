# MACA
Modular Architecture for Conversational Agents

## Architecture
[Diagram](https://drive.google.com/open?id=0B3VG4mDUTWdINnQ1T1Bac3RQbW8)

## Documentation
[Documentation](https://www.sharelatex.com/project/57e6a38ba43378350898ae02)

## Installation
No installation required. Cloning this repository is sufficient.

## Run a simple system
1. Go into the directory containing the cloned MACA repository
```
cd <your_dir>/MACA
```
2. [Optional] Configure the configuration file: config.py using your favorite text editor. Modify the field `system_description_file` to the appropriate configuration files (some examples are provided in `system_configs` directory.
3. <b>If you did step 2</b>, launch the system using python:
```
python main.py
```
<b>If you skipped step 2</b>, launch the system and specify the `system_description_file` using flag `-f`, for example:
```
python main.py -f system_configs/echo_system.py
```
4. To terminate, simply interrupt the system by pressing `Ctrl + C`.

## References
[POMDP](https://github.com/mbforbes/py-pomdp)

[HRED](https://github.com/julianser/hed-dlg-truncated)

[Dual encoder](https://github.com/NicolasAG/Discriminator)