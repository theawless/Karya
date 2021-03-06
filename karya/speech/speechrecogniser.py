import logging
from enum import Enum

import speech_recognition as sr
from gi.repository import GObject, GLib, Gtk

from settings.speechsettings import SpeechSettingsHandler

logger = logging.getLogger(__name__)
PREPARE_DURATION = 2


class SpeechStates(Enum):
    started = 0
    preparing = 1
    prepared = 2
    stopping = 3
    stopped = 4
    recognising = 5
    error = 6

    recognised = 7
    fatal_error = 8


class SpeechRecogniser(GObject.GObject):
    __gsignals__ = {
        'state_changed': (GObject.SIGNAL_RUN_FIRST, None, (object, str, str))
    }
    state = GObject.property(type=object)

    def __init__(self):
        GObject.GObject.__init__(self)
        self.source = None
        self.re = sr.Recognizer()
        self.mic = sr.Microphone()
        self.re_stopper = None
        self.is_listening = False
        self.is_prepared = False
        self.noise_level = None
        self.settings = SpeechSettingsHandler().config
        self.set_property('state', SpeechStates.stopped)

    def change_state(self, state, text, msg):
        # we emit signal in the main thread
        GLib.idle_add(self.emit, 'state_changed', state, text, msg)
        # finish gtk events -- not sure if this is the right place
        while Gtk.events_pending():
            Gtk.main_iteration()

    # called automatically after each state change
    def do_state_changed(self, state, recognised_txt, msg):
        # print('state_changed', state, recognised_txt, msg)
        self.set_property('state', state)
        if state is SpeechStates.fatal_error:
            self.stop_recognising()

    def start_recognising(self):
        if not self.is_prepared:
            self.setup_recogniser()
        if not self.is_listening:
            self.re_stopper = self.re.listen_in_background(self.mic, self.recog_callback)
            self.is_listening = True
            self.emit('state_changed', SpeechStates.started, "", "")
        else:
            self.stop_recognising()
            self.start_recognising()

    def setup_recogniser(self):
        self.change_state(SpeechStates.preparing, "", "")
        if self.is_listening:
            self.re.adjust_for_ambient_noise(self.source, duration=PREPARE_DURATION)
            self.change_state(SpeechStates.prepared, "", "")
        elif not self.is_listening:
            with self.mic as source:
                self.source = source
                self.re.adjust_for_ambient_noise(source, duration=PREPARE_DURATION)
                self.change_state(SpeechStates.prepared, "", "")
        self.is_prepared = True

    def stop_recognising(self):
        if self.is_listening:
            self.change_state(SpeechStates.stopping, "", "")
            self.re_stopper()
        self.is_listening = False
        self.change_state(SpeechStates.stopped, "", "")

    def recog_callback(self, r, audio):
        """
        Called from different thread. Uses inherited emit.
        Callback for start_recogniser, converts speech to text.
        """
        settings = self.settings
        sel = settings['Main']['recogniser']
        r.dynamic_energy_threshold = settings['Main']['dynamic_noise_suppression']
        recognized_text = ""
        # Recogniser begins
        if sel == "Sphinx":
            # Use Sphinx as recogniser
            self.change_state(SpeechStates.recognising, "", "Got your words! Processing with Sphinx")
            logger.debug("recognize speech using Sphinx")
            try:
                recognized_text = r.recognize_sphinx(audio)
                logger.debug("From recogniser module: " + recognized_text)
            except sr.UnknownValueError:
                self.change_state(SpeechStates.error, "", "Sphinx could not understand audio")
            except sr.RequestError as e:
                self.change_state(SpeechStates.fatal_error, "", "Sphinx error; {0}".format(e))
            finally:
                self.change_state(SpeechStates.recognised, recognized_text, "")

        elif sel == "Google":
            if settings['Google']['api_key'] != "":
                # Use Google with API KEY as recogniser
                google_api_key = settings['Google']['api_key']
                self.change_state(SpeechStates.recognising, "",
                                  "Got your words! Processing with Google Speech Recognition")
                logger.debug("recognize speech using Google Key Speech Recognition")
                try:
                    recognized_text = r.recognize_google(audio, google_api_key)
                    logger.debug("From recogniser module G : " + recognized_text)
                except sr.UnknownValueError:
                    self.change_state(SpeechStates.error, "",
                                      "Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    self.change_state(SpeechStates.fatal_error, "",
                                      "Could not request results from Google Speech Recognition service; {0}".format(e))
                finally:
                    self.change_state(SpeechStates.recognised, recognized_text, "")
            else:
                self.change_state(SpeechStates.recognising, "",
                                  "Got your words! Processing with Google Speech Recognition")
                logger.debug("recognize speech using Google Speech Recognition")
                try:
                    recognized_text = r.recognize_google(audio)
                    logger.debug("From recogniser module G : " + recognized_text)
                except sr.UnknownValueError:
                    self.change_state(SpeechStates.error, "",
                                      "Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    self.change_state(SpeechStates.fatal_error, "",
                                      "Could not request results from Google Speech Recognition service; {0}".format(e))
                finally:
                    self.change_state(SpeechStates.recognised, recognized_text, "")

        elif sel == "WITAI":
            # recognize speech using Wit.ai
            self.change_state(SpeechStates.recognising, "", "Got your words! Processing with WIT.AI")
            logger.debug("recognize speech using WitAI Speech Recognition")

            wit_ai_key = settings['WITAI']['api_key']
            # Wit.ai keys are 32-character uppercase alphanumeric strings
            try:
                recognized_text = r.recognize_wit(audio, key=wit_ai_key)
                logger.debug("Wit.ai thinks you said " + recognized_text)
            except sr.UnknownValueError:
                self.change_state(SpeechStates.error, "", "Wit.ai could not understand audio")
            except sr.RequestError as e:
                self.change_state(SpeechStates.fatal_error, "",
                                  "Could not request results from Wit.ai service; {0}".format(e))
            finally:
                self.change_state(SpeechStates.recognised, recognized_text, "")

        elif sel == "Bing":
            # recognize speech using Microsoft Bing Voice Recognition
            self.change_state(SpeechStates.recognising, "", "Got your words! Processing with Bing")
            logger.debug("recognize speech using Bing Speech Recognition")
            bing_key = settings['Bing']['api_key']
            try:
                recognized_text = r.recognize_bing(audio, key=bing_key)
                logger.debug("Microsoft Bing Voice Recognition thinks you said " + recognized_text)
            except sr.UnknownValueError:
                self.change_state(SpeechStates.error, "",
                                  "Microsoft Bing Voice Recognition could not understand audio")
            except sr.RequestError as e:
                self.change_state(SpeechStates.fatal_error, "",
                                  "Could not request results from Microsoft Bing Voice Recognition service; {0}".format(
                                      e))
            finally:
                self.change_state(SpeechStates.recognised, recognized_text, "")

        elif sel == "APIAI":
            # recognize speech using api.ai
            self.change_state(SpeechStates.recognising, "", "Got your words! Processing with API.AI")
            logger.debug("recognize speech using APIAI Speech Recognition")

            api_ai_client_access_token = settings['APIAI']['api_key']
            try:
                recognized_text = r.recognize_api(audio, client_access_token=api_ai_client_access_token)
                logger.debug("api.ai thinks you said " + recognized_text)
            except sr.UnknownValueError:
                self.change_state(SpeechStates.error, "", "api.ai could not understand audio")
            except sr.RequestError as e:
                self.change_state(SpeechStates.fatal_error, "",
                                  "Could not request results from api.ai service; {0}".format(e))
            finally:
                self.change_state(SpeechStates.recognised, recognized_text, "")

        elif sel == "IBM":
            # recognize speech using IBM Speech to Text
            self.change_state(SpeechStates.recognising, "", "Got your words! Processing with IBM")
            logger.debug("recognize speech using IBM Speech Recognition")

            ibm_username = settings['IBM']['username']
            # IBM Speech to Text usernames are strings of the form XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
            ibm_password = settings['IBM']['password']
            # IBM Speech to Text passwords are mixed-case alphanumeric strings
            try:
                recognized_text = r.recognize_ibm(audio, username=ibm_username, password=ibm_password)
                logger.debug("IBM Speech to Text thinks you said " + recognized_text)
            except sr.UnknownValueError:
                self.change_state(SpeechStates.error, "",
                                  "IBM Speech to Text could not understand audio")
            except sr.RequestError as e:
                self.change_state(SpeechStates.fatal_error, "",
                                  "Could not request results from IBM Speech to Text service; {0}".format(e))
            finally:
                self.change_state(SpeechStates.recognised, recognized_text, "")
