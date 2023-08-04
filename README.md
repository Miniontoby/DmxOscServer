# DMX OSC Server

DMX OSC Server is a python lib to make it easier to create OSC Servers for the DMX Protocol.

It allows you to register fixtures are the wanted universe, starting address and channels.
You will also be able to add an handler which will be called when a message is received for that fixture.


## Installation

```bash
pip install DmxOscServer
```

## Get Started

To create a simple DMX OSC Server that will listen on 0.0.0.0:9000 you can use this code:

```py
from DmxOscServer import DmxOscServer

server = DmxOscServer()

# Define a 3 channel Fixture at address 0 at universe 0 which will execute my_rgb_handler when called
@server.define_fixture(0, 0, 3)
def my_rgb_handler(fixture, address, *args):
    print ("{} got {}".format(address, args))

server.run()
```

To make the define more readable, you can use the argument names

```py
# Define a 3 channel Fixture at address 0 at universe 0 which will execute my_rgb_handler when called
@server.define_fixture(universe=0, starting_addr=0, channels=3)
def my_rgb_handler(fixture, address, *args):
    print ("{} has been set to {}".format(address, args))
```


To change the IP and/or port, you can specify that at the `.run()` method

```py
server.run("10.10.123.5", 1234) # Will listen on 10.10.123.5:1234
```


It is also possible to use the `Fixture` class and the `add_fixture` method

```py
from DmxOscServer import DmxOscServer, Fixture

def my_rgb_handler(fixture, address, *args):
    print ("{} has been set to {}".format(address, args))

server = DmxOscServer()
server.add_fixture(Fixture(0, 0, 3, my_rgb_handler)) # Register a 3 channel Fixture at address 0 at universe 0
```


And for the `add_fixture` method, you can also add multiple fixtures at once using:

```py
from DmxOscServer import DmxOscServer, Fixture
server = DmxOscServer()
server.add_fixtures(
    Fixture(0, 0, 3, my_rgb_handler), # Register a 3 channel Fixture at address 0 of universe 0
    Fixture(0, 3, 3, my_rgb_handler), # Register a 3 channel Fixture at address 3 of universe 0
)
```


You can use the `fixture.values` property to see all the current values

```py
@server.define_fixture(0, 0, 3)
def my_rgb_handler(fixture, address, *args):
    print (fixture.values)
```


# The handler

The handler receives a call when a message is received for that fixture
Arguments: `(fixture, address, *args)`
- `fixture` is the fixture, so you have a reference
- `address` is the message address (it starts at the starting_address, so use `address - fixture.starting_addr` if you want to have the internal address)
- `*args` are the args of the message. It is almost always 1 int going from 0 to 1, so you can just use `args[0]` in your code and multiply it by your max value

The handler should never receive an address out of its address range, if the fixture is called correctly

# More Documentation

More Documentation can be found at https://dmxoscserver.readthedocs.io/en/latest/
