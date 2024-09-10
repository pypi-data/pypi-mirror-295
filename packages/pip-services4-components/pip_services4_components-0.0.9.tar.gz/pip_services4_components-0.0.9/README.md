# <img src="https://uploads-ssl.webflow.com/5ea5d3315186cf5ec60c3ee4/5edf1c94ce4c859f2b188094_logo.svg" alt="Pip.Services Logo" width="200"> <br/> Portable Component Model for Python

This module is a part of the [Pip.Services](https://www.pipservices.org/) polyglot microservices toolkit.

It defines a portable component model interfaces and provides utility classes to handle component lifecycle.

The module contains the following packages:
- **Build** - basic factories for constructing objects
- **Config** - configuration pattern
- **Refer** - locator inversion of control (IoC) pattern
- **Run** - component life-cycle management patterns

<a name="links"></a> Quick links:

* [Logging](http://docs.pipservices.org/v4/tutorials/beginner_tutorials/observability/logging/)
* [Configuration](http://docs.pipservices.org/v4/tutorials/beginner_tutorials/configuration/) 
* [API Reference](https://pip-services4-python.github.io/pip-services4-components-python/index.html)
* [Change Log](CHANGELOG.md)
* [Get Help](http://docs.pipservices.org/v4/get_help/)
* [Contribute](http://docs.pipservices.org/v4/contribute/)

## Use

Install the Python package as
```bash
pip install pip_services4_components
```

Then you are ready to start using the Pip.Services patterns to augment your backend code.

For instance, here is how you can implement a component, that receives configuration, get assigned references,
can be opened and closed using the patterns from this module.

```python
from pip_services4_commons.config import IConfigurable, ConfigParams
from pip_services4_commons.refer import IReferenceable, IReferences, Descriptor
from pip_services4_commons.run import IOpenable


class MyComponentA(IConfigurable, IReferenceable, IOpenable):
    _param1 = 'ABC'
    _param2 = 123
    _another_component: MyComponentB
    _opened = True

    def configure(self, config):
        self._param1 = ConfigParams.get_as_string_with_default("param1", self._param1)
        self._param2 = config.get_as_integer_with_default("param2", self._param2)

    def set_references(self, references):
        self._another_component = references.get_one_required(
            Descriptor("myservice", "mycomponent-b", "*", "*", "1.0")
        )

    def is_opened(self):
        return self._opened

    def open(self, context):
        self._opened = True
        print("MyComponentA has been opened.")

    def close(self, context):
        self._opened = True
        print("MyComponentA has been closed.")
```

Then here is how the component can be used in the code

```python
from pip_services4_commons.config import IConfigurable, ConfigParams
from pip_services4_commons.refer import References, Descriptor

my_component_A = MyComponentA()

# Configure the component
my_component_A.configure(ConfigParams.from_tuples(
    'param1', 'XYZ',
    'param2', 987
))

# Set references to the component
my_component_A.set_references(References.from_tuples(
    Descriptor("myservice", "mycomponent-b", "default", "default", "1.0"), my_component_B
))

# Open the component
my_component_A.open(Context.from_trace_id("123"))
print("MyComponentA has been opened.")
```

If you need to create components using their locators (descriptors) implement 
component factories similar to the example below.

```python
from pip_services4_commons.refer import Descriptor
from pip_services4_components.build import Factory


class MyFactory(Factory):
    my_component_descriptor = Descriptor("myservice", "mycomponent", "default", "*", "1.0")

    def __init__(self):
        super(MyFactory, self).__init__()

        self.register_as_type(MyFactory.my_component_descriptor, MyFactory)


# Using the factory
my_factory = MyFactory()
my_component1 = my_factory.create(Descriptor("myservice", "mycomponent", "default", "myComponent1", "1.0"))
my_component2 = my_factory.create(Descriptor("myservice", "mycomponent", "default", "myComponent2", "1.0"))

...
```

## Develop

For development you shall install the following prerequisites:
* Python 3.7+
* Visual Studio Code or another IDE of your choice
* Docker

Install dependencies:
```bash
pip install -r requirements.txt
```

Run automated tests:
```bash
python test.py
```

Generate API documentation:
```bash
./docgen.ps1
```

Before committing changes run dockerized build and test as:
```bash
./build.ps1
./test.ps1
./clear.ps1
```

## Contacts

The initial implementation is done by **Sergey Seroukhov**. Pip.Services team is looking for volunteers to 
take ownership over Python implementation in the project.
