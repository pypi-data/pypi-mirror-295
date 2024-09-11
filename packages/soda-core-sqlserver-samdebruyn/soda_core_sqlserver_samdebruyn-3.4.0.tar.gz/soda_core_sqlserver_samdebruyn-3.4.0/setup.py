#!/usr/bin/env python

from setuptools import find_namespace_packages, setup

package_name = "soda-core-sqlserver-samdebruyn"
package_version = "3.4.0"
description = "Soda Core SQL Server Package with support for Entra ID authentication"

requires = ["soda-core>=3.3.20", "pyodbc", "azure-identity~=1.17.1"]
# TODO Fix the params
setup(
    name=package_name,
    version=package_version,
    install_requires=requires,
    packages=find_namespace_packages(include=["soda*"]),
)
