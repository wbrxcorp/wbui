import os,signal,json

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("GLib", "2.0")
from gi.repository import Gtk,GLib

class WbStreamInvoke:
    def __init__(self, parent, message, cmd, done_func):
        self.dlg = Gtk.MessageDialog(buttons = Gtk.ButtonsType.CANCEL, modal = True, text = message, transient_for=parent)
        content_area = self.dlg.get_content_area()
        self.progress_bar = Gtk.ProgressBar()
        self.progress_bar.set_margin_start(16)
        self.progress_bar.set_margin_end(16)
        self.progress_bar.set_size_request(500, -1)
        content_area.append(self.progress_bar)
        self.dlg.connect('response', self.on_response)
        self.pid, stdin_fd, stdout_fd, stderr_fd = GLib.spawn_async(["wb","invoke"], flags=GLib.SpawnFlags.SEARCH_PATH | GLib.SpawnFlags.DO_NOT_REAP_CHILD,
            standard_input=True,standard_output=True, standard_error=True)

        os.write(stdin_fd, cmd.encode() if type(cmd) is str else json.dumps(cmd).encode())
        os.close(stdin_fd)

        self.stdout = ""
        self.stderr = ""
        self.done_func = done_func
        io_flags = GLib.IO_IN | GLib.IO_ERR | GLib.IO_HUP | GLib.IO_NVAL
        self.stdout_watch = GLib.io_add_watch(stdout_fd, io_flags, self.on_stdout)
        self.stderr_watch = GLib.io_add_watch(stderr_fd, io_flags, self.on_stderr)
        GLib.child_watch_add(self.pid, self.on_process_exit)
        self.dlg.show()

    def on_process_exit(self, pid, status):
        GLib.source_remove(self.stdout_watch)
        GLib.source_remove(self.stderr_watch)
        GLib.spawn_close_pid(pid)
        self.dlg.destroy()
        self.done_func(status, self.stderr)

    def on_stdout(self, fd, condition):
        buf = os.read(fd, 4096)
        self.stdout += buf.decode()
        while '\n' in self.stdout:
            [line, remains] = self.stdout.split('\n', 1)
            self.stdout = remains
            if line.startswith("MESSAGE:"): 
                self.progress_bar.set_show_text(True)
                self.progress_bar.set_text(line[8:])
            elif line.startswith("PROGRESS:"): self.progress_bar.set_fraction(float(line[9:]))

        return True

    def on_stderr(self, fd, condition):
        buf = os.read(fd, 4096)
        self.stderr += buf.decode()
        return True

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
        self.stdout_watch = GLib.io_add_watch(stdout_fd, io_flags, self.on_stdout)
        self.stderr_watch = GLib.io_add_watch(stderr_fd, io_flags, self.on_stderr)
        GLib.child_watch_add(self.pid, self.on_process_exit)

    def on_process_exit(self, pid, status):
        GLib.source_remove(self.stdout_watch)
        GLib.source_remove(self.stderr_watch)
        GLib.spawn_close_pid(pid)
        try:
            result = json.loads(self.stdout)
        except:
            result = {}
        self.done_func(status, result, self.stderr)

    def on_stdout(self, fd, condition):
        buf = os.read(fd, 4096)
        self.stdout += buf.decode()
        return True

    def on_stderr(self, fd, condition):
        buf = os.read(fd, 4096)
        self.stderr += buf.decode()
        return True
