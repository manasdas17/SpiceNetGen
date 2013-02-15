#!/usr/bin/python
# -*- coding: utf-8 -*-

from LogicGates import And, Or, SingleInput
from Factories import PartFactory, NetsFactory
import LogicGates

def hello(inputs):							# generuje pierwsze potrzebne rzeczy w układzie - napięcie zasilania, sygnały prostokątne na wejścia ukladu
	result = []
	result.append("V_zas vcc gnd 5")		# zasilanko
	x = 0
	for inp in inputs:				# sygnały podajemy tylko na wejścia niezanegowane
		if inp[0] != '~':
			x += 1
			result.append("V" + str(x) + " " + inp + " gnd PULSE(0 " + str(4.0+(x-1)/20.0) + " 0 0.0001 0.0001 " + str((2**x)/2) + " " + str(2**x) + " 500)")
		
	return result

def goodbye(sim_time, tech_file):							## informacje końcowe , czas symulacji itp
	result = []
	if tech_file != None:
		result.append(".include " + tech_file)
	result.append(""".model NMOS NMOS
.model PMOS PMOS""")
	result.append(""".lib C:\Program Files\LTC\LTspiceIV\lib\cmp\standard.mos""")
	result.append(""".tran """ + sim_time + """
.backanno
.end
""")
	return result
	

def parseInput(formula):			# rozbija formułę
	formula = formula.split('+')		# najpierw po plusach (OR)
	for x in range(len(formula)):
		formula[x] = formula[x].split('*')		# później po '*' (AND)
	return formula	



class NetList():
	
	lista = []
	
	def makeNetwork(self, inp, params, sim_time, tech_file=None):
	
		self.lista = [inp]
		PartFactory.reset()				## fabryczki części zerujemy
		NetsFactory.reset()
		
		formula = parseInput(inp)			## parsujemy string wejściowy do tablicy tablic
		elements = []				## tablica z elementami
		negs = []					# .. z inwerterami
		inputs = {}					# słownik z wejściami

		
		if len(params) > 0 and params[0] >= 1:				## ustawiamy parametry tranzystorów
			LogicGates.Gate.params_pmos = params[1]
			LogicGates.Gate.params_nmos = params[2]
		else:
			LogicGates.Gate.params_pmos = ""
			LogicGates.Gate.params_nmos = ""
		
		if tech_file != None:
			LogicGates.Gate.P_model = "P_50n"
			LogicGates.Gate.N_model = "N_50n"
		else:
			LogicGates.Gate.P_model = "PMOS"
			LogicGates.Gate.N_model = "NMOS"
			
	# ↓ tu chodzi o to, żeby nie tworzyć kilku różnych wejść zegarowych
	# dla tej samej zmiennej która pojawia się wielokrotnie, tak samo
	# żeby nie było osobnego zegara dla X i ~X
	
		for x in range(len(formula)):				##
			for y in range(len(formula[x])):		## Wchodzimy w poszczególne zmienne
				if formula[x][y] not in inputs:			# jeżeli ta zmienna się jeszcze nie pojawiła
					if formula[x][y][0] != '~':						##i nie jest zanegowana, dodajemy normalnie do słownika
						inputs.update({formula[x][y] : formula[x][y]})		#
					else:										## jeśli jest zanegowana, 
						not_neg = formula[x][y][1:]				## dodajemy jej wersję niezanegowaną
						inputs.update({not_neg : not_neg})
						negs.append(SingleInput(not_neg, True))		## tworzymy negator
						formula[x][y] = negs[-1].getOutput()		   ## dalej będziemy używać wyjścia z nega
						inputs.update({ '~'+not_neg : formula[x][y]})		## dodajemy do słownika
				else:
					formula[x][y] = inputs[formula[x][y]]			## jeżeli zmienna już była, to zmieniamy ją na to co pojawiło się poprzednio
															## czyli tzw. nic dla zwykłych i na wyjście z nega dla poprzedzonych tyldą
					
					''' ↑ HERE GOES MAGIC! '''
						

	
	#	print negs
	#	print inputs
	#	print formula
		
		for x in formula:
	#		print "Got", x, "len:", len(x)
			if len(x) > 1:				# jezeli element nie jest elementem pojedynczym to zwraca anda
				elements.append(And(x))
			else:
				elements.append(SingleInput(x[0]))		# pojedyncze wejscia negujemy w razie potrzeby
	
	#	print elements
		

		
		if len(elements)>1:					
			orinput = []					# wali wszystkie wyjścia andów do jednej tablicy
			for x in elements:
				orinput.append(x.getOutput())		
	#		print "ORing:", orinput
			elements.append(Or(orinput))			# i sumuje je Orem
		
	#	print inputs
		
		
		elements = negs + elements				# dorzuca inwertery 
	
	#	print elements
		#hello(inputs)
		self.lista.extend(hello(inputs))			#hello, czyli napięcia
		
		for x in elements:
			for s in x.getNetlist():		# wrzuca do self.lista netlisty wszystkich elementów
				self.lista.append(s)		# linijka po linijce
		
		#print self.lista
		
		lastnet = NetsFactory.getLastNet()				
		for x in range(len(self.lista)):
			self.lista[x] = self.lista[x].replace(lastnet, 'output')	## zamienia nazwę ostatniej siatki na 'output' 
	
		self.lista.extend(goodbye(sim_time, tech_file))			# dodaje goodbye
	
		
	
