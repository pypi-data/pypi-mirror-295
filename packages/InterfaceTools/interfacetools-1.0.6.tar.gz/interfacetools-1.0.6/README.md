# Interface Decorator

allows the use of the @Interface class decorator, which allows for partai linterface behavoiur curretly only preventing direct instantaion. 
future feeatures hope to include method detection and force children implementations, however can be acompished with ABC pacakge.

this pacakge is desinged to be light waieghts and extremely simply to use. one @ to rule them all. in this case enforcing typical interface behavoiurs with good readability.


install

```cli
pip install InterfaceTools
```

## Instructions:

above any clases you wish to become a interface and restrict instantaition to only children: 

```Python
from Leviathan.interface import Interface

@interface
class MyClass():

    def Method():pass
```

that all thier is to it. this decorator then restrict this class ever to instanaite on its own meaning that the following:

```Python
foo = MyClass()
```
which givesthe follwing error:

```
InterfaceInstancingError: The class MyClass is an interface. Interfaces cannot be instantiated.
```

addiaitonally unlike inerfaces in C# or java you are not required to implent thier methods. however if you desire that functionality you can use this with the ABC pacakge to enforce children overriding methods 

example:

```python
from abc import ABCMeta, abstractmethod

@Interface 
class myClass(metaclass=ABCMeta):
    
    @abstractmethod
    def method():pass
```

the example above will give you full C# or Java Like interface.


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

the interface wrapper is fully compatable with all the default python functions, and abc package for further control over your interface.