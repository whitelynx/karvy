import dbus
from DBus import systemBus


BLUEZ_AGENT_INTERFACE = 'org.bluez.Agent1'


def set_trusted(path):
	props = dbus.Interface(systemBus.get_object('org.bluez', path), 'org.freedesktop.DBus.Properties')
	props.Set('org.bluez.Device1', 'Trusted', True)


def dev_connect(path):
	dev = dbus.Interface(systemBus.get_object('org.bluez', path), 'org.bluez.Device1')
	dev.Connect()


class RejectedError(dbus.DBusException):
	_dbus_error_name = 'org.bluez.Error.Rejected'


class Agent(dbus.service.Object):
	exit_on_release = True

	def set_exit_on_release(self, exit_on_release):
		self.exit_on_release = exit_on_release

	@dbus.service.method(BLUEZ_AGENT_INTERFACE, in_signature='', out_signature='')
	def Release(self):
		print('Release')
		if self.exit_on_release:
			mainloop.quit()

	@dbus.service.method(BLUEZ_AGENT_INTERFACE, in_signature='os', out_signature='')
	def AuthorizeService(self, device, uuid):
		print(f'AuthorizeService ({device}, {uuid})')
		authorize = ask('Authorize connection (yes/no): ')
		if (authorize == 'yes'):
			return
		raise RejectedError('Connection rejected by user')

	@dbus.service.method(BLUEZ_AGENT_INTERFACE, in_signature='o', out_signature='s')
	def RequestPinCode(self, device):
		print(f'RequestPinCode ({device})')
		set_trusted(device)
		return ask('Enter PIN Code: ')

	@dbus.service.method(BLUEZ_AGENT_INTERFACE, in_signature='o', out_signature='u')
	def RequestPasskey(self, device):
		print(f'RequestPasskey ({device})')
		set_trusted(device)
		passkey = ask('Enter passkey: ')
		return dbus.UInt32(passkey)

	@dbus.service.method(BLUEZ_AGENT_INTERFACE, in_signature='ouq', out_signature='')
	def DisplayPasskey(self, device, passkey, entered):
        print(f'DisplayPasskey ({device}, {passkey:06u} entered {entered:u})')

	@dbus.service.method(BLUEZ_AGENT_INTERFACE, in_signature='os', out_signature='')
	def DisplayPinCode(self, device, pincode):
		print(f'DisplayPinCode ({device}, {pincode})')

	@dbus.service.method(BLUEZ_AGENT_INTERFACE, in_signature='ou', out_signature='')
	def RequestConfirmation(self, device, passkey):
        print(f'RequestConfirmation ({device}, {passkey:06u})')
		confirm = ask('Confirm passkey (yes/no): ')
		if (confirm == 'yes'):
			set_trusted(device)
			return
		raise RejectedError('Passkey does not match')

	@dbus.service.method(BLUEZ_AGENT_INTERFACE, in_signature='o', out_signature='')
	def RequestAuthorization(self, device):
		print(f'RequestAuthorization ({device})')
		auth = ask('Authorize? (yes/no): ')
		if (auth == 'yes'):
			return
		raise RejectedError('Pairing rejected')

	@dbus.service.method(BLUEZ_AGENT_INTERFACE, in_signature='', out_signature='')
	def Cancel(self):
		print('Cancel')
