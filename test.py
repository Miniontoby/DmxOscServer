#!/usr/bin/env python3
import unittest

from DmxOscServer import *
from pythonosc.osc_message_builder import OscMessageBuilder

def _(fix, address, *args): return

class TestDmxOscServer(unittest.TestCase):
    def test_fixture_string(self):
        """
        Test the Fixture.__str__()
        """
        fixture1 = Fixture(0, 1, 2, _)
        self.assertEqual(fixture1.__str__(), "Fixture(universe=0, starting_addr=1, channels=2, values=[0, 0])")

        fixture2 = Fixture(universe=1, starting_addr=3, channels=2, handler=_)
        self.assertEqual(fixture2.__str__(), "Fixture(universe=1, starting_addr=3, channels=2, values=[0, 0])")

    def test_fixture_call(self):
        """
        Test the Fixture.__call__()
        """
        fixture = Fixture(universe=0, starting_addr=1, channels=2, handler=_)
        fixture(1, 0.1) # Call at address 1 which is the first channel
        fixture(2, 0.6) # Call at address 2
        self.assertEqual(fixture.values, [0.1, 0.6])

    def test_server_define_fixture(self):
        """
        Test the @server.define_fixture()
        """
        server = DmxOscServer()

        @server.define_fixture(0, 1, 2)
        def handle(): return

        @server.define_fixture(universe=0, starting_addr=3, channels=2)
        def handle(): return

        self.assertEqual(server.list_fixtures()[0].__str__(), "Fixture(universe=0, starting_addr=1, channels=2, values=[0, 0])")
        self.assertEqual(server.list_fixtures()[1].__str__(), "Fixture(universe=0, starting_addr=3, channels=2, values=[0, 0])")
    def test_server_add_fixture(self):
        """
        Test the server.add_fixture()
        """
        fix = Fixture(0, 1, 2, _)

        server = DmxOscServer()
        server.add_fixture(fix)

        self.assertEqual(server.list_fixtures()[0], fix)
    def test_server_add_fixtures(self):
        """
        Test the server.add_fixtures()
        """
        fix1 = Fixture(0, 1, 2, _)
        fix2 = Fixture(0, 3, 4, _)

        server = DmxOscServer()
        server.add_fixtures(fix1, fix2)

        self.assertEqual(server.list_fixtures(), [fix1, fix2])
    def test_server_list_fixtures(self):
        """
        Test the server.list_fixtures()
        """
        fix1 = Fixture(0, 1, 2, _)
        fix2 = Fixture(0, 3, 4, _)
        fix3 = Fixture(1, 1, 2, _)
        fix4 = Fixture(2, 3, 4, _)

        server = DmxOscServer()
        server.add_fixtures(fix1, fix2, fix3, fix4)

        self.assertEqual(server.list_fixtures(), [fix1, fix2, fix3, fix4])
        self.assertEqual(server.list_fixtures(0), [fix1, fix2])
        self.assertEqual(server.list_fixtures(1), [fix3])
        self.assertEqual(server.list_fixtures(2), [fix4])
    def test_server_raises_fixtures(self):
        """
        Test the exceptions of server.add_fixtures()
        """
        class obj:
            def __init__(self, uni, st, ch, hd):
                self.universe=uni
                self.starting_addr=st
                self.channels=ch
                self.handler=hd
        notfix = obj(0, 1, 3, _)
        fix1 = Fixture(0, 1, 3, _)
        fix2 = Fixture(1, 1, 4, _)
        fix3 = Fixture(0, 2, 4, _)

        server = DmxOscServer()

        # Test non-fixture
        with self.assertRaises(TypeError) as context: server.add_fixture(notfix)
        self.assertTrue('Not a Fixture!' in str(context.exception))

        # Test duplicates
        server.add_fixture(fix1)
        server.add_fixture(fix2) # check if universes don't matter by adding to universe 1
        with self.assertRaises(ValueError) as context: server.add_fixture(fix3)
        self.assertTrue('There is already a Fixture within that address!' in str(context.exception))

        # Test call with out of range
        with self.assertRaises(ValueError) as context: fix1(5, 0.5) # address 5 is out of the range
        self.assertTrue('Address 5 is not within the address range!' in str(context.exception))

        # Test read-only properties
        for prop in ["universe","starting_addr","channels","end_addr","address_range","values"]:
            with self.assertRaises(AttributeError) as context: fix1.__setattr__(prop, 1)
            self.assertTrue("Can't modify {}".format(prop) in str(context.exception))
    def test_server_dispatcher(self):
        """
        Test the dmx_handler using the OSC Dispatcher to make sure the code works
        """
        server = DmxOscServer()

        @server.define_fixture(0, 1, 2)
        def handler(fix, addr, *args): self.assertEqual(fix.__str__(), "Fixture(universe=0, starting_addr=1, channels=2, values=[0.5, 0])")

        msg = OscMessageBuilder("/0/dmx/1")
        msg.add_arg(0.5)

        for handler in server._dispatcher.handlers_for_address("/0/dmx/1"): handler.invoke("", msg.build())

if __name__ == '__main__':
    unittest.main()
