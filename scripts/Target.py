
import pymjin2

class TargetImpl(object):
    def __init__(self, user):
        # Refer.
        self.u = user
    def __del__(self):
        # Derefer.
        self.u = None

class Target(object):
    def __init__(self, sceneName, nodeName, environment):
        # Refer.
        self.env = environment
        # Create.
        self.u = pymjin2.EnvironmentUser("Target" + nodeName,
                                         "Turn specific node into WAM target")
        self.impl = TargetImpl(self.u)
        # Prepare.
        self.env.registerUser(self.u)
    def __del__(self):
        # Tear down.
        self.env.deregisterUser(self.u)
        # Destroy.
        del self.impl
        del self.u
        # Derefer.
        self.env = None

def SCRIPT_CREATE(sceneName, nodeName, environment):
    return Target(sceneName, nodeName, environment)

def SCRIPT_DESTROY(instance):
    del instance
