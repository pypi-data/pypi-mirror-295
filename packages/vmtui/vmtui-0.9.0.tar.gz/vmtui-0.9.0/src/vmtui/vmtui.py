#!/usr/bin/env python

"""
Chritian's VM Manager (VMTUI) 

A simple TUI to control (libvirt/QEMU) VMs.
"""

__author__    = "Christian Gruhl"
__license__   = ""
__copyright__ = "© 2024"
__version__   = "0.9.0"

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, ListView, ListItem, Label, DataTable, Input
from textual.containers import Horizontal, Vertical
from textual import work, on
from textual.message import Message
from textual.screen import Screen
from textual.validation import Length
from textual.css.query import NoMatches

import socket
import libvirt
import os
import xml.etree.ElementTree as ET
import configparser
import argparse
import importlib.resources as resources

class Domain:
    """ Wrapper around virDomain """

    States = {
        libvirt.VIR_DOMAIN_NOSTATE: "NO STATE",
        libvirt.VIR_DOMAIN_RUNNING: "running",
        libvirt.VIR_DOMAIN_BLOCKED: "blocked",
        libvirt.VIR_DOMAIN_PAUSED: "paused",
        libvirt.VIR_DOMAIN_SHUTDOWN: "shut down",
        libvirt.VIR_DOMAIN_SHUTOFF: "shut off",
        libvirt.VIR_DOMAIN_CRASHED: "crashed",
        libvirt.VIR_DOMAIN_PMSUSPENDED: "suspended"
    }
    
    def __init__(self, virDomain):
        self.virDomain = virDomain

    def name(self):
        return self.virDomain.name()

    def _read_xml(self):
        """ Update internal XML representation of the domain. """
        self.xmldesc = ET.fromstring(self.virDomain.XMLDesc())
        return self.xmldesc

    def _get_cdrom(self):
        for e in self.xmldesc.findall("devices/disk"):
            if e.get("device") == "cdrom":
                return e
        return None

    def net_interfaces(self):
        """ Read interface information from XML. """
        nics = self.xmldesc.findall("devices/interface")
        nicEntries = []
        for i,interface in enumerate(nics):
            mac = interface.find("mac").get("address")
            bridge = interface.find("source").get("bridge")

            nicEntries.append([f"net{i}", bridge, mac])
        return nicEntries

    ##########################################################################
    #                                                                        #
    #                     Domain Status Properties                           #
    #                                                                        #
    ##########################################################################
    @property
    def ID(self):
        did = self.virDomain.ID()
        did = "-" if did == -1 else did
        return did

    @property
    def state(self):
        s,_ = self.virDomain.state()
        return Domain.States[s]

    @property
    def cdrom_iso(self):
        iso_filename = '-'
        cdrom = self._get_cdrom()
        if cdrom is not None:
            iso_src = cdrom.find("source")
            if iso_src is not None:
                iso_file = iso_src.get("file")
                if iso_file is not None:
                    iso_filename = os.path.basename(iso_file)
        return iso_filename

    @property
    def graphics_remote_port(self):
        graphics = self.xmldesc.find('devices/graphics')
        graphics_port = '-'
        if graphics is not None:
            graphics_port = graphics.get('port')
        return graphics_port

    @property
    def autostart(self):
        return "yes" if self.virDomain.autostart() else "no"

    def status(self):
        """ Return status information about this domain. """
        self._read_xml()

        statusEntries = []
        statusEntries.append(["Name", self.name()])
        statusEntries.append(["ID", self.ID])
        statusEntries.append(["State", self.state])
        statusEntries.append(["Autostart", self.autostart])
        statusEntries.append(["ISO", self.cdrom_iso])
        statusEntries.append(["Graphics Port", self.graphics_remote_port])
        statusEntries += self.net_interfaces()

        return statusEntries
    ##########################################################################
    #                                                                        #
    #                  Domain Modification Methods                           #
    #                                                                        #
    ##########################################################################
    @cdrom_iso.setter
    def cdrom_iso(self, iso_path: str):
        """ Select ISO file to boot from. This requires that the domain has a cdrom drive attached.
        
        It will modify its source entry:

            DISK Entry:
            ------------
           <disk type="file" device="cdrom">
              <source file=$iso_path/>
           </disk>

        Parameters
        ----------
        iso_path : str
            Path to iso file to use
        
        """
        self._read_xml()
        cdrom = self._get_cdrom()
        if cdrom is not None:
            cd_src = cdrom.find("source")
            if cd_src is None:
                cd_src = ET.SubElement(cdrom, "source")
            cd_src.set("file", iso_path)

            updated_config = ET.tostring(cdrom).decode("utf-8")
            if self.virDomain.state()[0] != libvirt.VIR_DOMAIN_SHUTOFF:
                self.virDomain.updateDeviceFlags(updated_config, libvirt.VIR_DOMAIN_DEVICE_MODIFY_LIVE)
            self.virDomain.updateDeviceFlags(updated_config, libvirt.VIR_DOMAIN_DEVICE_MODIFY_CONFIG)
        else:
            raise Exception("No CD-ROM available!") 
        

    def set_graphics_password(self, password: str):
        """ Modify the password used to authenticate VNC/SPICE connections.
        
        The password is modified by changing the domain's XML description:

            GRAPHICS Entry:
            ---------------
            <graphics type="spice" port="5900" autoport="yes" listen="127.0.0.1" passwd="$password">

        Parameters
        ----------
        password : str
            New password

        """
        self._read_xml()
        graphics = self.xmldesc.find('devices/graphics')
        if graphics is not None:                                
            graphics.set("passwd", password)

        if self.virDomain.state()[0] != libvirt.VIR_DOMAIN_SHUTOFF:
            self._update_xml(graphics, live=True)

    def _update_xml(self, e, live=False):
        """ Write changes to Domain xml configuration.

        Parameters
        ----------
        e : xml_str
            Modified element
        live : bool
            Indicate if the running configuration should be changed as well.

        """
        self.virDomain.updateDeviceFlags(ET.tostring(e).decode("utf-8"), libvirt.VIR_DOMAIN_DEVICE_MODIFY_CONFIG)
        if live:
            self.virDomain.updateDeviceFlags(ET.tostring(e).decode("utf-8"), libvirt.VIR_DOMAIN_DEVICE_MODIFY_LIVE)
    
    ##########################################################################
    #                                                                        #
    #                     Domain Control Methods                             #
    #                                                                        #
    ##########################################################################
    def reset(self):
        self.virDomain.reset()

    def shutdown(self):
        self.virDomain.shutdown()

    def power(self):
        """ Based on the domains state the VM is either `created` or `destroyed`. """
        if self.virDomain.state()[0] == libvirt.VIR_DOMAIN_SHUTOFF:
            self.virDomain.create()
        else:
            self.virDomain.destroy()

    def boot_iso(self):
        """ Restarts the domain and boots the given iso image (if any).

        This is done by altering the domain's xmls configuration. 

        1. Modify the boot order of all disks by setting the cdrom's order to 1 
        2. Stop VM if running
        3. Start VM with modified boot order to boot image
        4. Revert changes (i.e. remove cdrom from boot order)

        **Note**: based on the machine's configuration this method may fail (depending on the boot settings).

        After a restart the VM will still boot the cdrom image - you have to power cycle the domain (i.e. call power()).
        
        """
        self._read_xml()
        
        cdrom = self._get_cdrom()
        if cdrom is None:
            return
        
        cd_boot = cdrom.find("boot")
        if cd_boot is None:
            cd_boot = ET.SubElement(cdrom, 'boot')
        cd_idx = int(cd_boot.get("order", 64))
        cdrom.remove(cd_boot)
        self._update_xml(cdrom)

        for disk in self.xmldesc.findall("devices/disk"):
            dboot = disk.find("boot")
            if dboot is not None:
                try:
                    d_idx = int(dboot.get("order"))
                    if d_idx < cd_idx:
                        dboot.set("order", str(d_idx+1))
                        self._update_xml(disk)
                except Exception as e:
                    self.log("ERROR in iso booting")
                    raise e
        
        cd_boot = ET.SubElement(cdrom, 'boot')
        cd_boot.set("order", "1")
        self._update_xml(cdrom)

        if self.virDomain.state()[0] != libvirt.VIR_DOMAIN_SHUTOFF:
            self.virDomain.destroy()
        
        self.virDomain.create()

        cdrom.remove(cd_boot)
        self._update_xml(cdrom)
        for disk in self.xmldesc.findall("devices/disk"):
            dboot = disk.find("boot")
            if dboot is not None:
                try:
                    d_idx = int(dboot.get("order"))
                    if d_idx <= cd_idx:
                        dboot.set("order", str(d_idx-1))
                        self._update_xml(disk)
                except Exception as e:
                    self.log("ERROR in iso booting")
                    raise e

