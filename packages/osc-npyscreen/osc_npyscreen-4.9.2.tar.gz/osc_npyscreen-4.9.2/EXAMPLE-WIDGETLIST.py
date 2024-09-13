#!/usr/bin/env python
import osc_npyscreen
#osc_npyscreen.disableColor()
class ActionFormExample(osc_npyscreen.ActionForm):
	initialWidgets = [
		(osc_npyscreen.TitleText,      {'w_id': 'TextLine', 'name': "Text:"}),
		(osc_npyscreen.TitleFilename,  {'name' : "Filename:"}),
		(osc_npyscreen.TitleFilename,  {'name' : "Filename:"}),
		(osc_npyscreen.TitleDateCombo, {'name' : "Date:"}),
		(osc_npyscreen.TitleSlider,    {'out_of': 12, 'name' : "Slider"}),
		(osc_npyscreen.MultiLineEdit,  {'value' : """try typing here!\nMutiline text, press ^R to reformat.\n""", 'max_height': 5,})
	]

class TestApp(osc_npyscreen.NPSApp):
	def main(self):
		# These lines create the form and populate it with widgets.
		# A fairly complex screen in only 8 or so lines of code - a line for each control.
		F = ActionFormExample(name = "Welcome to Oscscreen",)
	   #t = F.add(osc_npyscreen.TitleText, name = "Text:", )
	   #fn = F.add(osc_npyscreen.TitleFilename, name = "Filename:")
	   #dt = F.add(osc_npyscreen.TitleDateCombo, name = "Date:")
	   #s = F.add(osc_npyscreen.TitleSlider, out_of=12, name = "Slider")
	   #ml= F.add(osc_npyscreen.MultiLineEdit, 
	   #	value = """try typing here!\nMutiline text, press ^R to reformat.\n""", 
	   #	max_height=5, rely=9)
	   #ms= F.add(osc_npyscreen.TitleSelectOne, max_height=4, value = [1,], name="Pick One", 
	   #		values = ["Option1","Option2","Option3"], scroll_exit=True)
	   #ms2= F.add(osc_npyscreen.TitleMultiSelect, max_height=4, value = [1,], name="Pick Several", 
	   #		values = ["Option1","Option2","Option3"], scroll_exit=True)
	   #
		# This lets the user play with the Form.
		F.edit()
		return F.get_widget('TextLine').value

if __name__ == "__main__":
	App = TestApp()
	print App.run()
