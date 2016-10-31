"""Main module."""
from kivy.config import Config
# Config.set('graphics','resizable',0)
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
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import NumericProperty
# from kivy.core.audio import SoundLoader

APP_VERSION = "1.0.0"

kivy.require('1.7.2')
Config.set('kivy', 'log_level', 'debug')

class ARLayout(RelativeLayout):
    # maximize the children given the ratio
    ratio = NumericProperty(3 / 4.)

    def do_layout(self, *args):
        for child in self.children:
            self.apply_ratio(child)
        super(ARLayout, self).do_layout()

    def apply_ratio(self, child):
        # ensure the child don't have specification we don't want
        child.size_hint = None, None
        child.pos_hint = {"center_x": .5, "center_y": .5}

        # calculate the new size, ensure one axis doesn't go out of the bounds
        w, h = self.size
        h2 = w * self.ratio
        if h2 > self.height:
            w = h / self.ratio
        else:
            h = h2
        child.size = w, h


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
        layout = ARLayout()
        layout.add_widget(sm)
        return layout

    def on_pause(self):
        """Handle suspend on android."""
        return True

if __name__ == '__main__':
    # Window.size = (800, 600)
    kwad.attach()
    tracker.tracker.send(tracker.EventBuilder().set(ec="app_start", ea=platform).build())
    tracker.ScreenViewBuilder.set_defaults(an="TrumpStamp",
                                           av=APP_VERSION,
                                           aid="com.trumpstamp.trumpstamp")
    # sound
    # sound = SoundLoader.load('music/The_Low_Seas.mp3')
    # if sound:
    #     print("Sound found at %s" % sound.source)
    #     print("Sound is %.3f seconds" % sound.length)
    #     sound.play()
    ElectionsApp().run()
