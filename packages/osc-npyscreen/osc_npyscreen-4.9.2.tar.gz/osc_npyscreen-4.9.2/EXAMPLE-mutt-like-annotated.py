#!/usr/bin/env python
import osc_npyscreen

class TestListClass(osc_npyscreen.MultiLine):
	_contained_widgets = osc_npyscreen.AnnotateTextboxBase

class TestForm(osc_npyscreen.FormMutt):
	MAIN_WIDGET_CLASS = TestListClass

class TestApp(osc_npyscreen.NPSApp):
    def main(self):
        F = TestForm()
        F.wStatus1.value = "Status Line "
        F.wStatus2.value = "Second Status Line "
        F.wMain.values   = [str(x) for x in range(500)]
        
        F.edit()


if __name__ == "__main__":
    App = TestApp()
    App.run()
