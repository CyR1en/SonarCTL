# sonar.py
import time
import rtmidi
from steelseries_sonar_py import Sonar
from src.SonarCTL.logger import Logger

# Initialize Logger
logger = Logger()

# Initialize Sonar
sonar = Sonar("C:\\ProgramData\\SteelSeries\\SteelSeries Engine 3\\coreProps.json")
is_streaming = sonar.is_streamer_mode()

# Initialize MIDI
midi_in = rtmidi.MidiIn()

def midi_callback(message, data=None):
    logger.log("MIDI message received: " + str(message))
    msg, time_delta = message
    status, control, value = msg[0], msg[1], msg[2]
    if (status & 0xF0) == 0xB0:
        logger.log(f"Control Change: Control {control}, Value {value}")
        volume = map_midi(value, 0, 127, 0.0, 1.0)
        logger.log(f"Volume: {volume}")
        sonar.set_volume("media", volume, streamer_slider="monitoring")

def open_sonar_ctl_midi_port(available_ports):
    for i, port in enumerate(available_ports):
        if "SonarCTL" in port:
            midi_in.open_port(i)
            if midi_in.is_port_open():
                logger.log(f'Opened MIDI port "{port}"')
                return True
    return False

def open_midi_port():
    global midi_in
    available_ports = midi_in.get_ports()
    logger.log("Available MIDI ports: " + str(available_ports))
    if available_ports:
        if open_sonar_ctl_midi_port(available_ports):
            midi_in.set_callback(midi_callback)
            logger.log(f'Set callback for MIDI port "{available_ports[0]}"')
            return True
        else:
            logger.log("Failed to open MIDI port.")
            return False
    else:
        logger.log("No available MIDI ports.")
        return False

def map_midi(value, in_min, in_max, out_min=0.0, out_max=1.0):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def midi_monitor():
    midi_connected = open_midi_port()
    try:
        while True:
            if not midi_connected or midi_in.get_port_count() == 0:
                logger.log("MIDI connection lost. Attempting to reconnect...")
                midi_in.close_port()
                midi_connected = open_midi_port()
            time.sleep(2)
    except KeyboardInterrupt:
        pass
    finally:
        midi_in.close_port()