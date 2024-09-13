#!/usr/bin/env python
import osc_npyscreen
import curses
#osc_npyscreen.disableColor()

class BeepForm(osc_npyscreen.ActionForm):
    def create(self, *args, **keywords):
        super(BeepForm, self).create(*args, **keywords)
        #self.keypress_timeout = 10
    
    def while_waiting(self):
        curses.beep()
        
        
class TestApp(osc_npyscreen.NPSApp):
    def while_waiting(self):
        curses.beep()
        
    def main(self):
        # These lines create the form and populate it with widgets.
        # A fairly complex screen in only 8 or so lines of code - a line for each control.
        self.keypress_timeout_default = 10
        F = BeepForm(parentApp=self, name = "Welcome to Oscscreen",)
        t = F.add(osc_npyscreen.TitleText, name = "Text:", )
        fn = F.add(osc_npyscreen.TitleFilename, name = "Filename:")
        dt = F.add(osc_npyscreen.TitleDateCombo, name = "Date:")
        s = F.add(osc_npyscreen.TitleSlider, out_of=12, name = "Slider", color='DANGER')
        ml= F.add(osc_npyscreen.MultiLineEdit, 
            value = """try typing here!\nMutiline text, press ^R to reformat.\n""", 
            max_height=5, rely=9)
        ms= F.add(osc_npyscreen.TitleSelectOne, max_height=4, value = [1,], name="Pick One", 
                values = ["Option1","Option2","Option3"], scroll_exit=True)
        
        # This lets the user play with the Form.
        F.edit()


if __name__ == "__main__":
    App = TestApp()
    App.run()
