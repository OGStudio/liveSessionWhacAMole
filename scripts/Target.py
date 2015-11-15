
import pymjin2

TARGET_ACTION_POP_NAME  = "sequence.default.popTarget"
TARGET_ACTION_WAIT_NAME = "delay.default.waitForLeverage"

class TargetImpl(object):
    def __init__(self, user):
        # Refer.
        self.u = user
        # Create.
        self.isMoving = False
    def __del__(self):
        # Derefer.
        self.u = None
    def onPopFinish(self, key, value):
        self.isMoving = False
        self.u.report("target.$SCENE.$NODE.moving", "0")
    def onSelection(self, key, value):
        # Ignore selection if we're not moving.
        if (not self.isMoving):
            return
        self.u.report("target.$SCENE.$NODE.selected", "1")
        self.u.report("target.$SCENE.$NODE.selected", "0")
    def setMoving(self, key, value):
        self.isMoving = True
        self.u.set("$POP.$SCENE.$NODE.active", "1")

class Target(object):
    def __init__(self, sceneName, nodeName, environment):
        # Refer.
        self.env = environment
        # Create.
        self.u = pymjin2.EnvironmentUser("Target" + nodeName,
                                         "Turn specific node into WAM target")
        self.impl = TargetImpl(self.u)
        # Prepare.
        # Constant.
        self.u.d["SCENE"] = sceneName
        self.u.d["NODE"]  = nodeName
        self.u.d["POP"]   = TARGET_ACTION_POP_NAME
        self.u.d["WAIT"]  = TARGET_ACTION_WAIT_NAME
        # Provide "moving".
        self.u.provide("target.$SCENE.$NODE.moving", self.impl.setMoving)
        # Listen to pop action finish.
        self.u.listen("$POP.$SCENE.$NODE.active", "0", self.impl.onPopFinish)
        # Listen to node selection.
        self.u.listen("selector.$SCENE.selectedNode", nodeName, self.impl.onSelection)
        # Provide.
        self.u.provide("target.$SCENE.$NODE.selected")
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
