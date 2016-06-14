import gi

gi.require_version('Peas', '1.0')
from gi.repository import GObject, Peas


class ExampleAppActivatable(GObject.Object, Peas.Activatable):
    __gtype_name__ = 'PythonHelloPlugin'
    object = GObject.Property(type=GObject.Object)
    data = GObject.Property(type=GObject.Object)

    def do_activate(self):
        print('some activate')
        print(self.data)

    def do_deactivate(self):
        print('some deactivate')

    def do_update_state(self):
        pass

    def get_data(self, data):
        print(data.value)


print('yo')
