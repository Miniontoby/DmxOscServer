# Fixture Default Class

class Fixture():
  """
  Instantiate a Fixture

  :param int universe: The universe for this Fixture
  :param int starting_addr: The starting address for this Fixture
  :param int channels: The amount of channel that this Fixture should have
  :param handler: The callback function be to called when a message is received for this address
  :type handler: function
  :param bool channel_as_arra: Specify if the channels are lists or not
  """
  def __init__(self, universe, starting_addr, channels, handler, channel_as_array=False):
    self.universe = universe
    self.starting_addr = starting_addr
    self.channels = channels
    self.end_addr = starting_addr + channels
    self.address_range = range(self.starting_addr, self.end_addr)
    self.channel_as_array = channel_as_array
    self._handler = handler
    self.values = [[0]] * channels if channel_as_array else [0] * channels

  def __call__(self, address: int, *args):
    """
    Makes the Fixture callable for the server

    :param int address: The address of this Fixture that was called
    :param *args: The arguments sent by the OSC Client
    :raises ValueError: If the address is not within range

    :returns: The result from the handler function
    """
    # Set the values property
    relative_addr = address - self.starting_addr
    if address in self:
      if self.channel_as_array:
        if isinstance(args[0], list): # args = ([0.1, 0.5, 0.9])
          self.values[relative_addr] = args[0]
        elif isinstance(args[0], tuple): # args = ((0.1, 0.5, 0.9))
          self.values[relative_addr] = list(args[0])
        elif isinstance(args, tuple): # args = (0.1, 0.5, 0.9)
          self.values[relative_addr] = list(args)
      elif isinstance(args[0], list): # args = ([0.1, 0.5])
        self.values[relative_addr:relative_addr+len(args[0])] = args[0]
      elif isinstance(args[0], tuple): # args = ((0.1, 0.5))
        self.values[relative_addr:relative_addr+len(args[0])] = list(args)[0]
      elif isinstance(args, tuple): # args = (0.1,) and (0.1, 0.5)
        self.values[relative_addr:relative_addr+len(args)] = list(args)

      return self._handler(self, address, *args)
    else:
      raise ValueError("Address {} is not within the address range!".format(address))

  def __contains__(self, addr: int):
    """
    Checks if the address is in this Fixture's address range

    :param int addr: The address to look for

    :returns: True if the address is within this Fixture's address
    :rtype: bool
    """
    return addr in self.address_range

  def __str__(self):
    """
    This will be used as the template when printing the Fixture object

    :returns: The Fixture class as a string
    :rtype: str
    """
    return 'Fixture(universe={0.universe}, starting_addr={0.starting_addr}, channels={0.channels}, channel_as_array={0.channel_as_array}, values={0.values})'.format(self)

  def __setattr__(self, name, value):
    if name not in ["universe","starting_addr","channels","end_addr","address_range","channel_as_array","handler","values"]: pass
    elif name not in self.__dict__: pass
    else: raise AttributeError("Can't modify {}".format(name))
    super().__setattr__(name, value)
