# Class for decoding messages
# suppose to decode receiving message for both RF and BLE
import machine
from micropython import const
import struct

class processMssg:
    def __init__(self):
        # Variable for keeping track whether boat is currently performing an auto task or not
        # If true, no message will be sent to the boat or processed by the boat
        self.boatBusy = False

        # Remote mode variables

        # Auto mode variables
        self.getWaypoints = False
        self.getFileName = False
        self.expectedWaypoints = 0
    
    def process(self, mssg):
        # mode identifier
        remote_identifier = const(0x01)
        auto_identifier = const(0x02)
        time_identifier = const(0x03)

        print("Processing message...")

        # Extract the mode identifier
        mode_identifier = mssg[0]

        # Check for valid message length
        if(len(mssg)!=1):
            # Check for valid mode
            if mode_identifier == remote_identifier:
                return "R"

            elif mode_identifier == auto_identifier:
                return "A"

            elif mode_identifier == time_identifier:
                # Set time locally
                instruction = self.__decodeData(mssg)
                self.__setTimeLocally(instruction)
                return "I"

            else:
                # Invalid mode
                return "E"
        else:
            return "E"

    def __decodeData(self, mssg):
        # data type identifier
        integer_identifier = const(0x01)
        double_identifier = const(0x02)

        # Essentials for decoding message
        mssgStartingIndex = 6
        intBufferSize = 4
        doubleBufferSize = 8

        dataType_identifier = mssg[1]
        
        # Get the length of the information
        dataLength = struct.unpack('i', mssg[2:mssgStartingIndex])[0]

        if dataType_identifier == double_identifier:
            double_value = struct.unpack('d'* dataLength, mssg[mssgStartingIndex:mssgStartingIndex+(doubleBufferSize*dataLength)])
            print(double_value)
            return double_value

        elif dataType_identifier == integer_identifier:
            print(len( mssg[mssgStartingIndex:mssgStartingIndex+(intBufferSize*dataLength)]))
            integer_value = struct.unpack('i'* dataLength, mssg[mssgStartingIndex:mssgStartingIndex+(intBufferSize*dataLength)])
            print(integer_value)
            return integer_value

        else:
            raise ValueError("Unknown identifier")

    def __setTimeLocally(self, dateTime):
        # Set the RTC (Real-Time Clock) with the specified values
        rtc = machine.RTC()

        year = dateTime[0]+2000
        month = dateTime[1]
        day = dateTime[2]
        weekday = 0

        hours = dateTime[3]
        minutes = dateTime[4]
        seconds = dateTime[5]
        subseconds = 0

        # Set the local (year, month, day, weekday, hours, minutes, seconds, subseconds)
        rtc.datetime((year, month, day, weekday, 
                    hours, minutes, seconds, subseconds))



