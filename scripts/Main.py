
import pymjin2
import random

MAIN_TARGET_NAME_PREFIX = "target"
MAIN_TARGETS_NB = 4

class MainImpl(object):
    def __init__(self, user):
        # Refer.
        self.u = user
    def __del__(self):
        # Derefer.
        self.u = None
    def onPopFinish(self, key, value):
        print "Main.onPopFinish", key, value
        # Continue the game.
        self.step()
    def popRandomTarget(self):
        random.seed(None)
        id = random.randint(1, MAIN_TARGETS_NB)
        print "popRandomTarget", id
        self.u.d["TARGET"] = self.target(id)
        self.u.set("target.$SCENE.$TARGET.moving", "1")
    def step(self):
        self.popRandomTarget()
    def target(self, id):
        return MAIN_TARGET_NAME_PREFIX + str(id)

class Main(object):
    def __init__(self, sceneName, nodeName, environment):
        # Refer.
        self.env = environment
        # Create.
        self.u = pymjin2.EnvironmentUser("Main" + nodeName,
                                         "Run Whac-a-mole game")
        self.impl = MainImpl(self.u)
        # Prepare.
        # Constant.
        self.u.d["SCENE"] = sceneName
        # Listen to target pop finish.
        self.u.listen("target.$SCENE..moving", "0", self.impl.onPopFinish)
        self.env.registerUser(self.u)
        # Start the game.
        self.impl.step()
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
