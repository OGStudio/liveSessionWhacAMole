
import pymjin2

LEVERAGE_ACTION_ROTATE_NAME = "sequence.default.rotateLeverage"
LEVERAGE_ACTION_LOWER_NAME  = "rotate.default.lowerLeverage"

class LeverageImpl(object):
    def __init__(self, user):
        # Refer.
        self.u = user
    def __del__(self):
        # Derefer.
        self.u = None
    def setMoving(self, key, value):
        print "leverage.setMoving", key, value
        self.u.set("$ROTATE.$SCENE.$NODE.active", "1")

class Leverage(object):
    def __init__(self, sceneName, nodeName, environment):
        # Refer.
        self.env = environment
        # Create.
        self.u = pymjin2.EnvironmentUser("Leverage" + nodeName,
                                         "Turn specific node into WAM leverage")
        self.impl = LeverageImpl(self.u)
        # Prepare.
        # Constant.
        self.u.d["SCENE"]  = sceneName
        self.u.d["NODE"]   = nodeName
        self.u.d["ROTATE"] = LEVERAGE_ACTION_ROTATE_NAME
        self.u.d["LOWER"]  = LEVERAGE_ACTION_LOWER_NAME
        # Provide "moving".
        self.u.provide("leverage.$SCENE.$NODE.moving", self.impl.setMoving)
        # Listen to pop action finish.
#        self.u.listen("$POP.$SCENE.$NODE.active", "0", self.impl.onPopFinish)
#        # Listen to node selection.
#        self.u.listen("selector.$SCENE.selectedNode", nodeName, self.impl.onSelection)
#        # Provide.
#        self.u.provide("target.$SCENE.$NODE.selected")
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
    return Leverage(sceneName, nodeName, environment)

def SCRIPT_DESTROY(instance):
    del instance
