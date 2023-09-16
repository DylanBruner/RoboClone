import inspect

class Security:
    @staticmethod
    def isHarmful(func: object) -> bool:
        code = inspect.getsource(func)
        print(code)

def test():
    print(eval("1+1"))
    return "Test successful"

print(Security.isHarmful(test))