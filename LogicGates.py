#!/usr/bin/python
# -*- coding: utf-8 -*-

from Factories import *


class Gate:

    params_pmos = " l=400 w=15"
    params_nmos = " l=50 w=100"
    P_model = "PMOS"
    N_model = "NMOS"
    
    def getNetlist(self):
        return self.lines
            
    def getOutput(self):
        return self.output


        
class Nand(Gate):
    def __init__(self, inputs):
        self.lines = []
        self.output = NetsFactory.getNet()
        self.down = NetsFactory.getNet()
        
        self.lines.append(PartFactory.getPart() + " vcc " + inputs[0] + " " + self.output + " vcc " + self.P_model + " " + self.params_pmos + " ;NAND")                # pierwsza para tranzystorów
        self.lines.append(PartFactory.getPart() + " " + self.output + " " + inputs[0] + " " + self.down + " gnd " + self.N_model + " " + self.params_nmos)
            
        for inp in inputs[1:-1]:
            old_down = self.down
            self.down = NetsFactory.getNet()
            self.lines.append(PartFactory.getPart() + " vcc " + inp + " " + self.output + " vcc " + self.P_model + " " + self.params_pmos)
            self.lines.append(PartFactory.getPart() + " " + old_down + " " + inp + " " + self.down + " gnd " + self.N_model + " " + self.params_nmos)
        
        self.lines.append(PartFactory.getPart() + " vcc " + inputs[-1] + " " + self.output + " vcc " + self.P_model + " " + self.params_pmos)
        self.lines.append(PartFactory.getPart() + " " + self.down + " " + inputs[-1] + " gnd gnd " + self.N_model + " " + self.params_nmos)
        

class And(Gate):
    def __init__(self, inputs):
        a = Nand(inputs)
        inv = Inverter(a)
        self.lines = inv.getNetlist()
        self.output = inv.getOutput()
        del(a)
        
class Nor(Gate):
    def __init__(self, inputs):
        self.lines = []
        self.output = NetsFactory.getNet()
        self.down = NetsFactory.getNet()
        self.lines.append(PartFactory.getPart() + " vcc " + inputs[0] + " " + self.down + " vcc " + self.P_model + " " + self.params_pmos + " ;nor")
        self.lines.append(PartFactory.getPart() + " " + self.output + " " + inputs[0] + " gnd gnd " + self.N_model + " " + self.params_nmos)
            
        for inp in inputs[1:-1]:
            self.down = NetsFactory.getNet()
            self.lines.append(PartFactory.getPart() + " " + self.down + " " + inp + " " + self.output + " vcc " + self.P_model + " " + self.params_pmos)
            self.lines.append(PartFactory.getPart() + " " + self.output + " " + inp + " " + " gnd gnd " + self.N_model + " " + self.params_nmos)
        
        self.lines.append(PartFactory.getPart() + " " + self.down + " " + inputs[-1] + " " + self.output + " vcc " + self.P_model + " " + self.params_pmos)
        self.lines.append(PartFactory.getPart() + " " + self.output + " " + inputs[-1] + " gnd gnd " + self.N_model + " " + self.params_nmos)


class Or(Gate):
    def __init__(self, inputs):
        a = Nor(inputs)
        inv = Inverter(a)
        self.lines = inv.getNetlist()
        self.output = inv.getOutput()
        del(a)

class SingleInput(Gate):
    def __init__(self, singleinput, negate=False):
        if negate:            # tworzy inwerter gdy podane wejscie jest zanegowane
            self.output = NetsFactory.getNet()
            self.lines = []
            self.lines.append(PartFactory.getPart() + " vcc " + singleinput + " " + self.output + " vcc " + self.P_model + " " + self.params_pmos + " ;inwerter SingleInput")
            self.lines.append(PartFactory.getPart() + " " + self.output + " " + singleinput + " gnd gnd " + self.N_model + " " + self.params_nmos)
        else:
            self.output = singleinput
            self.lines = ""
 
class Inverter(Gate):
    def __init__(self, gate):
        signal = gate.getOutput()
        self.output = NetsFactory.getNet()
        self.lines = gate.getNetlist()
        self.lines.append(PartFactory.getPart() + " vcc " + signal + " " + self.output + " vcc " + self.P_model + " " + self.params_pmos + " ;inwerter bramki")
        self.lines.append(PartFactory.getPart() + " " + self.output + " " + signal + " gnd gnd " + self.N_model + " " + self.params_nmos)

#TODO przeciążenie konstruktora dla inwertera
        
    
