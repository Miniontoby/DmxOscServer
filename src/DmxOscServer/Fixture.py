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
  :param handler: The callback function that should be called when a DMX message is received for this Fixture
  :type handler: def
  """
  def __init__(self, universe, starting_addr, channels, handler):
    self.universe = universe
    self.starting_addr = starting_addr
    self.channels = channels
    self.end_addr = starting_addr + channels
    self.handler = handler
    self.values = [0] * channels
