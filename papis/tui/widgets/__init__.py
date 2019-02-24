from prompt_toolkit.formatted_text.html import HTML
from prompt_toolkit.layout.processors import BeforeInput
from prompt_toolkit.filters import has_focus, Condition
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import ConditionalContainer
from prompt_toolkit.layout.containers import (
    HSplit, Window, WindowAlign, ConditionalContainer
)
from prompt_toolkit.layout.controls import (
    BufferControl,
    FormattedTextControl
)
from prompt_toolkit.widgets import (
    HorizontalLine
)
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers import find_lexer_class_by_name
import logging

from .list import OptionsListControl

logger = logging.getLogger('pick')


class CommandLinePrompt(ConditionalContainer):
    """
    A vim-like command line prompt widget.
    It's supposed to be instantiated only once.
    """
    instance = None
    def __init__(self):
        CommandLinePrompt.instance = self
        self.buf = Buffer()
        self.buf.text = ''
        self.window = Window(
            content=BufferControl(
                buffer=self.buf,
                input_processors=[BeforeInput(':')]
            ),
            height=1
        )
        super(CommandLinePrompt, self).__init__(
            content=self.window,
            filter=has_focus(CommandLinePrompt.instance)
        )


class InfoWindow(ConditionalContainer):

    instance = None
    def __init__(self):
        InfoWindow.instance = self
        self.buf = Buffer()
        self.buf.text = ''
        self.lexer = PygmentsLexer(find_lexer_class_by_name('yaml'))
        self.window = HSplit([
            HorizontalLine(),
            Window(
                content=BufferControl(
                    buffer=self.buf, lexer=self.lexer)
            )
        ], height=20)
        super(InfoWindow, self).__init__(
            content=self.window,
            filter=has_focus(InfoWindow.instance)
        )

    def set_text(self, text):
        self.buf.text = text

    def get_text(self):
        return self.buf.text


class HelpWindow:
    shown = False
    text = """
    <span fg='ansired'> Bindings: </span>

----------------------------------------------------
/   Ctrl-e, Ctrl-down, Shift-down : Scroll Down     /
/   Ctrl-y, Ctrl-up,   Shift-up   : Scroll up       /
/   Ctrl-n, down                  : Next item       /
/   Ctrl-p, up                    : Previous item   /
/   Ctrl-q, Ctrl-c                : Quit            /
/   Home                          : First item      /
/   End                           : Last item       /
----------------------------------------------------
    """

    @Condition
    def is_shown():
        return HelpWindow.shown

    def __init__(self):
        self.format_text_control = FormattedTextControl(
            key_bindings=None,
            show_cursor=False,
            focusable=False,
            text=HTML(self.text)
        )
        self.window = ConditionalContainer(
            content=Window(
                content=self.format_text_control,
                align=WindowAlign.CENTER
            ),
            filter=HelpWindow.is_shown
        )