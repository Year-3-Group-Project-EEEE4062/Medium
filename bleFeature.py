# This example demonstrates a UART periperhal.

# This example demonstrates the low-level bluetooth module. For most
# applications, we recommend using the higher-level aioble library which takes
# care of all IRQ handling and connection management. See
# https://github.com/micropython/micropython-lib/tree/master/micropython/bluetooth/aioble

import bluetooth
import random
import struct
import time
from lib.BLE.ble_advertising import advertising_payload

from micropython import const

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)

_FLAG_READ = const(0x0002)
_FLAG_WRITE_NO_RESPONSE = const(0x0004)
_FLAG_WRITE = const(0x0008)
_FLAG_NOTIFY = const(0x0010)

UUID = "8d4bfdb1-f5ee-4f87-a0a8-50d82ad6db76"

_UART_UUID = bluetooth.UUID(UUID)

_UART_TX = (
    bluetooth.UUID(UUID),
    _FLAG_READ | _FLAG_NOTIFY,
)
_UART_RX = (
    bluetooth.UUID(UUID),
    _FLAG_WRITE | _FLAG_WRITE_NO_RESPONSE,
)
_UART_SERVICE = (
    _UART_UUID,
    (_UART_TX, _UART_RX),
)


class mediumBLE:
    def __init__(self, connectedCallback, disconnectCallback, receiveCallback, name="Medium"):
        # Create a Bluetooth Low Energy (BLE) object
        self._ble = bluetooth.BLE()
        self._ble.active(True)
        self._ble.irq(self._irq)

        ((self._handle_tx, self._handle_rx),) = self._ble.gatts_register_services((_UART_SERVICE,))
        
        # Create empty set to store connections
        self._connections = set()

        # Create callbacks for different event
        # This is so that in any event, it would return back to main.py file
        self._connectedCallback = connectedCallback
        self._disconnectCallback = disconnectCallback
        self._rxCallback = receiveCallback
    
        self._payload = advertising_payload(name=name, services=[_UART_UUID])
        self._advertise()    

    def _irq(self, event, data):
        # Track connections so we can send notifications.
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data

            # Keep track of connections
            self._connections.add(conn_handle)

            # After establish connection stop advertising
            self._ble.gap_scan(None)

            # Callback
            self._connectedCallback()

        # Disconnected event
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data

            # Remove connection
            self._connections.remove(conn_handle)
            
            # Start advertising again to allow a new connection.
            self._advertise()

            # Callback
            self._disconnectCallback()

        # Receiving data event
        elif event == _IRQ_GATTS_WRITE:
            conn_handle, value_handle = data
            value = self._ble.gatts_read(value_handle)
            if value_handle == self._handle_rx:
                # give received data to callback function
                self._rxCallback(value)

    def send(self, data):
        for conn_handle in self._connections:
            self._ble.gatts_notify(conn_handle, self._handle_tx, data)

    def is_connected(self):
        return len(self._connections) > 0

    def _advertise(self, interval_us=500000):
        print("Starting advertising")
        self._ble.gap_advertise(interval_us, adv_data=self._payload)
        