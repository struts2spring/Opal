

class Workspace(object):
    class __Workspace:
        def __init__(self):
            self.path = None
        def __str__(self):
            return `self` + self.path
    instance = None
    def __new__(cls): # __new__ always a classmethod
        if not Workspace.instance:
            Workspace.instance = Workspace.__Workspace()
        return Workspace.instance
    def __getattr__(self, name):
        return getattr(self.instance, name)
    def __setattr__(self, name):
        return setattr(self.instance, name)


if __name__=="__main__":
    x = Workspace()
    x.path = 'sausage'
    print(x)
    y = Workspace()
    y.path = 'eggs'
    print(y)
    z = Workspace()
    z.path = 'spam'
    print(z)
    print(x)
    print(y)