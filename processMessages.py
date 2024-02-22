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
        print(len(mssg))

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
                # User chooses remote mode
                instruction = self.__decodeData(mssg)
                self.__processRemoteMssg(instruction)
                return "R"

            elif mode_identifier == auto_identifier:
                # User chooses auto mode
                instruction = self.__decodeData(mssg)
                self.__processAutoMssg(instruction)
                return "A"

            elif mode_identifier == time_identifier:
                # Set time locally
                instruction = self.__decodeData(mssg)
                self.__setTimeLocally(instruction)
                return "Idle"

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

    def __processAutoMssg(self, autoMssg):
        pass

    def __processRemoteMssg(self, remoteMssg):
        # Determine whether it is a feature or movement messsage
        # feature message's length is always 1
        # movement message's length is always 2
        if(len(remoteMssg)==1):
            print("User using remote features!")
            # This means that it is a features message
            if(remoteMssg[0]==0):
                # Indicating user using measure feature
                print("Using remote measure feature!")
                # Call that function here to do the feature

            elif(remoteMssg[0]==1):
                # Indicating user using go home feature
                print("Using remote go home feature!")
                # Call that function here to do the feature

        elif(len(remoteMssg)==2):
            print("User using remote movements!")
            # This means that it is a movement message
            # Have to ask Donald how he sets slow, average and fast motion on the boat

            # Check for movement only (temporary)
            if(remoteMssg[0]==0):
                print("Boat moves forward!")
                # Call the motor function here

            elif(remoteMssg[0]==1):
                print("Boat moves backwards!")
                # Call the motor function here

            elif(remoteMssg[0]==2):
                print("Boat moves rightwards!")
                # Call the motor function here

            elif(remoteMssg[0]==3):
                print("Boat moves leftwards!")
                # Call the motor function here

            else:
                # Invalid movement control
                print("Invalid movement!")

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



