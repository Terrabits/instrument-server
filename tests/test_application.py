from   ddt                              import ddt, data
from   instrument_server.application    import Application
from   instrument_server.errors         import OpenDeviceError
import unittest


# constants
NO_PLUGINS = []
NO_DEVICES = {}
TEST_DEVICE = {
    'instr': {
        'type':    'socket',
        'address': 'rsa23650'}}
MISSING_DEVICE = {
    'instr': {
        'type':    'socket',
        'address': 'unknown-hostname'}}


@ddt
class TestApplication(unittest.TestCase):
    def test_open_devices(self):
        app = Application(NO_PLUGINS, TEST_DEVICE)
        self.assertIn('instr', app.devices)
        app.close()

    def test_hostname_not_found(self):
        with self.assertRaises(OpenDeviceError):
            app = Application(NO_PLUGINS, MISSING_DEVICE)
            app.close()

    def test_error_queue(self):
        # init app
        app = Application(plugins=[], devices={})

        # query errors
        errors = app.execute(b'errors?')

        # should be no errors
        self.assertEqual(errors, '[]')

        # generate error
        app.execute(b'missing-command')
        errors = app.execute(b'errors?')
        self.assertTrue(len(errors) > 2)

        app.close()
