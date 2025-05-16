from setuptools import setup
from setuptools import find_packages

# Fake reference so GitHub still considers it a real package.
setup(
    name="mk-obwiki",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    package_data={
        "mk_obwiki": [
            "stylesheets/*.css",
            "templates/partials/*.html",
        ]
    },
    entry_points={
        "mkdocs.plugins": [
            "mk-obwiki = mk_obwiki.plugin:MyPlugin",
        ]
    },
)
