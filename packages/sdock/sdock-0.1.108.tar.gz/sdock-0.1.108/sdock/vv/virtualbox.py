import datetime
import os,sys,mystring
from . import Provider

class app(Provider):
	def __init__(self):
		super().__init__()
		self.name = None

	@property
	def raw_name(self):
		return "virtualbox"

	def exe_name(self):
		return "VBoxManage"

	def install(self):
		return

	def uninstall(self):
		return

	def vagrant_string(self, timeoffset=None):
		offset_strings = []
		if timeoffset:
			offset_strings = [
				"""vb.customize ["setextradata", :id, "VBoxInternal/Devices/VMMDev/0/Config/GetHostTimeDisabled", 1]""",
				"""vb.customize [ "modifyvm", :id, "--biossystemtimeoffset","{0}" ] """.format(str(str(timeoffset).split(".")[0]))
			]
		return """
win10.vm.provider :virtualbox do |vb|
	vb.name = "{0}"
	vb.gui = true
	{1}
end
""".format(self.name,"\n	".join(offset_strings))

	def on(self):
		self.exe("startvm {0}".format(self.name))

	def off(self):
		#self.exe("controlvm {0} acpipowerbutton".format(self.name))
		self.exe("controlvm {0} poweroff".format(self.name))

	def delete(self):
		self.exe("unregistervm --delete {0}".format(self.name))

	def disable_timesync(self):
		self.exe("setextradata {0} VBoxInternal/Devices/VMMDev/0/Config/GetHostTimeDisabled 1".format(self.name))

	def set_date(self, datetime_value:datetime.datetime=None):
		self.exe("modifyvm {0} --biossystemtimeoffset {1}".format(self.name, 
			str((datetime_value - datetime.datetime.now()).total_seconds())
		))
	
	def set_offset(self, value):
		self.exe("modifyvm {0} --biossystemtimeoffset {1}".format(
			self.name, 
			str(str(value).split(".")[0])
		))

	def disable_network(self):
		self.exe("modifyvm {0} --nic1 null".format(self.name))
		self.exe("modifyvm {0} --cableconnected1 off".format(self.name))


	"""
name=tempbox
vag=sudo vagrant
vb=sudo VBoxManage
breather=10

default:: cycle

install: #https://developer.hashicorp.com/vagrant/downloads
	#-wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
	#-echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com jammy main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
	-sudo apt update
	-sudo apt install vagrant


uninstall: #https://developer.hashicorp.com/vagrant/docs/installation/uninstallation
	-rm -rf /opt/vagrant
	-rm -f /usr/bin/vagrant

cycle: proc #down up

proc: down
	$(vag) up
	
	$(vb) controlvm $(name) poweroff #acpipowerbutton
	#$(vag) halt
	sleep $(breather)
	
	@make disable

	#$(vag) up
	$(vb) startvm $(name)

disable:
	$(vb) modifyvm $(name) --biossystemtimeoffset -31536000000
	$(vb) setextradata $(name) VBoxInternal/Devices/VMMDev/0/Config/GetHostTimeDisabled 1
	#$(vb) modifyvm $(name) --nic1 null
	$(vb) modifyvm $(name) --cableconnected1 off

rup:
	$(vag) resume 
up:
	$(vag) up

full: up
	$(vag) halt

down:
	-$(vag) destroy -f
cache:
	$(vag) global-status --prune

delete:
	VBoxManage unregistervm --delete "$$name"
	"""