#!/usr/bin/env python
# encoding: utf-8


# The system here is an experimental one. See documentation for details.




import osc_npyscreen
class TestApp(osc_npyscreen.NPSApp):
    def main(self):
        Options = osc_npyscreen.OptionList()
        
        # just for convenience so we don't have to keep writing Options.options
        options = Options.options
        
        options.append(osc_npyscreen.OptionFreeText('FreeText', value='', documentation="This is some documentation."))
        options.append(osc_npyscreen.OptionMultiChoice('Multichoice', choices=['Choice 1', 'Choice 2', 'Choice 3']))
        options.append(osc_npyscreen.OptionFilename('Filename', ))
        options.append(osc_npyscreen.OptionDate('Date', ))
        options.append(osc_npyscreen.OptionMultiFreeText('Multiline Text', value=''))
        options.append(osc_npyscreen.OptionMultiFreeList('Multiline List'))
        
        try:
            Options.reload_from_file('/tmp/test')
        except FileNotFoundError:
            pass        
        
        F  = osc_npyscreen.Form(name = "Welcome to Oscscreen",)

        ms = F.add(osc_npyscreen.OptionListDisplay, name="Option List", 
                values = options, 
                scroll_exit=True,
                max_height=None)
        
        F.edit()
        
        Options.write_to_file('/tmp/test')

if __name__ == "__main__":
    App = TestApp()
    App.run()   
