# CAU (Central Asian University) Services Python Client

<img src="https://github.com/timur-urunbaev/cau_services/blob/main/centralasian_logo.png" alt="cau_services" style="width:250px;" align="left"/>

This opensource Python Client for services of [Central Asian University](https://centralasian.uz/). With this package you will be able to get timetable, attendance and other stuff, and automate for your purposes, this can be useful for pet-projects.

For now here:
- [timetable](https://cau.edupage.org/timetable/) ([link to code](https://github.com/timur-urunbaev/cau_services/blob/main/cau/Timetable.py))

Comming Soon:
- attendance
- marks

For more information on how Timetable API works, you can take a look to `timetable.ipynb`.

## Usage

### Installation

| I will try to make this README "begginers friendly", trying to explain the whole process of installation in details.

Create Python Environment:

```shell
python3 -m venv .venv
```

Activating python environment (For Linux/UNIX/MacOS):

```shell
source .venv/bin/activate
# OR
. .venv/bin/activate
```

Activating python environment (For Windows PowerShell):

```shell
# for PowerShell
.venv\Scripts\Activate.ps1

# CMD
.venv\Scripts\activate.bat
```

! FOR NOW PACKAGE ISN'T UPLOADED TO ANY PACKAGE REPOSITORY SO USE FOLLOWING INSTRUCTIONS TO INSTALL IT.

```shell
git clone https://github.com/timur-urunbaev/cau_services.git .
```

Inside the cloned repo write this command (so the package will be installed to your virtual environment):

```shell
python -m pip install .
```

Now you can use this package inside of your projects.

### Download

```python
from cau import Timetable

timetable = Timetable()
timetable.download()
```

### Timetable

```python
from cau import Timetable

timetable = Timetable()
timetable.download()
week: dict = timetable.get_week_by_class_id("<class_id>")
```

Then you can turn Python `dict` to `json` using any your preferable tool, e.g. `json` package:

```python
import json
from cau import Timetable

timetable = Timetable()
timetable.download()
week: dict = timetable.get_week_by_class_id("<class_id>")

print(json.dumps(week)) # to see the result
```

## Author

Urunbaev Timur