class HyperVisor:

    def __init__(self):
        self.conn = libvirt.open("qemu:///system")
        self.domains = []        

    def refresh_domains(self):
        """ Read existing domains and create Wrappers. """
        self.domains = [Domain(virDom) for virDom in self.conn.listAllDomains()]

class VMList(Static):
    """ Display available VMs """

    BORDER_TITLE = "Virtual Machines"

    def __init__(self, **args):
        self.dom_mapper = {}
        super().__init__(**args)

    class Selected(Message):
        def __init__(self, domain, should_focus=False):
            self.domain = domain
            self.should_focus = should_focus
            super().__init__()
    class VMItem(ListItem):

        def __init__(self, domain):
            self.domain = domain
            super().__init__()

        def compose(self) -> ComposeResult:
            yield Label(self.domain.name())

    def compose(self) -> ComposeResult:
        self.vm_list = ListView()
        yield self.vm_list

    def on_list_view_selected( self, event: ListView.Selected ) -> None: 
        self.log("SELECTED")
        if event.item is not None:
            self.log("POSTING")
            self.post_message(self.Selected(event.item.domain, should_focus=True))
        

    def on_list_view_highlighted(self, event ) -> None:        
        if event.item is not None:
            self.log(event.item.domain)
            self.post_message(self.Selected(event.item.domain))

    def update_domains(self, domains):
        self.vm_list.clear()
        
        for dom in domains:                        
            self.vm_list.append(self.VMItem(dom))

