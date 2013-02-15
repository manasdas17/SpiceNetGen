#!/usr/bin/python
# -*- coding: utf-8 -*-

import gtk
import proj
import os

class Interface(object):       
	
	spice_bin_file = 'spice_location.txt'
	out_file_value = ""
	spice_binary = ""
	
	def on_window_destroy(self, widget, data=None):
		gtk.main_quit()
		
	def spice_binary_set(self, widget, data=None):
		self.spice_binary = self.spice_executable.get_filename()
		
		f = open(self.spice_bin_file, 'w')
		f.write(self.spice_binary)
		f.close()
		pass	
			
	def get_mos_params(self):		## pobiera rozmiary ze SpinButtonów
		tab = []
		for x in self.sbuttons:
			tab.append(int(x.get_value())) 
		return [ self.mos_type.get_active(), " l=" + str(tab[0])+"n" + " w=" + str(tab[1])+"n", " l=" + str(tab[2])+"n" + " w=" + str(tab[3])+"n" ]
#		return [ self.mos_type.get_active(), " l=" + str(tab[0]) + " w=" + str(tab[1]), " l=" + str(tab[2]) + " w=" + str(tab[3]) ]
	
	def run_spice(self, widget, data=None):
		print 'wine "' + self.spice_binary + '" ' + self.out_file_value + ' &' 
		if self.spice_binary != "":
			os.system('wine "' + self.spice_binary + '" ' + self.out_file_value + ' &' )

	def btn_clicked(self, widget, data=None):

		if len(self.tb.get_text()) == 0:			
			return

		nl = proj.NetList()
		simulation_time = self.simtime.get_text()
		params = self.get_mos_params()
		if self.mos_type.get_active() == 2:
			tech_file = self.mos_tech_file.get_filename()
		else:
			tech_file = None	
		
		nl.makeNetwork(self.tb.get_text(), params, simulation_time, tech_file)
		
		self.out_file_value = self.output_file.get_text() 

		# zapis do pliku
		outfile = open(self.out_file_value, 'w')
		for linia in nl.lista:
			outfile.write(linia + '\n')
		outfile.close()
		
	def component_type_change(self, widget):
		if self.mos_type.get_active() >= 1:		## dla n/pMOS4 uaktywnia wybór rozmiaru kanału
			val = True
		else:
			val = False
		for x in self.sbuttons:
			x.set_sensitive(val)
		
		if self.mos_type.get_active() == 2:			## dla pliku tech uaktywnia pole wyboru pliku
			self.mos_tech_file.set_sensitive(True)
		else:
			self.mos_tech_file.set_sensitive(False)
			
	
	def __init__(self):
		builder = gtk.Builder()
		builder.add_from_file("interfejs.glade")
		builder.connect_signals(self)
		
		######################## KOMPONENTY
		
		# podłączenie komponentów
		self.window = builder.get_object("mainWindow")
		self.tb = builder.get_object("formula_TB")
		self.mos_type = builder.get_object("component_type")
		self.spice_executable = builder.get_object("spice_binary")
		self.output_file = builder.get_object("output_file")
		self.mos_tech_file = builder.get_object("mos_tech_file")
		self.simtime = builder.get_object("sim_time")
		
		#podpięcie SpinButtonów
		self.sbuttons = []
		for x in range(1,4+1):
			self.sbuttons.append(builder.get_object("spinbutton"+str(x)))
			
		#######################################################
		
		## generowanie listy do ComboBoxa z wyborem typu tranzystora
		model=gtk.ListStore(str)
		self.mos_type.set_model(model)
		cell = gtk.CellRendererText()
		self.mos_type.pack_start(cell, True)
		self.mos_type.add_attribute(cell, 'text', 0)
		mos_values = ["nMOS/pMOS", "nMOS4/pMOS4", "nMOS4/pMOS4 z plikiem tech."]
		for x in mos_values:
			self.mos_type.append_text(x)
		self.mos_type.set_active(0)
		
		## probujemy odczytać plik w którym zapisana jest ostatnia prawidlowa lokalizacja scad3, coby nie trzeba wybierać
		#  za każdym uruchomieniem programu
		
		try:
			f = open(self.spice_bin_file, 'r')
		finally:
			path = f.readline()
			f.close()
			self.spice_binary = path
			self.spice_executable.set_filename(path)
		
		
		

if __name__ == "__main__":
	app = Interface()
	app.window.show()
	gtk.main()
