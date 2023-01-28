import os,signal,json

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("GLib", "2.0")
from gi.repository import Gtk,GLib

class ProcessExecutionDialog(Gtk.MessageDialog):
    def __init__(self, parent, cmd, done_func):
        Gtk.MessageDialog.__init__(self, buttons = Gtk.ButtonsType.CLOSE, modal = True, text = "メッセージ", transient_for=parent)
        self.connect('response', self.on_response)
        self.pid, stdin_fd, stdout_fd, stderr_fd = GLib.spawn_async(cmd, flags=GLib.SpawnFlags.SEARCH_PATH | GLib.SpawnFlags.DO_NOT_REAP_CHILD,
            standard_input=True,standard_output=True, standard_error=True)
        GLib.child_watch_add(self.pid, self.on_process_exit)

        os.write(stdin_fd, '{"method":"list","params":{"sleep":5, "fail":true}}'.encode())

        self.stdout = ""
        self.stderr = ""
        self.done_func = done_func
        io_flags = GLib.IO_IN | GLib.IO_ERR | GLib.IO_HUP | GLib.IO_NVAL
        GLib.io_add_watch(stdout_fd, io_flags, self.on_stdout)
        GLib.io_add_watch(stderr_fd, io_flags, self.on_stderr)
        self.show()

    def on_process_exit(self, pid, status):
        print("process_exit", pid, status)
        self.destroy()
        self.done_func(status, self.stdout, self.stderr)

    def on_stdout(self, fd, condition):
        buf = os.read(fd, 4096)
        self.stdout += buf.decode()

    def on_stderr(self, fd, condition):
        buf = os.read(fd, 4096)
        self.stderr += buf.decode()

    def on_response(self, dialog, response):
        os.kill(self.pid, signal.SIGTERM)

class WbSimpleInvoke:
    def __init__(self, cmd, done_func):
        self.pid, stdin_fd, stdout_fd, stderr_fd = GLib.spawn_async(["wb", "invoke"],
            flags=GLib.SpawnFlags.SEARCH_PATH | GLib.SpawnFlags.DO_NOT_REAP_CHILD,
            standard_input=True,standard_output=True, standard_error=True)
        os.write(stdin_fd, cmd.encode() if type(cmd) is str else json.dumps(cmd).encode())
        os.close(stdin_fd)
        self.stdout = ""
        self.stderr = ""
        self.done_func = done_func
        io_flags = GLib.IO_IN | GLib.IO_ERR | GLib.IO_HUP | GLib.IO_NVAL
        GLib.io_add_watch(stdout_fd, io_flags, self.on_stdout)
        GLib.io_add_watch(stderr_fd, io_flags, self.on_stderr)
        GLib.child_watch_add(self.pid, self.on_process_exit)

    def on_process_exit(self, pid, status):
        GLib.spawn_close_pid(pid)
        self.done_func(status, self.stdout, self.stderr)

    def on_stdout(self, fd, condition):
        buf = os.read(fd, 4096)
        self.stdout += buf.decode()

    def on_stderr(self, fd, condition):
        buf = os.read(fd, 4096)
        self.stderr += buf.decode()
