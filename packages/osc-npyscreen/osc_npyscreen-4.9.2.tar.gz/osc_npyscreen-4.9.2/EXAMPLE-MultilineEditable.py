#!/usr/bin/env python
# encoding: utf-8
import osc_npyscreen
#osc_npyscreen.disableColor()


class TestApp(osc_npyscreen.NPSApp):
    def main(self):
        value_list = [
           "This is the first",
           "This is the second",
           "This is the third",
           "This is the fourth",
        ]
        F  = osc_npyscreen.Form(name = "Welcome to Oscscreen",)
        t = F.add(osc_npyscreen.MultiLineEditableBoxed,
                        max_height=20,
                        name='List of Values',
                        footer="Press i or o to insert values", 
                        values=value_list, 
                        slow_scroll=False)
        
        # This lets the user play with the Form.
        F.edit()
        
if __name__ == "__main__":
    App = TestApp()
    App.run()   
