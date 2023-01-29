import json

import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

import wbui.process

class StatusPage(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.grid = Gtk.Grid()
        self.grid.set_margin_top(8)
        self.grid.set_margin_start(8)
        self.grid.set_column_spacing(16)
        self.grid.set_row_spacing(8)
        self.grid.attach(Gtk.Label(label="シリアルナンバー"), 0, 0, 1, 1)
        self.grid.attach(Gtk.Label(label="カーネルバージョン"), 0, 1, 1, 1)
        self.grid.attach(Gtk.Label(label="IPアドレス"), 0, 2, 1, 1)
        self.grid.attach(Gtk.Label(label="CPU"), 0, 3, 1, 1)
        self.grid.attach(Gtk.Label(label="論理CPUコア数"), 0, 4, 1, 1)
        self.grid.attach(Gtk.Label(label="CPUクロック"), 0, 5, 1, 1)
        self.grid.attach(Gtk.Label(label="メモリ容量"), 0, 6, 1, 1)
        self.append(self.grid)
        self.kvm_warning = Gtk.Label()
        self.kvm_warning.set_margin_top(16)
        self.kvm_warning.set_margin_start(8)
        self.kvm_warning.set_markup("<span foreground='red'>このコンピュータは仮想化命令に対応していないため、仮想マシンの実行性能が極端に低くなります。\n仮想化命令を有効にするにはコンピュータのBIOS/UEFI設定を確認してください。</span>")
        self.kvm_warning.hide()
        self.append(self.kvm_warning)

        wbui.process.WbSimpleInvoke({"execute":"system-status"}, self.done_system_status)

    def system_status_fail(self):
        wbui.footer.get_instance().set_message("エラー:システム情報の取得に失敗しました")

    def done_system_status(self, status, result, stderr):
        if status != 0:
            self.system_status_fail()
            return
        if "return" not in result:
            self.system_status_fail()
            return
        #else
        system_status = result["return"]
        serial_number = system_status["serial_number"]
        kernel_version = system_status["kernel_version"]
        ip_address = system_status["ip_address"] if "ip_address" in system_status else "不明"
        cpu_model = system_status["cpu_model"] if "cpu_model" in system_status else "不明"
        cpus = system_status["cpus"] if "cpus" in system_status else "不明"
        clock = "不明"
        if "clock" in system_status:
            clock = "%dMHz" % (system_status["clock"]["current"] / 1000)
            if "min" in system_status["clock"] and "max" in system_status["clock"]:
                min = system_status["clock"]["min"]
                max = system_status["clock"]["max"]
                if min > 0 and max > 0:
                    clock = "%d-%dMHz" % (min / 1000, max / 1000)
        memory = "不明"
        if "memory" in system_status:
            unused = system_status["memory"]["unused"]
            total = system_status["memory"]["total"]
            memory = "空き %dMB / 全体 %dMB" % (unused / 1024 / 1024, total / 1024 / 1024)

        self.grid.attach(Gtk.Label(label=serial_number,halign=Gtk.Align.START), 1, 0, 1, 1)
        self.grid.attach(Gtk.Label(label=kernel_version,halign=Gtk.Align.START), 1, 1, 1, 1)
        self.grid.attach(Gtk.Label(label=ip_address,halign=Gtk.Align.START), 1, 2, 1, 1)
        self.grid.attach(Gtk.Label(label=cpu_model,halign=Gtk.Align.START), 1, 3, 1, 1)
        self.grid.attach(Gtk.Label(label=cpus,halign=Gtk.Align.START), 1, 4, 1, 1)
        self.grid.attach(Gtk.Label(label=clock,halign=Gtk.Align.START), 1, 5, 1, 1)
        self.grid.attach(Gtk.Label(label=memory,halign=Gtk.Align.START), 1, 6, 1, 1)
        if not system_status["kvm"]: self.kvm_warning.show()
