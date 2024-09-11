import RPi.GPIO as IO
from time import sleep
from typing import Tuple, Union
import spidev
from collections import Counter
from enum import IntEnum


W1_SENSOR_ID_OFFSET = 200

class HwType(IntEnum):
    Relay = 0
    DO = 1 # digital output
    DI = 2 # digital input
    AI = 3 # analog input
    W1_SENSOR = 4 # temperature sensor

class HwDirection(IntEnum):
    INPUT = 0
    OUTPUT = 1

class RelayActions(IntEnum):
    OFF = 0
    ON = 1

class DoActions(IntEnum):
    Deactivated = 0
    Activated = 1

class DiStates(IntEnum):
    Grounded = 0
    High = 1

class EBRPIH1118:
    ADC_CHANN_NUM = 4
    NUM_OF_READ = 5
    NUM_OF_REL = 4
    NUM_OF_INPUT = 5
    NUM_OF_OUTPUT = 5
    FIRST_DO = 5
    FIRST_VOICE = 10
    out_pin_dict =  {1:17,2:27,3:12,4:19}
    relays_gpios = list(out_pin_dict.values())
    dout_pin_dict = {1:21,2:20,3:25,4:26,5:24}
    dout_gpios = list(dout_pin_dict.values())
    din_pin_dict = {1:23,2:18,3:5,4:4,5:6}
    din_gpios = list(din_pin_dict.values())
    reference_ai_volt = 3.25
    ai_channels = (1,2,3,4)
    
    def __init__(self):
        self.spi = spidev.SpiDev(0,0)
        self.spi.max_speed_hz = 1000000
        IO.setmode(IO.BCM)
        IO.setwarnings(False)
        self.setup_gpios(EBRPIH1118.relays_gpios, IO.OUT, initial=IO.LOW)
        self.setup_gpios(EBRPIH1118.dout_gpios, IO.OUT, initial=IO.LOW)
        self.setup_gpios(EBRPIH1118.din_gpios, IO.IN, pull_up_down=IO.PUD_OFF)

    def energize_relay(self,relay_number):
        if (relay_number <= EBRPIH1118.NUM_OF_REL):
            IO.output(EBRPIH1118.out_pin_dict[relay_number], IO.HIGH)
            return True
        else:
            return False


    def relay_on(self, relay_number) -> tuple:
        """
        Trun on the actual relays (0-4) only
        return boolean shows the success state, and error string if there is any.
        """
        rc, msg = self.check_relay_number(relay_number)
        if not rc:
            return (rc, msg)
        
        relay_gpio_pin = type(self).out_pin_dict[relay_number]
        IO.output(relay_gpio_pin,IO.HIGH)
        if not self._verify_relay_state(relay_gpio_pin, 1):
            reutn (False, f"Unable to trun on relay: '{relay_number}'")
        return (True, f"Relay: '{relay_number}' has been activated.")
    
    def relay_off(self, relay_number) -> tuple:
        """
        Trun on the actual relays (0-4) only
        return boolean shows the success state, and error string if there is any.
        """
        rc, msg = self.check_relay_number(relay_number)
        if not rc:
            return (rc, msg)

        relay_gpio_pin = EBRPIH1118.out_pin_dict[relay_number]
        IO.output(relay_gpio_pin,IO.LOW)
        if not self._verify_relay_state(relay_gpio_pin, 0):
            reutn (False, f"Unable to trun off relay: '{relay_number}'")
        return (True, f"Relay: '{relay_number}' has been deactivated.")


    def check_relay_number(self, relay_number) -> tuple:
        relay_numbers = list(type(self).out_pin_dict.keys())
        if not relay_number in relay_numbers:
            print(f"Invalid relay number, Valid numbers: '{relay_numbers}'")
            return (False, f"Invalid relay number, Valid numbers: '{relay_numbers}'")
        return (True, "")


    def energize_all_relay(self):
        print("energizing all")
        ret = list(map(self.energize_relay,EBRPIH1118.out_pin_dict.keys()))
        if False in ret:
            return False
        else:
            return True

    def denergize_relay(self, relay_number):
        if (relay_number <= EBRPIH1118.NUM_OF_REL):
            IO.output(EBRPIH1118.out_pin_dict[relay_number], IO.LOW)
            return True
        else:
            return False
    
    def denergize_all_relay(self):
        ret= list(map(self.denergize_relay,EBRPIH1118.out_pin_dict.keys()))
        if False in ret:
            return False
        else:
            return True


    def check_DI(self,input_string):
        valid_numbers = list(type(self).din_pin_dict.keys())
        try:
            input_number=list(map(int,input_string.split(",")))
        except:
            return (False, f"Invalid digital input number. Valid digital input numbers: {valid_numbers}")
        di_dict={}
        for pin in input_number:
            if pin>EBRPIH1118.NUM_OF_INPUT:
                return (False, f"Invalid digital input number: {pin}. Valid digital input numbers: '{valid_numbers}'")
            state = ['Grounded','High'][IO.input(EBRPIH1118.din_pin_dict[pin])]
            di_dict.update({pin:state})
        return (True, di_dict)
    

    def check_DI_by_id(self, channel_id) -> Tuple[bool,int]:
        """simply returns the value from the GPIO to the user."""
        if channel_id > EBRPIH1118.NUM_OF_INPUT:
            return (False, f"Invalid digital input number: {channel_id}.")
        
        return (True, IO.input(EBRPIH1118.din_pin_dict[channel_id]))
    
    def active_DO(self,do_number) -> tuple:
        if(do_number>EBRPIH1118.NUM_OF_OUTPUT):
            return (False, f"Invalid Digital Output Number. Valid numbers: {list(type(self).dout_pin_dict.keys())}")
        
        IO.output(EBRPIH1118.dout_pin_dict[do_number],IO.HIGH)
        return (True, f"Digital output: {do_number} has been activated")


    def deactive_DO(self,do_number):
        if(do_number>EBRPIH1118.NUM_OF_OUTPUT):
            return (False, f"Invalid Digital Output Number. Valid numbers: {list(type(self).dout_pin_dict.keys())}")
        
        IO.output(EBRPIH1118.dout_pin_dict[do_number],IO.LOW)
        return (True, f"Digital output: {do_number} has been deactivated")
    

    def _verify_relay_state(self, relay_number:int, state:str) -> bool:
        """
            Verify the requested state on the actual relay number
            1 means the relay is energized
            0  means the realy is de-energized
        """
        return IO.input(relay_number) == state
    
    def setup_gpios(self, pins:list, gpio_function:int, **kwargs):
        if self._verify_gpio_func(pins, gpio_function):
            print(f"The {pins=} has been already set to {gpio_function=}")
            # we should always setup GPIOs since the IO module requires.
            # but if the GPIO has already been set, we dont not want to set
            # initial values. because it would reset the current state.
            # this would be helpful if this module gets recalled and we dont 
            # want to change the state e.g. relays.
            kwargs = {}
        IO.setup(pins, gpio_function, **kwargs)

    def _verify_gpio_func(self, pins:list, expected_func:int) -> bool:
        for pin in pins:
            if not expected_func == IO.gpio_function(pin):
                return False
        return True
    
    
    def _read_ai_value(self, channel, num_samples=10):
        readings = []
        for _ in range(num_samples):
            # Start bit + single-ended bit + channel bits + 000
            adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
            data = ((adc[1] & 3) << 8) + adc[2]
            readings.append(data)
            sleep(0.01)
        # Use Counter to find the most common reading
        most_common_data_list = Counter(readings).most_common(1)
        most_common_value, number_of_occured = most_common_data_list[0]
        converted_to_volt = ((most_common_value * type(self).reference_ai_volt) / 1024) * 10
        
        return f"{converted_to_volt:.2f}"

    @staticmethod
    def check_channels(channels:str, expected_channels:Tuple[list,tuple]) -> Tuple[bool,list]:
        """Helpers to check the given channels all are integers and compatible
            with 'expected' channels"""
        if len(channels) == 1: # if the channels is like '2'
            if not channels.isdigit():
                return (False, [])
            if not int(channels) in expected_channels:
                return (False, [])
            return (True, [int(channels)])

        try:
            channel_numbers=list(map(int,channels.split(",")))
        except:
            return (False, [])
        
        for channel_num in channel_numbers:
            if not channel_num in expected_channels:
                return (False, [])
        return (True, channel_numbers)

    
    def read_ai_channels(self, channels:str, num_samples=10):
        rc, channels = self.check_channels(channels=channels, expected_channels=type(self).ai_channels)
        if not rc:
            return (False, f"Ananlog input Channels: {channels} are not valid. valid channels: {type(self).ai_channels}")

        ai_dict = {}
        for channel in channels:
            channel -= 1 # in AI the channel number is zero-indexed
            ai_value = self._read_ai_value(channel, num_samples)
            ai_dict.update({(channel+1):ai_value})
        return (True, ai_dict)
    
    def read_single_ai_channel(self, channel_id:int, num_samples=10):
        if not channel_id in type(self).ai_channels:
            return (False, f"Invalid Analog Input channel number")
        # channel id is zero-indexed
        channel_id -= 1
        return (True, self._read_ai_value(channel_id,num_samples))


    def check_relay_state(self, channels: str) -> Tuple[bool, Union[dict,str]]:
        """
        @param: channels can be from 1 to 4, or in form of comma-separated like 1,2,3,4
        """
        rc, channels =  self.check_channels(channels=channels, expected_channels= type(self).out_pin_dict.keys())
        if not rc:
            return (False, f"Relay numbers: {channels} are not valid. valid channels: {list(type(self).out_pin_dict.keys())}")
        states_dict = {}
        for channel in channels:
            states_dict[channel] = IO.input(type(self).out_pin_dict[channel])
        return (True, states_dict)
    

    def check_single_relay_state(self, channel_id: int) -> Tuple[bool, int]:
        rc, channel =  self.check_channels(channels=str(channel_id), expected_channels= type(self).out_pin_dict.keys())
        if not rc:
            return (False, -1)
        return (True, IO.input(type(self).out_pin_dict[channel_id]))

    
    def check_do_states(self, channels: str) -> Tuple[bool, Union[dict,str]]:
        """
        @param: channels can be from 1 to 5, or in form of comma-separated like 1,2,3,4,5
        """
        rc, channels =  self.check_channels(channels=channels, expected_channels= type(self).dout_pin_dict.keys())
        if not rc:
            return (False, f"Digital Output numbers: {channels} are not valid. valid channels: {list(type(self).dout_pin_dict.keys())}")

        states_dict = {}
        for channel in channels:
            states_dict[channel] = IO.input(type(self).dout_pin_dict[channel])
        return (True, states_dict)
    
    def check_single_do_state(self, channel_id: int) -> Tuple[bool, int]:
        rc, channel =  self.check_channels(channels=str(channel_id), expected_channels= type(self).dout_pin_dict.keys())
        if not rc:
            return (False, -1)
        return (True, IO.input(type(self).dout_pin_dict[channel_id]))

    def cleanup(self):
        IO.cleanup()

