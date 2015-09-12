# coding=utf-8

import re
import sys
from datetime import datetime
import time
from functools import partial
import threading

from termcolor import colored, COLORS
import humanize


# We don't agree about the meaning of some colors
COLORS['black'] = COLORS['grey']
COLORS['grey'] = 90


ansi_escape = re.compile(r'\x1b[^m]*m')
def strip_ansi(text):
    return ansi_escape.sub('', text)


class NewLineManager(object):
    """
    Wrap a file descriptor, manage writing exactly one \n between lines
    """
    def __init__(self, fd):
        self.fd = fd
        self._are_we_on_new_line = True

    def write(self, s):
        if len(s) > 0:
            self.fd.write(s)
            self._are_we_on_new_line = False

    def new_line(self):
        if not self._are_we_on_new_line:
            self.fd.write('\n')
            self._are_we_on_new_line = True


out = NewLineManager(sys.stdout)


class TerminalWriterConfig(object):
    """
    Configuration defining all styles used in the output. Think CSS.
    """
    box_style = partial(colored, color='magenta')

    timestamp_format = '%H:%m:%S'
    timestamp_bracket_style = partial(colored, color='white')
    timestamp_style = partial(colored, color='grey')

    substeps_style = partial(colored, color='grey')

    progress_dot_style = partial(colored, color='grey')

    eta_style = partial(colored, color='grey')


class Substeps(object):
    """
    Manage output of line like:
    (1/2) First step
    (2/2) Second step
    """
    def __init__(self, config):
        """
        :type config: TerminalWriterConfig
        """
        self.config = config
        self.current = 0
        self.steps = -1

    def str(self):
        if self.current > self.steps:
            return ''
        else:
            retval = self.config.substeps_style('(%s/%s) ' % (self.current, self.steps))
            self.current += 1
            return retval

    def start(self, n):
        self.current = 1
        self.steps = n

    def reset(self):
        self.current = 0
        self.steps = -1


class DotterThread(threading.Thread):
    """
    A stoppable thread that outputs dots every N seconds.
    Used to indicate progress in short, but not immediately finishing tasks.
    """
    def __init__(self, interval_seconds, style):
        super(DotterThread, self).__init__()
        self._interval_seconds = interval_seconds
        self._stop = threading.Event()
        self._style = style
        self.setDaemon(True)

    def run(self):
        while not self._stop.is_set():
            out.write(self._style('.'))
            time.sleep(self._interval_seconds)

    def stop(self):
        self._stop.set()


class Dotter(object):
    """
    Manage DotterThreads
    """
    def __init__(self, config):
        """
        :type config: TerminalWriterConfig
        """
        self.config = config
        self.thread = None

    def start(self, interval_seconds):
        self.reset()
        self.thread = DotterThread(interval_seconds, self.config.progress_dot_style)
        self.thread.start()

    def reset(self):
        if self.thread is not None:
            self.thread.stop()
            self.thread = None


class EtaThread(threading.Thread):
    """
    A stoppable thread that updates an ETA at the end of the line, and writes the elapsed time once the task is done.
    Used to indicate progress in long-running tasks.
    """
    def __init__(self, line, seconds, style):
        super(EtaThread, self).__init__()
        self._line = line
        self._eta = seconds
        self._elapsed = 0
        self._stop = threading.Event()
        self._style = style
        self._last_printed = ''
        self.setDaemon(True)

    def _write(self, suffix):
        out.write('\r' + ' ' * len(strip_ansi(self._last_printed)) + '\r')
        self._last_printed = self._line + ' ' + suffix
        out.write(self._last_printed)

    def run(self):
        while not self._stop.is_set():
            eta = self._eta - self._elapsed
            self._write(self._style('(ETA: ' + humanize.naturaltime(eta, eta > 0) + ')'))
            time.sleep(1)
            self._elapsed += 1

    def stop(self):
        self._stop.set()
        self._write(self._style('(Finished in ' + humanize.naturaldelta(self._elapsed) + ')'))


class Eta(object):
    """
    Manage EtaThreads
    """
    def __init__(self, config):
        self.config = config
        self.thread = None

    def start(self, line, seconds):
        self.reset()
        self.thread = EtaThread(line, seconds, self.config.eta_style)
        self.thread.start()

    def reset(self):
        if self.thread is not None:
            self.thread.stop()
            self.thread = None


class TerminalWriter(object):
    """
    The public API
    """

    def __init__(self, config=None):
        """
        :type config: TerminalWriterConfig
        """
        if config is None:
            config = TerminalWriterConfig
        self._config = config
        self._substeps = Substeps(config)
        self._dotter = Dotter(config)
        self._eta = Eta(config)

    def box(self, text):
        self._substeps.reset()
        self._dotter.reset()
        self._eta.reset()
        stripped = strip_ansi(text)
        style = self._config.box_style
        out.new_line()
        out.write(style('┌' + ('─' * (len(stripped) + 2)) + '┐') +
           '\n' + style('│ ')        + text +        style(' │') +
           '\n' + style('└' + ('─' * (len(stripped) + 2)) + '┘'))

    def _timestamp(self):
        return ''.join([
            self._config.timestamp_bracket_style('['),
            self._config.timestamp_style(datetime.now().strftime(self._config.timestamp_format)),
            self._config.timestamp_bracket_style(']')
        ])

    def line(self, text):
        return self._timestamp() + ' ' + self._substeps.str() + text

    def msg(self, text):
        self._dotter.reset()
        self._eta.reset()
        out.new_line()
        out.write(self.line(text))

    def eta(self, text, seconds):
        self._dotter.reset()
        self._eta.reset()
        out.new_line()
        self._eta.start(self.line(text), seconds)

    def substeps(self, n):
        self._substeps.start(n)

    def progress_dot_every_n_seconds(self, n):
        self._dotter.start(n)

    def done(self):
        self._substeps.reset()
        self._dotter.reset()
        self._eta.reset()
        out.new_line()


writer = TerminalWriter()
