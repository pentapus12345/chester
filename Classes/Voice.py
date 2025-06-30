import pyttsx3

class Voice(object):
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty("voice","com.apple.voice.compact.en-GB.Daniel")
        self.engine.setProperty("rate", 160)
        self.print_to_screen=True
        self._last_text = ""
        self.say("")

    def set_print_to_screen(self, print_to_screen: bool):
        self.print_to_screen = print_to_screen

    def say(self, text: str)->None:
        if text == self._last_text:
            return
        self._last_text = text
        self.engine.say( text ) # uncomment when you have a speaker
        self.engine.runAndWait()

        if self.print_to_screen:
            print( f"Chester: {text}")

    def change_speaking_volume(self, change: float = .1)->None:
        volume = self.engine.getProperty("volume")
        new_volume = volume + change
        if new_volume > 1:
            new_volume = 0
        self.engine.setProperty("volume", new_volume)

    def change_speaking_speed(self, change: int = 10)->None:
        rate = self.engine.getProperty( "rate")
        new_rate = rate + change
        self.engine.setProperty("rate", new_rate)

    
