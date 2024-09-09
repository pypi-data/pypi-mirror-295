from setuptools import find_packages, setup

setup(
    name="django-feature-flags",
    version="0.0.1",
    author="",
    author_email="",
    packages=find_packages(),
    scripts=[],
    url="http://pypi.python.org/pypi/django-feature-flags/",
    license="MIT",
    description="A django app to help you manage the django-shopify-app package billing",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    package_data={"feature_flags": ["templates/app_name/*.html"]},
    install_requires=[
        "Django",
        "pytest",
    ],
)
