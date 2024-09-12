# AA Bootswatch

A Simple collection of Bootswatch themes for users to explore. This repo also acts as an example of the new Theming options in Alliance Auth v4.x

## Installation

### Step One - Install

Install the app with your venv active

```shell
pip install aa-bootswatch
```

### Step Two - Configure

- Add as many, or as little of the following lines to `INSTALLED_APPS` as required.

```python
'bootswatch.theme.cerulean',
'bootswatch.theme.cosmo',
'bootswatch.theme.cyborg',
'bootswatch.theme.journal',
'bootswatch.theme.litera',
'bootswatch.theme.lumen',
'bootswatch.theme.lux',
'bootswatch.theme.minty',
'bootswatch.theme.morph',
'bootswatch.theme.pulse',
'bootswatch.theme.quartz',
'bootswatch.theme.sandstone',
'bootswatch.theme.simplex',
'bootswatch.theme.sketchy',
'bootswatch.theme.slate',
'bootswatch.theme.solar',
'bootswatch.theme.spacelab',
'bootswatch.theme.superhero',
'bootswatch.theme.united',
'bootswatch.theme.vapor',
'bootswatch.theme.yeti',
'bootswatch.theme.zephyr',
```

### Step Three - Update Project

- Run migrations `python manage.py migrate` (There should be none )
- Gather your staticfiles `python manage.py collectstatic`
