
from Leviathan.interface import InterfaceInstancingError, Interface


class yolo:
    
    def yolo2(self):pass

@Interface
class MyClass():   
   
   def method_1(self): 
            pass
@Interface    
class Myinter():
    
    def method_3(self):pass

class My2Class(MyClass, yolo):
    
    def __init__(self):
        pass
    
    def method_2(self):
        pass

    




def test_interface_instance():
    try:
        foo = MyClass()  # Should raise an error
        assert False
    except InterfaceInstancingError as e:
        assert True
        print(f"interface instancing worked {e}")    
        

def test_instancing():
    try:
        fog = My2Class()  # Creating an instance should work fine
    except Exception as e:
        print(e)
        assert False
    assert True
    
def test_polymorphism():
    fog = My2Class()
    
    print(isinstance(fog, MyClass))          # Should return True
    assert isinstance(fog, MyClass)          # Should return True
    
    print(isinstance(fog, My2Class))         # Should return True
    assert isinstance(fog, My2Class)         # Should return True
    
    print(isinstance(MyClass, My2Class))     # Should return False    
    assert not isinstance(MyClass, MyClass)  # Should return False => therefore assert true
    
    print(isinstance(fog,Myinter))           # should be false
    assert not isinstance(fog, Myinter)      # Should return false => therefore assert True
   
   
    
    
   