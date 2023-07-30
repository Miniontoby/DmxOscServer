# Project libs
from .Fixture import Fixture

# Other libs
from re import search
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server

class DmxOscServer():
  """
  Instantiate a DMX OSC Server

  :param ip: The IP address to listen on
  :type ip: str
  :param port: The Port to listen on
  :type port: int
  """
  def __init__(self, ip="0.0.0.0", port=9000):
    self.ip = ip
    self.port = port

    self.fixtures = []

    self.dispatcher = Dispatcher()
    self.dispatcher.map("/*/dmx/*", self.dmx_handler)
    self.osc_server = osc_server.ThreadingOSCUDPServer((ip, port), self.dispatcher)

  def dmx_handler(self, address, *args):
    """
    The OSC Handler for the DMX Messages

    This shouldn't be called by anything other than the Dispatcher
    """
    matches = search(r"^\/([0-9]+)\/dmx\/([0-9]+)", address) # /0/dmx/0 -> /<universe>/dmx/<addr>
    universe, address = int(matches[1]),int(matches[2])
    for fixture in self.fixtures:
      if fixture.universe == universe and address in range(fixture.starting_addr, fixture.end_addr):
        fixture.handler(fixture, address, *args)
        break

  def add_fixture(self, fixture):
    """
    Adds a new Fixture to the fixture list

    :param fixture: The Fixture to add
    :type fixture: Fixture
    """
    if not(isinstance(fixture, Fixture)): raise Exception("Not a fixture!")
    self.fixtures.append(fixture)

  def add_fixtures(self, *fixtures):
    """
    Adds multiple Fixtures to the fixture list

    :param fixtures: The Fixtures to add
    :type fixtures: Fixture[]
    """
    for fixture in fixtures: self.add_fixture(fixture)

  def run(self):
    """
    Start the server run

    Should be called always AFTER all fixtures are added
    """
    print("Serving on {}".format(self.osc_server.server_address))
    self.osc_server.serve_forever()

