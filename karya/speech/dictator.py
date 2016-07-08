from speech.lexical_analyser import DictatorActions
from speech.speechrecogniser import SpeechStates
from utilities import Writer


class Dictator:
    def __init__(self, speech_recogniser):

        self.speech_recogniser = speech_recogniser
        self.speech_recogniser.connect('state_changed', self.on_recogniser_state_changed)
        self.is_on = False

    def on_recogniser_state_changed(self, recogniser, state, text, msg):
        print(self.is_on)
        if state is not SpeechStates.recognised:
            return
        if text is '':
            return
        curr_action, num, special = DictatorActions.decide_action(text)
        print(curr_action)
        if curr_action == "start_dictation":
            self.is_on = True
        elif not self.is_on:
            return

        if curr_action == "stop_dictation":
            self.is_on = False
        if curr_action == "continue_dictation":
            Writer.inserttext(text, True)
        elif curr_action == "put":
            if special != "":
                for _ in range(num):
                    if 'digit' in special:
                        # using the format how digits are saved
                        Writer.inserttext(DictatorActions.digits[special][0])
                    else:
                        # sure that the special is not a digit, again using the format how specials are saved
                        Writer.inserttext(DictatorActions.special_chars[special][0])
                Writer.inserttext(' ')
        elif curr_action == "undo":
            Writer.undo()
        elif curr_action == "redo":
            Writer.redo()
        elif curr_action == "cut_clipboard":
            Writer.cut_clipboard()
        elif curr_action == "copy_clipboard":
            Writer.copy_clipboard()
        elif curr_action == "paste_clipboard":
            Writer.paste_clipboard()
        elif curr_action == "delete_selection":
            Writer.delete_selection()
        elif curr_action == "select_all":
            Writer.select_all()
        elif curr_action == "sentence_end":
            Writer.inserttext('. ')
        elif curr_action == "line_end":
            Writer.inserttext('\n')
        elif curr_action == "clear_document":
            Writer.clear_document()
