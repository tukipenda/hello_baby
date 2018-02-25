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
        self.getCode=threading.Thread(name='getCode', target=self.getCode)
        self.update=threading.Thread(name='update', target=self.updateBabyStatus)
        self.prepComplete=False
        self.resusComplete=False
        self.babyUpdate=None
        self.babyTimer=BabyTimer()

    def loadData(self):
        # Initialize a scenario
        self.scenario_data={'scenario_text':"You are called by the OB team for a stat C/S. Mom is 25 years old, and gestational age is 36 weeks."}
        self.baby=Baby(33, [])

        pL="Prenatal labs: VZVI, RI, HIV negative, Hep B negative, RPRNR, GC/Chlamydia negative"
        hsv="No history of HSV and has no active lesions."
        gbs="GBS+.  She was febrile to 38.1, and received ampicillin 2 hours before delivery."
        rom="ROM occurred 16 hours ago."
        gp="G1PO"
        self.mom=Mom(age=25, prenatalLabs=pL, HSV=hsv, GBS=gbs, ROM=rom, GP=gp)

        nurse=staff.RN("Juan")
        respiratory=staff.RT("Sheri")
        self.staff=staff.Staff([nurse, respiratory])

        supplyList=[
            "pulse_ox",
            "hat",
            "transwarmer",
            "plastic_bag",
            "temp_probe",
            "blankets",
            "bulb_suction",
            "meconium_aspirator",
            "stethoscope",
            "epinephrine",
            "normal_saline_bag",
            "cord_clamp",
            "scalpel",
            "flush",
            "UVC"
        ]
        loadSupplyList={"laryngoscope":[], "ETT":[], "mask":[]}
        for supplyName in supplyList:
            supply=supplies.Supply(supplyName)
            loadSupplyList[supplyName]=supply

        for size in ["0", "1", "00"]:
            laryngoscope=supplies.Laryngoscope(size)
            loadSupplyList["laryngoscope"].append(laryngoscope)

        for size in ["2.5", "3", "3.5", "4"]:
            ETT=supplies.ETT(size)
            loadSupplyList["ETT"].append(ETT)

        for maskType in ["Infant", "Preemie"]:
            mask=supplies.Mask(maskType)
            loadSupplyList["mask"].append(mask)

# temperature (turned on), suction, bag/mask, oxygen flow, baby timer
# supplies - ETT (sizes), masks, pulse ox, laryngoscope, hat, blankets, bulb suction, deep suction/meconium aspirator, preemie supplies
        self.supplyMGR=supplies.SupplyManager(loadSupplyList)
        self.supplyMGR.fetchSupply("mask", "Infant")
        self.supplyMGR.fetchSupply("mask", "Preemie")

        self.warmer=warmer.Warmer()


        self.babyUpdate=baby_update.PreemiePPV(self.baby, self.warmer, self.supplyMGR)
        self.babyUpdate.loadData()

        self.taskMGR=tasks.TaskManager(self.supplyMGR, self.baby, self)
        self.taskMGR.loadTasks()

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
            self.taskMGR.completeTasks(self.babyTimer.getElapsedTime())
     
    def getCode(self):
        self.run_loop(self.resusComplete)
    
    def run_loop(self, condition):
      while(not condition):
          cmd=input(">>> ")
          if cmd=="quit()":
            condition=True
          try:
            exec(cmd)
          except Exception as e: print(e)
            

    def scoring(self):
        pass