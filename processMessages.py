# Class for decoding messages
# suppose to decode receiving message for both RF and BLE
import machine
import utime

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
        

    def __setTimeLocally(self, dateTime):
        # Set the RTC (Real-Time Clock) with the specified values
        rtc = machine.RTC()
        # (year, month, day, weekday, hours, minutes, seconds, subseconds)
        rtc.datetime((year=dateTime[0]+2000, month=dateTime[1], day=dateTime[2], 0, hour=dateTime[3], minute=dateTime[4], second=dateTime[5], 0))

        # Debug purpose
        local_time = utime.localtime()
        print(f"Manually set local time: {local_time}")


