import gi

from settings.speechsettings import SpeechSettingsHandler
from speech.speechrecogniser import SpeechStates

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


class SpeechInfoBar:
    def __init__(self, speech_recogniser):

        # initialize the speech settings once
        self.speech_settings = SpeechSettingsHandler()
        self.speech_settings.load_settings()

        self.info_bar = Gtk.InfoBar()
        self._setup_status_label()
        self._setup_infobar_menu()
        # TO-DO find a better way to colour it
        self.info_bar.modify_bg(Gtk.StateType.NORMAL, Gdk.Color.parse('gray')[1])
        self.info_bar.show()

        self._speech_recogniser = speech_recogniser
        self._speech_recogniser.connect('state_changed', self.on_speech_state_changed)

    def _setup_status_label(self):
        self.info_bar.set_message_type(Gtk.MessageType.OTHER)
        self.speech_status_label = Gtk.Label('Welcome to Karya!')
        self.speech_status_label.set_justify(Gtk.Justification.CENTER)
        self.speech_status_label.show()
        self.info_bar.get_content_area().pack_start(self.speech_status_label, True, True, 0)

        self.speech_error_label = Gtk.Label('Error messages to be shown here.')
        self.speech_error_label.show()

    def _setup_infobar_menu(self):
        # not using direct packing -to make the button smaller in size, info bar stretches them otherwise
        content_box = Gtk.Box()
        content_box.show()

        self.speech_button = Gtk.ToolButton()
        self.speech_button.set_icon_widget(Gtk.Image.new_from_icon_name('media-record', Gtk.IconSize.SMALL_TOOLBAR))
        self.speech_button.show_all()
        self.speech_button.connect('clicked', self.speech_button_clicked)
        content_box.pack_start(self.speech_button, False, False, 0)
        self.info_bar.get_action_area().pack_start(content_box, False, False, 0)
        self.mode_button = Gtk.ToolButton()
        self.mode_button.set_icon_widget(Gtk.Image.new_from_icon_name('go-up', Gtk.IconSize.SMALL_TOOLBAR))
        self.mode_button.show_all()
        self.mode_button.set_hexpand(False)
        content_box.pack_start(self.mode_button, False, False, 0)

    def speech_button_clicked(self, widget):
        if self._speech_recogniser.is_listening:
            self._speech_recogniser.stop_recognising()
        elif not self._speech_recogniser.is_listening:
            self._speech_recogniser.start_recognising()

    def on_speech_state_changed(self, speech_recogniser, state, recognised_text, msg):
        if state == SpeechStates.started:
            self.speech_status_label.set_text('Speak!')
        if state == SpeechStates.preparing:
            self.speech_status_label.set_text('Preparing...')
        if state == SpeechStates.prepared:
            self.speech_status_label.set_text('Prepared. Speak!')
        if state == SpeechStates.stopping:
            self.speech_status_label.set_text('Stopping!')
        if state == SpeechStates.stopped:
            self.speech_status_label.set_text('Stopped Listening.')
        if state == SpeechStates.recognising:
            self.speech_status_label.set_text('Processing...')
        if state == SpeechStates.error:
            self.speech_status_label.set_text('Error. Try speaking again.')
        if state == SpeechStates.recognised:
            self.speech_status_label.set_text('Got it!')
        if state == SpeechStates.fatal_error:
            self.speech_error_label.set_text('Whoops! Fatal Error!')
        while Gtk.events_pending():
            Gtk.main_iteration_do(True)
