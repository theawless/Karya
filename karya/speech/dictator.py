from speech.lexical_analyser.dictatoractions import DictatorActions
from speech.speechrecogniser import SpeechStates


class Dictator:
    def __init__(self, speech_recogniser):
        self.speech_recogniser = speech_recogniser
        self.speech_recogniser.connect('state_changed', self.on_recogniser_state_changed)
        self.is_on = False

    def on_recogniser_state_changed(self, recogniser, state, text, msg):
        if state is not SpeechStates.recognised:
            return
        if text is '':
            return
        curr_action, num, special = DictatorActions.decide_action(text)

        if curr_action == "start_dictation":
            self.is_on = True

        if not self.is_on:
            return

        if curr_action == "stop_dictation":
            self.is_on = False
        elif curr_action == "put":
            if special != "":
                for _ in range(num):
                    if 'digit' in special:
                        # using the format how digits are saved
                        self.inserttext(DictatorActions.digits[special][0])
                    else:
                        # sure that the special is not a digit, again using the format how specials are saved
                        self.inserttext(DictatorActions.special_chars[special][0])
                self.inserttext(' ')
        elif curr_action == "undo":
            doc = self.document
            if not doc:
                return
            for _ in range(num):
                if doc.can_undo():
                    doc.undo()
        elif curr_action == "redo":
            doc = self.document
            if not doc:
                return
            for _ in range(num):
                if doc.can_redo():
                    doc.redo()
        elif curr_action == "cut_clipboard":
            vi = self.view
            if not vi:
                return
            vi.cut_clipboard()
        elif curr_action == "copy_clipboard":
            vi = self.view
            if not vi:
                return
            vi.copy_clipboard()
        elif curr_action == "paste_clipboard":
            vi = self.view
            if not vi:
                return
            vi.paste_clipboard()
        elif curr_action == "delete_selection":
            vi = self.view
            if not vi:
                return
            vi.delete_selection()
        elif curr_action == "select_all":
            vi = self.view
            if not vi:
                return
            vi.select_all()
        elif curr_action == "sentence_end":
            self.inserttext('. ')
        elif curr_action == "line_end":
            self.inserttext('\n')
        elif curr_action == "clear_document":
            doc = self.document
            if not doc:
                return
            doc.begin_user_action()
            doc.set_text('')
            doc.end_user_action()
