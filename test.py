#!/usr/bin/env python3
import unittest

from DmxOscServer import *

def _(): return

class TestDmxOscServer(unittest.TestCase):
    def test_fixture_string(self):
        """
        Test the Fixture.__str__()
        """
        fixture = Fixture(0, 1, 2, _)
        self.assertEqual(fixture.__str__(), "Fixture(universe=0, starting_addr=1, channels=2, values=[0, 0])")
    def test_server_define_fixture(self):
        """
        Test the @server.define_fixture()
        """
        server = DmxOscServer()

        @server.define_fixture(0, 1, 2)
        def handle(): return

        self.assertEqual(server.list_fixtures()[0].__str__(), "Fixture(universe=0, starting_addr=1, channels=2, values=[0, 0])")
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

if __name__ == '__main__':
    unittest.main()
