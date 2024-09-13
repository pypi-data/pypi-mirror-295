
## Welcome to UDINI-Packages, the TOOLS package.
<img alt="Udini dental suite" src="https://www.udini.co/_next/image?url=%2Fsvg%2Fhome%2FudiniLogoWhiteBackground.svg&w=256&q=75">


### PyPi deployment

In order to push changes to the **TOOLS** package, be sure that:

- You've put into the `setup.cfg` *required* packages for the shared utilities with its version.



#### Deploy new version

To deploy new version, be sure you have the latest version of PyPa’s build installed:
```shell
python3 -m pip install --upgrade build
```


Go to the `/pix_plus` folder and run next command:
```shell
python3 -m build
```

This command should output a lot of text and once completed should generate two folder in the directory:
**dist** and **pix_plus.egg-info**

To upload new version of the package, also be sure to update the **version** of the package. See the semantics of the versioning at *https://semver.org/*

Install **twine**, to upload all the archives under dist:
```shell
python3 -m pip install --upgrade twine
```

After, you can push new version of the package with `python3 -m twine upload --skip-existing dist/* --verbose`. You will be prompted for *username* and *password*. 

Once uploaded, you can check your new version at *https://pypi.org/project/pix-plus/*

If any issues are met, look at the complete [tutorial](https://packaging.python.org/en/latest/tutorials/packaging-projects/).
