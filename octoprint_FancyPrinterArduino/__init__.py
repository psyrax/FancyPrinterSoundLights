# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin
import serial.tools.list_ports
import serial 

class FancyprinterarduinoPlugin(
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.SettingsPlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.EventHandlerPlugin
):

    portList = []
    serialCon = ''
    serialOpen = False
    def serialOpen(self, port):
        try:
            self.serialCon = serial.Serial(port, 115200)
            self.serialOpen = True
        except:
            print('Serial failed')

    def sendSerialMsg(self, msg):
        if(self.serialOpen):
            self.serialCon.write('{}\r\n'.format(msg).encode())

    def on_event(self, event, payload):
        if event == 'Startup':
            ports = serial.tools.list_ports.comports()
            for port, desc, hwid in sorted(ports):
                self.portList.append(port)
            if self._settings.get(["selectedPort"]) != '':
                self.serialOpen(self._settings.get(["selectedPort"]))         
            self.sendSerialMsg('8')

        if event == 'PrintStarted':
            self.sendSerialMsg('3')
            self.sendSerialMsg('l')
        
        if event == 'Upload':
            self.sendSerialMsg('4')
        
        if event == 'PrintDone':
            self.sendSerialMsg('2')
            self.sendSerialMsg('o')

        if event in ['PrintFailed', 'PrintCancelled']:
            self.sendSerialMsg('6')
            self.sendSerialMsg('o')

    ### PrintFailed, PrintDone, PrintCancelling, PrintCancelled, PrintPaused, PrintResumed, 


 
    ##~~ SettingsPlugin mixin

    def get_settings_defaults(self):
        selectedPort = 'nope'
        return {
            'ports': self.portList,
            'selectedPort': selectedPort
        }

    def get_template_configs(self):
        return [
            dict(type="settings", custom_bindings=False)
        ]

    def get_template_vars(self):
        return {
            'ports' : self._settings.get(["ports"]),
            'selectedPort' : self._settings.get(["selectedPort"])
        }

    ##~~ AssetPlugin mixin

    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return {
            "js": ["js/FancyPrinterArduino.js"],
            "css": ["css/FancyPrinterArduino.css"],
            "less": ["less/FancyPrinterArduino.less"]
        }

    ##~~ Softwareupdate hook

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
        # for details.
        return {
            "FancyPrinterArduino": {
                "displayName": "Fancyprinterarduino Plugin",
                "displayVersion": self._plugin_version,

                # version check: github repository
                "type": "github_release",
                "user": "psyrax",
                "repo": "OctoPrint-Fancyprinterarduino",
                "current": self._plugin_version,

                # update method: pip
                "pip": "https://github.com/psyrax/OctoPrint-Fancyprinterarduino/archive/{target_version}.zip",
            }
        }


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Fancyprinterarduino Plugin"

# Starting with OctoPrint 1.4.0 OctoPrint will also support to run under Python 3 in addition to the deprecated
# Python 2. New plugins should make sure to run under both versions for now. Uncomment one of the following
# compatibility flags according to what Python versions your plugin supports!
#__plugin_pythoncompat__ = ">=2.7,<3" # only python 2
#__plugin_pythoncompat__ = ">=3,<4" # only python 3
__plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = FancyprinterarduinoPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
