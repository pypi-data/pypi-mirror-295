# iccore

This project has a collection of common data structures and utilities used in other ICHEC tools.

# Install  #

It is available on PyPI:

``` sh
pip install iccore
```

# Features #

The idea of this project is to provide some common, tested and 'production focused' utilities for use in other ICHEC projects.

Here 'production focused' means that features like 'dry run', logging and secure defaults are included.

This is done by wrapping basic Python utilities that interact with system resources, for example:

* external processes
* the filesystem
* network 

with stubs that can be mocked for tests or executed in 'dry run' mode.

By using the `filesystem`, `process` and `network` utils provided here instead of the low-level Python libraries directly you get to benefit from these extra features and help to standarize our tooling.

## CLI ##
A basic CLI is included, mostly for testing, but it may be useful for getting ideas on what features the package can be used to support.

### Downloading a file ###

``` shell
iccore download --url $RESOURCE_URL --download_dir $WHERE_TO_PUT_DOWNLOAD
```

### Getting Gitlab Milestones ###

This is an example of using the CLI to get Gitlab Milestones given a project id and access token.

``` shell
iccore gitlab --token $GITLAB_TOKEN milestone $PROJECT_ID
```

### Getting The Latest Project Release ###

This example uses the CLI to get version number of the most recent project release

``` shell
iccore gitlab --token $GITLAB_TOKEN latest_release $PROJECT_ID
```

# License #

This project is licensed under the GPLv3+. See the incluced `LICENSE.txt` file for details.
