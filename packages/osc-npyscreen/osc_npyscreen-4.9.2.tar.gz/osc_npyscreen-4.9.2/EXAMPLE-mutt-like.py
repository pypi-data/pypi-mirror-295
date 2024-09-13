#!/usr/bin/env python
import osc_npyscreen

class TestApp(osc_npyscreen.NPSApp):
    def main(self):
        F = osc_npyscreen.FormMutt()
        F.add
        F.wStatus1.value = "Status Line "
        F.wStatus2.value = "Second Status Line "
        F.wMain.values   = [str(x) for x in range(500)]
        
        F.edit()


if __name__ == "__main__":
    App = TestApp()
    App.run()
