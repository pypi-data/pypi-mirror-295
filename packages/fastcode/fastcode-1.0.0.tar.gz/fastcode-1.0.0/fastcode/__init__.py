def _check_dependencies():
    _hard_dependencies = ()
    _missing_dependencies = ['imaplib' , 'smtplib' , 'email' , 'typing' , 're' , 'os']

    for _dependency in _hard_dependencies:
        try:
            __import__(_dependency)
        except ImportError as _e:  
            _missing_dependencies.append(f"{_dependency}: {_e}")

    if _missing_dependencies:  
        raise ImportError("Unable to import required dependencies:\n" + "\n".join(_missing_dependencies))
    
    del _hard_dependencies, _dependency, _missing_dependencies




if __name__ == "__main__":
    _check_dependencies()

    from .email_protocols import *
    
    

