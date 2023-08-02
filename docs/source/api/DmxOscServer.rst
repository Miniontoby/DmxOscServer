==============
DmxOscServer
==============

.. currentmodule:: DmxOscServer.DmxOscServer

.. Don't include inherited members to keep the doc short
.. autoclass:: DmxOscServer.DmxOscServer
    :members:


Example
---------

.. code-block:: python

    from DmxOscServer import DmxOscServer

    server = DmxOscServer()

    @server.define_fixture(0, 0, 3) # Defines a fixture at universe 0, starting_address 0, with 3 channels
    def rgb_handler(fixture, address, *args):
      print ("Fixture got changed at {} to {}".format(address, args))

    server.run()
