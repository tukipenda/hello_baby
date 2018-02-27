from jsonclass import JSONClass, merge_dicts
from baby import *
import warmer
import staff
import supplies
import tasks
import threading
from baby_timer import *
import baby_update
import time

#probably should move this into scenario_data of some sort
class Mom(JSONClass):
    def __init__(self, **kwargs):
        super().__init__()
        self.data=kwargs

class Scenario(JSONClass):
    def __init__(self):
        self.baby=None
        self.mom=None
        self.staff=None
        self.warmer=None
        self.supplyMGR=None
        self.scenario_data=None
        self.taskMGR=None

        #move to another place
        self.getCode=threading.Thread(name='getCode', target=self.getCode)
        self.update=threading.Thread(name='update', target=self.updateBabyStatus)
        self.prepComplete=False
        self.resusComplete=False
        self.babyUpdate=None
        self.babyTimer=BabyTimer()

    def loadData(self, loadSupplyList, baby):
        # Initialize a scenario
        self.baby=baby
        self.supplyMGR=supplies.SupplyManager(loadSupplyList)
        self.supplyMGR.fetchSupply("mask", "Infant")
        self.supplyMGR.fetchSupply("mask", "Preemie")
        self.warmer=warmer.Warmer()
        self.taskMGR=tasks.TaskManager(self.supplyMGR, self.baby, self)
        self.taskMGR.loadTasks()
        self.loadBabyUpdate()

#this method should not be called by itself
    def loadBabyUpdate(self):
        self.babyUpdate=baby_update.BabyUpdate(self.baby, self.warmer, self.supplyMGR)
        self.babyUpdate.loadData()

    def prepWarmer(self):
        print("Prep the Warmer")

    def resuscitation(self):
        self.baby.deliver()
        self.getCode.start()
        self.update.start()
        self.babyTimer.startTimer()
        print("Resuscitate the baby")

    def updateBabyStatus(self):
        while(not self.resusComplete):
            time.sleep(5)
            self.babyUpdate.update()

    def getCode(self):
        self.run_loop(self.resusComplete)

    def run_loop(self, condition):
        while(not condition):
            cmd=input(">>> ")
            if cmd=="quit()":
                condition=True
                break
            if cmd=="l":
                print("pb, pv, pw, pt, ps")
                break
            if cmd[0]=="p":
                # things to print - baby's status, warmer's status, time, supplies (and supply status), 
                if cmd[1]=="b":
                    pe=self.baby.PE
                    for k,v in pe.items():
                        print(k+": "+str(v)+"\n")
                    break
                if cmd[1]=="v":
                    print(self.baby.vitals)
                    break
                if cmd[1]=="w":
                    print(self.warmer.__dict__)
                    break
                if cmd[1]=="t":
                    print(self.babytimer.getElapsedTime())
                    break
                if cmd[1]=="s":
                    s=self.supplyMGR.supplies
                    for k,v in s.items():
                        if k in ["ETT", "laryngoscope", "mask"]:
                            v=" ".join([str(k) for k in v])
                        print(k+": "+str(v)+"\n")
                    break
            if cmd.startswith("run"):
                cmds=cmd.split(" ")
                cmds=cmds[1:]
                try:
                    self.taskMGR.doTask(*cmds)
                except Exception as e: print(e)
                break
            else:
                try:
                    exec(cmd)
                except Exception as e: print(e)