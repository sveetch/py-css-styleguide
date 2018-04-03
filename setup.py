from setuptools import setup, find_packages

setup(
    name='py-css-styleguide',
    version=__import__('py_css_styleguide').__version__,
    description=__import__('py_css_styleguide').__doc__,
    long_description=open('README.rst').read(),
    author='David Thenon',
    author_email='sveetch@gmail.com',
    url='https://github.com/sveetch/py-css-styleguide',
    license='MIT',
    packages=find_packages(exclude=['tests*']),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
        'tinycss2',
    ],
    include_package_data=True,
    zip_safe=False
)