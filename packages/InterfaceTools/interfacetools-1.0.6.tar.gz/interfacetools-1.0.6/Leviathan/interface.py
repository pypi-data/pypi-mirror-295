


class InterfaceInstancingError(Exception):
    
    def __init__(self, message:str,*args) -> None:
        self.message = f"The class {message} is an interface. Interfaces cannot be instantiated."
        super().__init__(self.message,*args)

def Interface(cls:type) -> type:   
    '''
    ### Decorator class wrapper
    any class with this decorator will enforce partial interfaceing behavoiur to the class.
    mainly, the class cannot be directly made into an object.

    #### example:
    ```python    
    @Interface
    class Myclass():
            ...
    
    ```
    
    '''

    class metaInterface:
        
        def __new__(cls, *args, **kwargs):
            if cls.__bases__.__contains__(metaInterface):
                raise InterfaceInstancingError(cls.__name__)
            return object.__new__(cls,*args,**kwargs)     
   
   
    jclass = type(cls.__name__, (cls,metaInterface), cls.__annotations__) 
    return jclass