class VMActions(Static):
    """ Display available actions """

    BORDER_TITLE = "Actions"
    BORDER_SUBTITLE = "modify your virtual machine"

    class VMAction(ListItem):
        def __init__(self, action, label):
            self.action = action
            self.label = label
            super().__init__()

        def compose(self) -> ComposeResult:
            yield Label(self.label)

    class Execute(Message):
        def __init__(self, action):
            self.action = action
            super().__init__()

    def compose(self) -> ComposeResult:
        yield ListView(*[self.VMAction(a,l) for a,l in [("reset", "Reset"),
                                                    ("power", "Power Off/On"),
                                                    ("shutdown", "Shutdown"),
                                                    ("console", "Console"),
                                                    ("iso", "Select ISO"),
                                                    ("boot", "Boot ISO"),
                                                    ("vnc", "Set VNC Passwort")]])

    def on_list_view_selected(self, event: ListView.Selected):
        self.post_message(self.Execute(event.item))

    def set_domain(self):        
        # TODO user reactive element here? self.app.domain?
        for child in self.children:
            child.disabled = self.app.domain is None

class VMStatus(Static):
    """ Display a table with status information about the selected domain. """

    BORDER_TITLE = "Status"
    BORDER_SUBTITLE = "$VMNAME"

    def compose(self) -> ComposeResult:
        yield DataTable()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("Property", "Value", "Extra")
        table.cursor_type = "none"

    def refresh_table(self):
        table = self.query_one(DataTable)
        table.clear()

        if self.app.domain is not None:
            self.border_subtitle = self.app.domain.name()
            table.add_rows(self.app.domain.status())
                
class PasswordInput(Screen):
    """ This Screen is used to update the graphics password of a domain. """
    BINDINGS = [("escape", "app.pop_screen", "Cancel Password")]
    MINLENGTH=6

    class NewPassword(Message):

        def __init__(self, new_password):
            self.new_password = new_password
            super().__init__()

    def compose(self) -> ComposeResult:
        # TODO: make password policy configurable in vmtui.ini?
        yield Input(placeholder="New Password", validators=[Length(PasswordInput.MINLENGTH)], max_length=32, id="pwbox")
        yield Footer()

    @on(Input.Submitted)
    def post_password(self, event : Input.Submitted):
        inputField = self.query_one(Input)
        if event.validation_result.is_valid:
            inputField.clear()
            self.post_message(self.NewPassword(event.value))
            self.app.pop_screen()
        else:
            self.notify("Invalid Password!", severity='warning')

class ISOSelection(Screen):
    """ This Screen provides a selection interface for ISO images. 
    
    The directory is configured using the config.ini file. It reads the

        [storage]
        ISOPath=$iso_path

    entry.
    """

    BINDINGS = [("escape", "app.pop_screen", "Cancel Selection")]

    EMPTY_DRIVE = "EMPTY DRIVE"

    def compose(self) -> ComposeResult:
        yield Label("Select one of the available images:")
        yield DataTable(id="isolist", cursor_type="row")
        yield Footer()

    def on_mount(self):
        dt = self.query_one(DataTable)
        dt.add_columns("Name")

        dt.add_row(ISOSelection.EMPTY_DRIVE)

        try:
            for img in self.read_images():
                dt.add_row(img)
        except Exception as e:
            self.notify("Could not read ISO directory. Missing config.ini?", severity="error")
    class ISOSelected(Message):

        def __init__(self, iso):
            self.iso = iso
            super().__init__()

    @on(DataTable.RowSelected)
    def select_iso(self, event: DataTable.RowSelected):
        try:
            iso_file = event.control.get_row(event.row_key)[0]
            if iso_file == self.EMPTY_DRIVE:
                iso_path = ""
            else:
                iso_path = os.path.join(self.app.config['storage']['ISOPath'], iso_file)
            self.post_message(self.ISOSelected(iso_path))
        except Exception as e:
            self.notify("Could not select ISO. %s" % str(e), severity="error")
        finally:
            self.app.pop_screen()

    def read_images(self):
        isopath = self.app.config['storage']['ISOPath']
        if isopath is None:
            return []
        
        else:
            return [ iso for iso in os.listdir(isopath) if iso.lower().endswith(".iso")]

