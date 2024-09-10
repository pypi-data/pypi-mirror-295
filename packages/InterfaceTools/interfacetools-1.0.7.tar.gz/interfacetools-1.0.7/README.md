# Interface Decorator

allows the use of the @Interface class decorator, which allows for partial interface behavior currently only preventing direct instantiation. 
future features hope to include method detection and force children implementations, however, this can be accomplished with the ABC package.

this package is designed to be light weight and extremely simple to use. one @ to rule them all. in this case, enforcing typical interface behaviors with good readability.


install
 windows
```cli
pip install InterfaceTools
```

Mac
```cli
pip3 install InterfaceTools
```

## Instructions:

above any classes you wish to become an interface and restrict instantaition to only children: 

```Python
from Leviathan.interface import Interface

@interface
class MyClass():

    def Method():pass
```

that is all there is to it. this decorator then restricts this class never to instantiate on its own; meaning the following:

```Python
foo = MyClass()
```
which gives the following error:

```
InterfaceInstancingError: The class MyClass is an interface. Interfaces cannot be instantiated.
```

Additionally, unlike interfaces in C# or Java, you are not required to implement their methods. however, if you desire that functionality you can use this with the ABC package to enforce children-overriding methods 

example:

```python
from abc import ABCMeta, abstractmethod

@Interface 
class myClass(metaclass=ABCMeta):
    
    @abstractmethod
    def method():pass
```

the example above will give you a full C# or Java-like interface.


other things you can do with this module are interface inheritance:


example:

```python
@Interface 
class myClass():
    pass
@Interface
class class2(myClass):
    pass
```

which you can also inherit from regular classes as well.

```python
class myClass():
    pass
@Interface
class class2(myClass):
    pass
```

the interface wrapper is fully compatible with all the default Python functions, and the ABC package for further control over your interface.
