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
      "per-universe": []
    }

    self.dispatcher = Dispatcher()
    self.dispatcher.map("/*/dmx/*", self.dmx_handler)

  def dmx_handler(self, address, *args):
    """
    The OSC Handler for the DMX Messages

    This shouldn't be called by anything other than the Dispatcher
    """
    matches = search(r"^\/([0-9]+)\/dmx\/([0-9]+)", address) # /0/dmx/0 -> /<universe>/dmx/<addr>
    universe,address = int(matches[1]),int(matches[2])
    for fixture in self.list_fixtures(universe):
      if address in fixture: return fixture(address, *args)

  def add_fixture(self, fixture):
    """
    Adds a new Fixture to the fixture list

    :param fixture: The Fixture to add
    :type fixture: Fixture
    """
    if not(isinstance(fixture, Fixture)): raise Exception("Not a fixture!")
    self.fixtures["all"].append(fixture)
    if not(fixture.universe in self.fixtures["per-universe"]):
      if fixture.universe > 10: raise Exception("Sorry but WHY do you need 10 universes?")
      while len(self.fixtures["per-universe"]) <= fixture.universe:
        self.fixtures["per-universe"].append([])
    self.fixtures["per-universe"][fixture.universe].append(fixture)

  def add_fixtures(self, *fixtures):
    """
    Adds multiple Fixtures to the fixture list

    :param fixtures: The Fixtures to add
    :type fixtures: Fixture[]
    """
    for fixture in fixtures: self.add_fixture(fixture)

  def new_fixture(self, universe, starting_addr, channels):
    """
    Allows you to create a new fixture using a function decorator

    :param universe: The universe for this Fixture
    :type universe: int
    :param starting_addr: The starting address for this Fixture
    :type starting_addr: int
    :param channels: The amount of channel that this Fixture should have
    :type channels: int


    Example
    ---------

    .. code-block:: python3

       @server.new_fixture(0, 0, 3)
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
    :type universe: int|False

    :returns: List of Fixtures
    :rtype: Fixture[]
    """
    if universe is False: return self.fixtures["all"]
    elif len(self.fixtures["per-universe"]) > universe: return self.fixtures["per-universe"][universe]
    else: return []

  def run(self, ip="0.0.0.0", port=9000):
    """
    Start the server run

    Should be called always AFTER all fixtures are added

    :param ip: The IP address to listen on
    :type ip: str
    :param port: The Port to listen on
    :type port: int
    """
    self.osc_server = osc_server.ThreadingOSCUDPServer((ip, port), self.dispatcher)
    print ("Serving on {}".format(self.osc_server.server_address))
    self.osc_server.serve_forever()

