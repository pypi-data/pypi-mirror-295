# hatch-external-dependencies

The package is a hatch plugin.

When building with hatchling this plugin will look in the project toml configuration for an external section and adds dependencies in the built package's metadata as a Requires-External entry.



## Toml Example

There are two supported syntax to define the external dependencies in the pyproject.toml:

    [project]
    external-dependencies = ["pkg:generic/libsomething", ...]

or (based on https://peps.python.org/pep-0725/):

    [external]
    dependencies = ["pkg:generic/libsomething", ...]