class VMTUI(App):
    """ TUI to control basic VM functionality for libvirt/QEMU VMs."""

    BINDINGS = [("q", "disconnect", "Disconnect"), ("r", "refresh", "Refresh")]
    with resources.path('vmtui.static', 'vmtui.css') as css_path:
        CSS_PATH = str(css_path)

    def __init__(self, config):
        self.domain = None
        self.config = config
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        with Horizontal():
            yield VMList(id="vmlist")
            with Vertical():
                yield VMActions(id="vmactions")
                yield VMStatus(id="vmstatus")

    @work(exclusive=True)
    async def update_vmlist(self) -> None:
        """ Connect to Hypervisor (i.e. qemu), read domains and update the VMList. """
        self.log("updating ...")
        vmlist = self.query_one("#vmlist")
        
        try:
            self.hv = HyperVisor()
            self.hv.refresh_domains()
        except:
            self.notify("Could not connect to hypervisor!", severity="error")
            return

        vmlist.update_domains(self.hv.domains)
            
    def on_mount(self):
        self.title = "Christian's VM Manager"
        self.sub_title = "running on %s as %s" % (socket.gethostname(), os.getlogin())

        self.update_vmlist()

        self.install_screen(PasswordInput(), name="pwin")
        self.install_screen(ISOSelection(), name="iso")

    def action_disconnect(self) -> None:
        self.exit()

    def action_refresh(self) -> None:
        self.update_vmlist()

    def open_console(self) -> None:
        """ Connect to a running domain.
        
        This suspends the textual app and opens the serial console using `virsh`.
        The VM must be configured to use `ttyS0`, otherwise a blank screen is displayed.
         """
        with self.suspend():
            os.system("virsh -c qemu:///system console %s" % self.domain.name())

    @on(VMList.Selected)
    def update_domain_selection(self, message: VMList.Selected):
        self.domain = message.domain
        self.refresh_views()        

    def refresh_views(self):
        try:
            vmstatus = self.query_one("#vmstatus")
            vmstatus.refresh_table()
            vmactions = self.query_one("#vmactions")
            vmactions.set_domain()
        except NoMatches:
            pass
    
    @on(VMActions.Execute)
    def execute_vmaction(self, message):
        """ Dispatcher for domain actions."""

        if self.domain is not None:
            dom = self.domain
            try:
                {
                    "reset": dom.reset,
                    "console": self.open_console,
                    "power": dom.power,
                    "shutdown": dom.shutdown,
                    "vnc": lambda : self.push_screen("pwin"), # open password screen: PasswordInput
                    "iso": lambda : self.push_screen("iso"),  # open image selection sreen: ISOSelection
                    "boot": dom.boot_iso,
                }.get(message.action.action, lambda: True)()
            except Exception as e:
                self.notify(str(e), severity="error")
            
            self.refresh_views()

    @on(PasswordInput.NewPassword)
    def set_password(self, message : PasswordInput.NewPassword):
        self.log(message.new_password)

        if self.domain is not None:
            try:
                self.domain.set_graphics_password(message.new_password)
            except libvirt.libvirtError as e:
                self.notify(str(e), severity="error")

    @on(ISOSelection.ISOSelected)
    def set_iso(self, message: ISOSelection.ISOSelected):
        if self.domain is not None:
            try:
                self.domain.cdrom_iso = message.iso
            except Exception or libvirt.libvirtError as e:
                self.notify(str(e), severity="error")
            self.refresh_views()

def arguments():
    parser = argparse.ArgumentParser(description="vmtui")
    parser.add_argument('-c', '--config', type=str, default="vmtui.ini", help="Path to the configuration file")
    return parser.parse_args()

def main():

    args = arguments()

    config = configparser.ConfigParser()
    config.read(args.config)

    app = VMTUI(config)
    app.run()

if __name__ == "__main__":
    main()
