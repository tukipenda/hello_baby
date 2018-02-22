#need to include what is shown on the screen at any given time, possible actions, who to assign each action to, duration of actions.  Infant status, vitals (if known)

# on screen - should be time elapsed since birth (if timer has been started), appearance of infant (including color, chest rise, audible breath sounds, any anatomical abnormality, term/preterm)
# vitals for infant - O2 sat/HR (if probe in place), temperature.  Need to request HR/breath check/PE check.  Last PE can stay up there
#staff - who is working on what.  Who is standing around uncertainly.  
#info about compressions - rate/quality.  Info about PPV/intubation.  
#possible actions (should include update on appearance/vitals etc...)

#one timer should be the deliveryTimer, the other the trueTimer (based on true time of delivery)

#I need timer to be available everywhere, I need babyhealth to be updated at any time, I need a log of procedures together with time they occurred at (as well as log of infant's status)

from timeit import default_timer as timer

class BabyTimer:
  def __init__(self):
    self.startTime=None
    
  def startTimer(self):
    if not self.startTime:
      self.startTime=timer()
    
    else:
      pass #need to raiseError timealreadystarted
  
  def getElapsedTime(self):
    return round(timer()-self.startTime)

class EventLog:
  def __init__(self):
    pass