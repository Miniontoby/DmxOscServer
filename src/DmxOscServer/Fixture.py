# Fixture Default Class

class Fixture():
  """
  Instantiate a Fixture

  :param universe: The universe for this Fixture
  :type universe: int
  :param starting_addr: The starting address for this Fixture
  :type starting_addr: int
  :param channels: The amount of channel that this Fixture should have
  :type channels: int
  :param handler: The callback function be to called when a message is received for this address
  :type handler: function
  """
  def __init__(self, universe, starting_addr, channels, handler):
    self.universe = universe
    self.starting_addr = starting_addr
    self.channels = channels
    self.end_addr = starting_addr + channels
    self.handler = handler
    self.values = [0] * channels

  def __call__(self, address: int, *args):
    """
    Makes the Fixture callable for the server

    :param address: The address of this Fixture that was called
    :type address: int
    :param *args: The arguments sent by the OSC Client
    """
    return self.handler(self, address, *args)

  def __contains__(self, addr: int):
    """
    Checks if the address is in this Fixture's address range

    :param addr: The address to look for
    :type addr: int

    :returns: True if the address is within this Fixture's address
    """
    return addr in range(self.starting_addr, self.end_addr)

  def __str__(self):
    """
    This will be used as the template when printing the Fixture object

    :returns: The Fixture class as a string
    """
    return 'Fixture(universe={0.universe}, starting_addr={0.starting_addr}, channels={0.channels}, values={0.values})'.format(self)
