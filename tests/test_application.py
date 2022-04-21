from   ddt                              import ddt, data
from   instrument_server.application    import Application
from   instrument_server.errors         import OpenDeviceError
import unittest


@ddt
class TestApplication(unittest.TestCase):
    def test_basic_application(self):
        plugins = []
        devices = {
            'instr': {
                'type':    'socket',
                'address': 'rsa23650' }}

        # start
        with Application(plugins, devices) as app:
            self.assertTrue('instr' in app.devices)
            with self.assertRaises(SystemExit):
                app.execute(b'quit\n')

    def test_hostname_not_found(self):
        plugins = [
            'instrument_server.devices.socket_factory',
            'instrument_server.commands.quit_command' ]

        devices = {
            'instr': {
                'type':    'socket',
                'address': 'missing-instr' }}

        # start
        with self.assertRaises(Exception):
            app = Application(plugins, devices)

    def test_error_queue(self):
        # init app
        plugins = []
        devices = {}
        with Application(plugins, devices) as app:
            # query errors
            errors = app.execute(b'errors?')

            # should be no errors
            self.assertEqual(errors, '[]')

            # generate error
            app.execute(b'missing-command')
            errors = app.execute(b'errors?')
            self.assertTrue(len(errors) > 2)
