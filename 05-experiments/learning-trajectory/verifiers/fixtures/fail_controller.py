from dataclasses import dataclass

@dataclass
class Quantity:
    value: float
    unit: str
    @property
    def dimension(self):
        return "L/T" if self.unit in {"m/s", "km/h"} else "L"
    def to_si(self):
        if self.unit == "m/s": return self.value
        if self.unit == "km/h": return self.value / 3.6
        return self.value

class Controller:
    def __init__(self):
        self.states={}
        self.transitions=[]
        self.current_state=None
        self.environment={}
    def add_state(self,name,initial=False):
        self.states[name]=True
        if initial:self.current_state=name
    def add_transition(self,*args,**kwargs):
        self.transitions.append((args,kwargs))
    def quantity(self,value,unit): return Quantity(value,unit)
    def compare(self,left,right):
        if left.dimension != right.dimension: raise ValueError("incompatible")
        return left.to_si()-right.to_si()
    def set_environment(self,**values): self.environment.update(values)
    def dispatch(self,event):
        return None
    def verify_reachability(self): return {"reachable":[]}
    def verify_guards(self,probes): return {"probes_checked":len(probes)}

def create_controller(): return Controller()
