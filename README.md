NOTE: This project is a work in progress and will not currently run properly.

# Japanese Data Extractor

Extracting data from Japanese texts is a complicated topic.
In this project, we do not try any fancy machine learning, but rather try to extract and process data using regular expressions.

## Getting Started

I recommend setting up a project in PyCharm and pulling the sources from git.
Run 'pip install requirements.txt' to install all required packages.
Go to Edit Configurations in PyCharm and specify the below scripts.
(PyCharm will add the project root to PYTHONPATH, otherwise you will have to do this manually.)

The executable scripts are per below:
OBS: This project is still in early stages and have no executable scripts yet

### Prerequisites

This should run fine on any environment that supports Python 3.6.

## Built With

Development tools

* [Python 3.6](https://www.python.org/downloads/) - Language runtime
* [PyCharm](https://www.jetbrains.com/pycharm/) - IDE by JetBrains

Key Libraries

* [regex](https://pypi.org/project/regex/) - Regex library that extends the standard re-library that is the default library that comes with Python.

See requirements.py for all libraries used.

## Authors

* **Krister S Jakobsson** - *Implementation and pretty much everything else*

## License

This project is licensed under the Boost License - see the [license](LICENSE.md) file for details

## Acknowledgments

* **Regular-Expression.info** - Great page explaining regex in general and differences between platforms and libraries in particular. [Link](https://www.regular-expressions.info/)
* **regex101.com** - Great online tool for playing around with and learning about regex. [Link](https://regex101.com/)

Disclaimer: I am in no way associated with above mentioned homepages and tools, and take no responsibility for how they use data you input on their platforms.
Use them on your own risk.