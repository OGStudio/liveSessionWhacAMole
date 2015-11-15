
import pymjin2

class MainImpl(object):
    def __init__(self, user):
        # Refer.
        self.u = user
    def __del__(self):
        # Derefer.
        self.u = None

class Main(object):
    def __init__(self, sceneName, nodeName, environment):
        # Refer.
        self.env = environment
        # Create.
        self.u = pymjin2.EnvironmentUser("Main" + nodeName,
                                         "Run Whac-a-mole game")
        self.impl = MainImpl(self.u)
        # Prepare.
        self.env.registerUser(self.u)
        print "Main.__init__"
    def __del__(self):
        # Tear down.
        self.env.deregisterUser(self.u)
        # Destroy.
        del self.impl
        del self.u
        # Derefer.
        self.env = None
        print "Main.__del__"


def SCRIPT_CREATE(sceneName, nodeName, environment):
    return Main(sceneName, nodeName, environment)

def SCRIPT_DESTROY(instance):
    del instance
