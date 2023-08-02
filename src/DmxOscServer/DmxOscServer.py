# Project libs
from .Fixture import Fixture

# Other libs
from re import search
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server

class DmxOscServer():
  """
  Instantiate a DMX OSC Server
  """
  def __init__(self):
    self.fixtures = {
      "all": [],
      "per-universe": {}
    }

    self.dispatcher = Dispatcher()
    self.dispatcher.map("/*/dmx/*", self.dmx_handler)

  def dmx_handler(self, address, *args):
    """
    The OSC Handler for the DMX Messages

    This shouldn't be called by anything other than the OSC Dispatcher
    """
    matches = search(r"^\/([0-9]+)\/dmx\/([0-9]+)", address) # /0/dmx/0 -> /<universe>/dmx/<addr>
    universe,address = int(matches[1]),int(matches[2])
    for fixture in self.list_fixtures(universe):
      if address in fixture: return fixture(address, *args)

  def add_fixture(self, fixture):
    """
    Adds a new Fixture to the fixture list

    :param Fixture fixture: The Fixture to add
    :raises TypeError: if the fixture is not a Fixture


    Example
    ---------

    .. code-block:: python3

       from DmxOscServer import DmxOscServer, Fixture

       server = DmxOscServer()

       def handler(fixture, address, *args): return

       fix = Fixture(0, 0, 3, handler)
       server.add_fixture(fix)
    """
    if not(isinstance(fixture, Fixture)): raise TypeError("Not a Fixture!")
    self.fixtures["all"].append(fixture)
    if not(fixture.universe in self.fixtures["per-universe"]): self.fixtures["per-universe"][fixture.universe] = []
    self.fixtures["per-universe"][fixture.universe].append(fixture)

  def add_fixtures(self, *fixtures):
    """
    Adds multiple Fixtures to the fixture list

    :param Fixture \*fixtures: The Fixtures to add


    Example
    ---------

    .. code-block:: python3

       from DmxOscServer import DmxOscServer, Fixture

       server = DmxOscServer()

       def handler(fixture, address, *args): return

       fix1 = Fixture(0, 0, 3, handler)
       fix2 = Fixture(0, 3, 3, handler)

       server.add_fixtures(fix1, fix2)
    """
    for fixture in fixtures: self.add_fixture(fixture)

  def define_fixture(self, universe, starting_addr, channels):
    """
    Allows you to define a new fixture using a function decorator

    :param int universe: The universe for this Fixture
    :param int starting_addr: The starting address for this Fixture
    :param int channels: The amount of channel that this Fixture should have


    Example
    ---------

    .. code-block:: python3

       from DmxOscServer import DmxOscServer, Fixture

       server = DmxOscServer()

       @server.define_fixture(0, 0, 3)
       def rgb_handler(fixture, address, *args):
           fixture.values[address] = args[0]
    """
    def decorator(func):
      result = Fixture(universe, starting_addr, channels, func)
      self.add_fixture(result)
      return result

    return decorator

  def list_fixtures(self, universe=False):
    """
    If `universe` is set to False, it will return all the Fixtures
    If `universe` is set to a universe number, it will return all the Fixtures of that universe

    :param universe: Specifies the universe. Set to False for all Fixtures
    :type universe: int or False

    :returns: List of Fixtures
    :rtype: Fixture[]


    Example
    ---------

    .. code-block:: python3

       from DmxOscServer import DmxOscServer

       server = DmxOscServer()

       # Add fixtures here

       all_fixtures = server.list_fixtures()
       universe_zero_fixtures = server.list_fixtures(0)
    """
    if universe is False: return self.fixtures["all"]
    elif universe in self.fixtures["per-universe"]: return self.fixtures["per-universe"][universe]
    else: return []

  def run(self, ip="0.0.0.0", port=9000):
    """
    Start the server run

    Should be called always AFTER all fixtures are added

    :param str ip: The IP address to listen on
    :param int port: The Port to listen on
    """
    self.osc_server = osc_server.ThreadingOSCUDPServer((ip, port), self.dispatcher)
    print ("Serving on {}".format(self.osc_server.server_address))
    self.osc_server.serve_forever()

