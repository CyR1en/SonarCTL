# src/SonarCTL/sonar.py
import json
import time
import rtmidi
from steelseries_sonar_py import Sonar
from src.SonarCTL.logger import Logger


class SonarMidiListener:
    def __init__(self, core_props_path, status_callback=None, channel_mappings=None, logger=None):
        self.logger = logger
        print(core_props_path)
        self.sonar = Sonar(core_props_path)
        self.midi_in = rtmidi.MidiIn()
        self.channel_mappings = channel_mappings or {}
        self.status_callback = status_callback

    def midi_callback(self, message, data=None):
        msg, time_delta = message
        status, control, value = msg[0], msg[1], msg[2]
        if (status & 0xF0) == 0xB0:
            self.logger.log(f"Control Change: Control {control}, Value {value}")
            volume = self.map_midi(value, 0, 127, 0.0, 1.0)
            self.logger.log(f"Volume: {volume}")
            mapped_channel = self.channel_mappings.get(f"channel_{control}")
            if mapped_channel and mapped_channel != "None":
                channel = mapped_channel.lower()
                volume = round(volume, 2)
                self.logger.log(f"Setting volume for {channel} to {volume}")
                try:
                    result = self.sonar.set_volume(channel, volume, streamer_slider="monitoring")
                    self.logger.log(result)
                except Exception as e:
                    self.logger.log(e)

    def open_sonar_ctl_midi_port(self, available_ports):
        for i, port in enumerate(available_ports):
            if "SonarCTL" in port:
                self.midi_in.open_port(i)
                if self.midi_in.is_port_open():
                    self.logger.log(f'Opened MIDI port "{port}"')
                    return True
        return False

    def open_midi_port(self):
        available_ports = self.midi_in.get_ports()
        self.logger.log("Available MIDI ports: " + str(available_ports))
        if available_ports:
            if self.open_sonar_ctl_midi_port(available_ports):
                self.midi_in.set_callback(self.midi_callback)
                self.logger.log(f'Set callback for MIDI port "{available_ports[0]}"')
                if self.status_callback:
                    self.status_callback(True)  # Notify connection status
                return True
            else:
                self.logger.log("Failed to open MIDI port.")
                if self.status_callback:
                    self.status_callback(False)  # Notify connection status
                return False
        else:
            self.logger.log("No available MIDI ports.")
            if self.status_callback:
                self.status_callback(False)  # Notify connection status
            return False

    @staticmethod
    def map_midi(value, in_min, in_max, out_min=0.0, out_max=1.0):
        return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def midi_monitor(self):
        print("Monitoring MIDI...")
        midi_connected = self.open_midi_port()
        try:
            while True:
                if not midi_connected or self.midi_in.get_port_count() == 0:
                    self.logger.log("MIDI connection lost. Attempting to reconnect...")
                    self.midi_in.close_port()
                    midi_connected = self.open_midi_port()
                time.sleep(2)
        except KeyboardInterrupt:
            pass
        finally:
            self.midi_in.close_port()
            if self.status_callback:
                self.status_callback(False)  # Notify disconnection status

    def start(self):
        self.midi_monitor()
