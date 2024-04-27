# Class for decoding messages
# suppose to decode receiving message for both RF and BLE
import machine
from micropython import const
import struct

class processMssg:
    def process(self, mssg):
        # mode identifier
        remote_identifier = const(0x01)
        auto_identifier = const(0x02)
        time_identifier = const(0x03)
        bleTest_identifier = const(0x04)
        test_identifier = const(0x21)
        
        print("Processing message...")

        # Extract the mode identifier
        mode_identifier = mssg[0]

        print(mode_identifier)
        
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

        elif mode_identifier == test_identifier:
            return "T"

        elif mode_identifier == bleTest_identifier:
            instruction = self.__decodeData(mssg)
            return "BRT", instruction
            
        else:
            # Invalid mode
            return "E"

    def __decodeData(self, mssg):
        # data type identifier
        integer_identifier = 0x01
        float_identifier = 0x02

        # Essentials for decoding message
        mssgStartingIndex = 6
        intBufferSize = 4
        floatBufferSize = 4
        
        # Pick out where the data type identifier is stored in the message
        dataType_identifier = mssg[1]
        
        # Get the length of the information
        dataLength = struct.unpack('i', mssg[2:mssgStartingIndex])[0]

        # Decode data based on the stored data type identifier
        if dataType_identifier == float_identifier:
            float_value = struct.unpack('f'* dataLength, mssg[mssgStartingIndex:mssgStartingIndex+(floatBufferSize*dataLength)])
            float_value = [round(num,6) for num in float_value]
            print(float_value)
            return float_value # return decoded message

        elif dataType_identifier == integer_identifier:
            integer_value = struct.unpack('i'* dataLength, mssg[mssgStartingIndex:mssgStartingIndex+(intBufferSize*dataLength)])
            print(integer_value)
            return integer_value # return decoded message

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



