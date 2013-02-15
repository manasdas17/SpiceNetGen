#!/usr/bin/python
# -*- coding: utf-8 -*-

class NetsFactory:                                ## metoda zwraca kolejne numery NETów, coby się nie powtarzały
    net_id = 0
 
    @staticmethod
    def getNet():
        NetsFactory.net_id += 1
        return "N_" + str(NetsFactory.net_id)
    
    @staticmethod
    def getLastNet():
        return "N_" + str(NetsFactory.net_id)
    
    @staticmethod
    def reset():
        NetsFactory.net_id = 0

    
class PartFactory:                                ## zwraca numery elementów /tranzystorów/
    part_id = 0
    @staticmethod
    def getPart():
        PartFactory.part_id += 1
        return "M" + str(PartFactory.part_id)
    
    @staticmethod
    def reset():
        PartFactory.part_id = 0