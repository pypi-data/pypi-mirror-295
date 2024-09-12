from setuptools import setup, find_packages

setup(
    name='virtualenv-better-bash',
    version='0.2',
    description='Add in custom modifications to virtualenv',
    author='Bill Clark',
    packages=find_packages(),
    include_package_data=True,
    package_data={'virtualenv_bb':['activate']},
    install_requires=[
        "virtualenv>=20.0"
    ],
    entry_points="""
    [virtualenv.activate]
    better_bash=virtualenv_bb:BashActivator
    """
)
