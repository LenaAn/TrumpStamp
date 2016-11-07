from kivy.core.audio import SoundLoader


class SoundManager(object):

    cache = dict()
    volume = 1

    @staticmethod
    def play_audio(url, loop=False):
        if url not in SoundManager.cache:
            SoundManager.cache[url] = SoundLoader.load(url)
        SoundManager.cache[url].volume = SoundManager.volume
        SoundManager.cache[url].loop = loop
        SoundManager.cache[url].play()

    @staticmethod
    def stop_audio(url):
        if url in SoundManager.cache:
            SoundManager.cache[url].stop()

    @staticmethod
    def stop_all_audio():
        for url in SoundManager.cache:
            SoundManager.cache[url].stop()

    @staticmethod
    def set_volume(new_volume):
        SoundManager.volume = new_volume
        for url, sound in SoundManager.cache.items():
            sound.volume = new_volume
