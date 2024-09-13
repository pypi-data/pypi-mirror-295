# icreports

This project is a collection of tools and templates for generating reports at ICHEC.


## Installation ##

The project is available on PyPi, you can install it with:

``` shell
pip install icreports
```

Some features rely on converting images between various formats. For full image format support `imagemagick`, `cairo` and a full LaTeX environment are required. On Mac you can install the former with `brew`. MacTeX can be used to install the LaTeX environment.

## Features ##

### Books ###

You can build a book, like the ICHEC handbook, with:

``` shell
icreports book --source_dir $SOURCE_DIR 
```

where `SOURCE_DIR` is the location of the book sources, including a `_config.yml` and `_toc.yml` file.

If you prefer to build in a container instead of installing build dependencies you can do:

``` shell
cd infra
podman build --platform linux/arm64 -t icreports .
podman run -it -v $SOURCE_DIR:/src -v $BUILD_DIR/:/build -p 8000:8000 --platform linux/arm64 icreports
```

You can replace `podman` with `docker` if preferred. The `SOURCE_DIR` is the path to the book sources on the host. The `BUILD_DIR` is somewhere you want build output to go on the host.

Running the container involves building the book by default, which will take a few minutes. It will then be served at [localhost:8000](http://localhost:8000) which you can launch in browser.

# Copyright #

Copyright 2024 Irish Centre for High End Computing

The software in this repository can be used under the conditions of the GPLv3+ license, which is available for reading in the accompanying `LICENSE` file.
