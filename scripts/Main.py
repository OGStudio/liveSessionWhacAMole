
import pymjin2
import random

MAIN_LEVERAGE_NAME_PREFIX = "leverage"
MAIN_SCORE_NAME_PREFIX    = "score"
MAIN_SCORE_MATERIAL       = "score"
MAIN_TARGET_NAME_PREFIX   = "target"
MAIN_TARGETS_NB           = 4

class MainImpl(object):
    def __init__(self, user):
        # Refer.
        self.u = user
        # Create.
        self.activeTarget = None
        self.score        = 0
    def __del__(self):
        # Derefer.
        self.u = None
    def onCatch(self, key, value):
        if (value[0] == "1"):
            self.activeTarget = key[2]
        else:
            self.activeTarget = None
    def onPopFinish(self, key, value):
        # Continue the game.
        self.step()
    def onHit(self, key, value):
        # No active target.
        if (self.activeTarget is None):
            return
        leverage = key[2]
        targetLeverage = self.targetToLeverage(self.activeTarget)
        if (leverage == targetLeverage):
            self.setScore(self.score + 1)
    def onSelection(self, key, value):
        self.u.d["LEVERAGE"] = self.targetToLeverage(key[2])
        self.u.set("leverage.$SCENE.$LEVERAGE.moving", "1")
    def popRandomTarget(self):
        random.seed(None)
        id = random.randint(1, MAIN_TARGETS_NB)
        self.u.d["TARGET"] = self.target(id)
        self.u.set("target.$SCENE.$TARGET.moving", "1")
    def setScore(self, score):
        self.score = score
        print "setScore", score
        self.u.d["SCORE"] = MAIN_SCORE_NAME_PREFIX + str(score)
        self.u.set("node.$SCENE.$SCORE.material", MAIN_SCORE_MATERIAL)
    def step(self):
        self.popRandomTarget()
    def target(self, id):
        return MAIN_TARGET_NAME_PREFIX + str(id)
    def targetToLeverage(self, target):
        v = target.split(MAIN_TARGET_NAME_PREFIX)
        return MAIN_LEVERAGE_NAME_PREFIX + v[1]

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
        # Listen to target selection.
        self.u.listen("target.$SCENE..selected", "1", self.impl.onSelection)
        # Listen to leverage hit.
        self.u.listen("leverage.$SCENE..hit", "1", self.impl.onHit)
        # Listen to target catch.
        self.u.listen("target.$SCENE..catch", None, self.impl.onCatch)
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
