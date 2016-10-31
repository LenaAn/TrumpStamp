"""Main module."""
import kivy
import kwad
from kivy.app import App
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager
from kivy.utils import platform
import start_screen
import end_screen
import tracker
#from plyer.facades.uniqueid import UniqueID
from kivy.storage.jsonstore import JsonStore

APP_VERSION = "1.0.0"

kivy.require('1.7.2')
Config.set('kivy', 'log_level', 'debug')

class ElectionsApp(App):
    """Main app."""

    start_screen_name = "startscreen"
    end_screen_name = "endscreen"
    game_screen_name = "electionsgame"

    def build(self):
        """Init screen manager."""
        sm = ScreenManager()
        start_screen_ = start_screen.StartScreen(sm, name=self.start_screen_name)
        sm.switch_to(start_screen_)
        # end_screen_ = end_screen.EndScreen(sm, 'Trump')
        # sm.switch_to(end_screen_)
        return sm

    def on_pause(self):
        """Handle suspend on android."""
        return True

if __name__ == '__main__':
    kwad.attach()
    tracker.tracker.send(tracker.EventBuilder().set(ec="app_start", ea=platform).build())
    tracker.ScreenViewBuilder.set_defaults(an="TrumpStamp",
                                           av=APP_VERSION,
                                           aid="com.trumpstamp.trumpstamp")
    ElectionsApp().run()
