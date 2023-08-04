# Project libs
from .Fixture import Fixture

# Other libs
from re import search
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer

class DmxOscServer():
  """
  Instantiate a DMX OSC Server
  """
  def __init__(self):
    # Init fixture list (should be private)
    self.__fixtures = {
      "all": [],
      "per-universe": {}
    }

    # Define OSC Message handler in init and private, so it cannot be called by anything else
    def __dmx_handler(address, *args):
      matches = search(r"^\/([0-9]+)\/dmx\/([0-9]+)", address) # /<universe>/dmx/<addr>
      universe,address = int(matches[1]),int(matches[2])
      for fixture in self.list_fixtures(universe):
        if address in fixture: return fixture(address, *args) # They have the __call__ set to their handler

    # Should be 'private/protected'
    self._dispatcher = Dispatcher()
    self._dispatcher.map("/*/dmx/*", __dmx_handler)

  def add_fixture(self, fixture):
    """
    Adds a new Fixture to the fixture list

    :param Fixture fixture: The Fixture to add
    :raises TypeError: If the fixture is not a Fixture
    :raises ValueError: If the address of the fixture is already used in the universe


    Example
    ---------

    .. code-block:: python3

       from DmxOscServer import DmxOscServer, Fixture

       server = DmxOscServer()

       def handler(fixture, address, *args): print(fixture.values)

       fix = Fixture(0, 0, 3, handler)
       server.add_fixture(fix)
    """
    if not(isinstance(fixture, Fixture)): raise TypeError("Not a Fixture!")

    if not(fixture.universe in self.__fixtures["per-universe"]): self.__fixtures["per-universe"][fixture.universe] = []
    if any([len([i for i in fixture.address_range if i in j]) > 0 for j in self.__fixtures["per-universe"][fixture.universe]]):
        raise ValueError("There is already a Fixture within that address!")

    self.__fixtures["all"].append(fixture)
    self.__fixtures["per-universe"][fixture.universe].append(fixture)

  def add_fixtures(self, *fixtures):
    """
    Adds multiple Fixtures to the fixture list

    :param Fixture \*fixtures: The Fixtures to add
    :raises TypeError: If one or more of the fixtures is not a Fixture
    :raises ValueError: If the address of one or more of the fixtures is already used in the universe


    Example
    ---------

    .. code-block:: python3

       from DmxOscServer import DmxOscServer, Fixture

       server = DmxOscServer()

       def handler(fixture, address, *args): print(fixture.values)

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
    :raises TypeError: If the fixture is not a Fixture
    :raises ValueError: If the address of the fixture is already used in the universe


    Example
    ---------

    .. code-block:: python3

       from DmxOscServer import DmxOscServer, Fixture

       server = DmxOscServer()

       @server.define_fixture(0, 0, 3)
       def rgb_handler(fixture, address, *args):
           print(fixture.values)
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
    if universe is False: return self.__fixtures["all"]
    elif universe in self.__fixtures["per-universe"]: return self.__fixtures["per-universe"][universe]
    else: return []

  def run(self, ip="0.0.0.0", port=9000):
    """
    Start the server run

    Should be called always AFTER all fixtures are added

    :param str ip: The IP address to listen on
    :param int port: The Port to listen on
    """
    self.__osc_server = ThreadingOSCUDPServer((ip, port), self.__dispatcher)
    print ("Serving on {}".format(self.__osc_server.server_address))
    self.__osc_server.serve_forever()

  def __setattr__(self, name, value):
    if name not in ["__fixtures","__dispatcher","__osc_server"]: pass
    elif name not in self.__dict__: pass
    else: raise AttributeError("Can't modify {}".format(name))
    super().__setattr__(name, value)
