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
from DmxOscServer import DmxOscServer, Fixture

def my_rgb_handler(fixture, address, *args):
    fixture.values[address] = args[0]
    print (fixture.values)

server = DmxOscServer()
server.add_fixture(Fixture(0, 0, 3, my_rgb_handler)) # Register a 3 channel Fixture at address 0 of universe 0
server.run()
```


To change the IP and/or port, you can add them to the DmxOscServer initializer

```py
server = DmxOscServer("10.10.123.5", 1234) # Will listen on 10.10.123.5:1234
```


You can add multiple fixtures at once using:

```py
server = DmxOscServer()
server.add_fixtures(
    Fixture(0, 0, 3, my_rgb_handler), # Register a 3 channel Fixture at address 0 of universe 0
    Fixture(0, 3, 3, my_rgb_handler), # Register a 3 channel Fixture at address 3 of universe 0
)
```
