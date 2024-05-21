import dbus
from DBus import systemBus


def getManagedObjects():
    rootBTObj = systemBus.get_object('org.bluez', '/')
    return rootBTObj.GetManagedObjects(dbus_interface='org.freedesktop.DBus.ObjectManager')


def _dictToFilterFunc(filterDict):
    return lambda obj: all(obj[k] == v for k, v in filterDict.items())


def findObject(wellKnownName, pathFilter=None, interfacesFilter=None):
    if pathFilter is None:
        pathFilter = lambda path: True
    if not callable(pathFilter):
        raise Exception('Invalid path filter passed!')

    if interfacesFilter is None:
        interfacesFilter = lambda interfaces: True
    if not callable(interfacesFilter):
        raise Exception('Invalid interfaces filter passed!')

    managedObjects = getManagedObjects()

    for path, interfaces in managedObjects.items():
        if pathFilter(path) and interfacesFilter(interfaces):
            return systemBus.get_object(wellKnownName, path)


def findObjectInterface(wellKnownName, interfaceName, interfaceFilter=None, pathFilter=None):
    if interfaceFilter is None:
        interfaceFilter = lambda interface: True
    if isinstance(interfaceFilter, dict):
        iFDict = interfaceFilter
        interfaceFilter = lambda interface: all(interface[k] == v for k, v in iFDict.items())
    if not callable(interfaceFilter):
        raise Exception('Invalid interface filter passed!')

    def interfacesFilter(interfaces):
        interface = interfaces.get(interfaceName)
        if interface is None:
            return False
        return interfaceFilter(interface)

    obj = findObject(wellKnownName, pathFilter, interfacesFilter)
    return dbus.Interface(obj, interfaceName)


def findBluetoothDevice(address):
    return findObjectInterface('org.bluez', 'org.bluez.Device1', { 'Address': address })
