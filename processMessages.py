# Class for decoding messages
# suppose to decode receiving message for both RF and BLE
import machine

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
        print("processing message...")

        # Decode the data
        decoded = list(mssg)

        # Indicate that the message related to remote mode
        if(decoded[0]==0):
            self.__processRemoteMssg(decoded) 
            return "R"
        
        # Indicate that the message related to auto mode
        elif(decoded[0]==1):
            
            return "A"
        
        # Indicate that the message related to setting local time
        elif(decoded[0]==2):
            self.__setTimeLocally(decoded)
            return "Idle"
        
        # Invalid message
        else:
            # return "E" to indicate on OLED screen that mssg invalid
            return "E"

    
    def __processAutoMssg(self,autoMssg):
        pass

    def __processRemoteMssg(self, remoteMssg):
        # Determine whether it is a feature or movement messsage
        # feature message's length is always 2
        # movement message's length is always 3
        if(len(remoteMssg)==2):
            print("User using remote features!")
            # This means that it is a features message
            if(remoteMssg[1]==0):
                # Indicating user using measure feature
                print("Using remote measure feature!")
                pass
            elif(remoteMssg[2]==1):
                # Indicating user using go home feature
                print("Using remote go home feature!")
                pass

        elif(len(remoteMssg)==3):
            print("User using remote movements!")
            # This means that it is a movement message
            # Have to ask Donald how he sets slow, average and fast motion on the boat

            # Check for movement only (temporary)
            if(remoteMssg[2]==0):
                print("Boat moves forward!")
            elif(remoteMssg[2]==1):
                print("Boat moves backwards!")
            elif(remoteMssg[2]==2):
                print("Boat moves rightwards!")
            elif(remoteMssg[2]==3):
                print("Boat moves leftwards!")
            else:
                # Invalid movement control
                print("Invalid movement!")

    def __setTimeLocally(self, dateTime):
        # Set the RTC (Real-Time Clock) with the specified values
        rtc = machine.RTC()

        # Extract date and time data
        year = dateTime[1]+2000
        month = dateTime[2]
        day = dateTime[3]
        weekday = 0
        hours = dateTime[4]
        minutes = dateTime[5]
        seconds = dateTime[6]
        subseconds = 0

        # (year, month, day, weekday, hours, minutes, seconds, subseconds)
        rtc.datetime((year, month, day, weekday, hours, minutes, seconds, subseconds))


    import struct

# def extract_doubles_from_string(input_string):
#     try:
#         # Split the input string using the comma as a delimiter
#         double_str1, double_str2 = input_string.split(',')

#         # Unpack the double values from the string
#         double1, = struct.unpack('d', double_str1.encode())
#         double2, = struct.unpack('d', double_str2.encode())

#         return double1, double2
#     except ValueError:
#         print("Invalid input format. Please provide two comma-separated double values.")

# # Example usage
# input_str = "104.253562435452,150.2145124"
# double1, double2 = extract_doubles_from_string(input_str)
# print(f"Extracted doubles: {double1}, {double2}")



