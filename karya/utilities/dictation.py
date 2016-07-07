import logging

from speech.speechrecogniser import SpeechStates

logger = logging.getLogger(__name__)


class DictationProvider:
    def __init__(self, speech_recogniser):
        self.speech_recogniser = speech_recogniser
        self.speech_recogniser.connect('state_changed', self.on_speech_state_changed)

    def on_speech_state_changed(self, speech_recogniser, state, recognised_txt, msg):
        if state == SpeechStates.recognised:
            pass
