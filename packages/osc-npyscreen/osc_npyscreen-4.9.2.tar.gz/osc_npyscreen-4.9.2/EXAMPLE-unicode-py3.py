#!/usr/bin/env python
# encoding: utf-8

import osc_npyscreen
#osc_npyscreen.disableColor()
class TestApp(osc_npyscreen.NPSApp):
	def main(self):
		# These lines create the form and populate it with widgets.
		# A fairly complex screen in only 8 or so lines of code - a line for each control.
		F = osc_npyscreen.ActionForm(name = "Welcome to Oscscreen",)
		t = F.add(osc_npyscreen.TitleText, name = "Text:", value= "This is unicode: éé ≈∂ƒ© and it works on unicode terminals")
		fn = F.add(osc_npyscreen.TitleFilename, name = "Filename:")
		dt = F.add(osc_npyscreen.TitleDateCombo, name = "Date:")
		s = F.add(osc_npyscreen.TitleSlider, out_of=12, name = "Slider")
		ml= F.add(osc_npyscreen.MultiLineEdit, 
			value = """try typing here!\nMutiline text, press ^R to reformat.\n""", 
			max_height=5, rely=9)
		cb = F.add(osc_npyscreen.Checkbox, name = "A Checkbox é")
		bn = F.add(osc_npyscreen.MiniButton, name = "Button Testing Testing éß",)

		ms= F.add(osc_npyscreen.TitleSelectOne, max_height=2, value = [1,], name="Pick One", 
				values = ["Option1","Option2","Option3"], scroll_exit=True)
		
		
		ms2= F.add(osc_npyscreen.TitleMultiSelect, max_height=2, value = [1,], name="Pick Several", 
				values = ["Option1","Option2","Option3"], scroll_exit=True)
        
		# This lets the user play with the Form.
		F.edit()


if __name__ == "__main__":
	App = TestApp()
	App.run()
	App = TestApp()
	App.run()
	
