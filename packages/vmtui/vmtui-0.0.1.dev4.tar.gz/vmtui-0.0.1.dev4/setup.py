from setuptools import setup

setup(setup_requires=["pbr"],
      pbr=True,
      entry_points={'console_scripts': ['vmtui=vmtui.vmtui:main']})
