"""
Arduino in Junying's setup.

Sends out TTL pulses to NI-DAQ.
TTL pulses trigger acquisition and convey stimulus information.

"""

import logging
import time

import serial

from trigger_count.log import get_basic_logger

BAUD_RATE = 9600
PORT = "/dev/ttyACM0"
POSSIBLE_STIM_TRIGGERS = ["A", "B"]


class AutoStopArduino:
    """
    Serial communication with arduino.
    This arduino is programmed to stop acquisition automatically after some time.
    """
    def __init__(self, port: str = PORT, logger: logging.Logger | None = None) -> None:
        # params
        self.port = port
        self.logger = logger

        # go
        if self.logger is None:
            self.logger = get_basic_logger("arduino")
        self.serial_connection = serial.Serial(
            port=port,
            baudrate=BAUD_RATE,
        )
        self.logger.info(f"Serial connection established: {PORT}")
        time.sleep(1)

    def send_acquisition_trigger(self) -> None:
        self.serial_connection.write("T".encode())
        self.logger.info("Acquisition trigger sent.")

    def send_stim_trigger(self, code: str = "A") -> None:
        assert code in POSSIBLE_STIM_TRIGGERS
        self.serial_connection.write(code.encode())
        self.logger.info(f"Stim trigger sent: {code}")

    def confirm(self) -> None:
        reply = self.serial_connection.readline()
        reply = reply.decode().strip()
        assert reply == "X", f"{reply=}"
        self.logger.info(f"Received confirmation: {reply}")

    def close(self) -> None:
        self.serial_connection.close()
        self.logger.info(f"Serial connection closed: {PORT}")


class ManualStopArduino:
    """Serial communication with arduino.
    This arduino needs commands to both start and stop a recording.
    """
    def __init__(self, port: str = PORT, logger: logging.Logger | None = None) -> None:
        # params
        self.port = port
        self.logger = logger

        # go
        if self.logger is None:
            self.logger = get_basic_logger("arduino")
        self.serial_connection = serial.Serial(
            port=port,
            baudrate=BAUD_RATE,
        )
        self.logger.info(f"Serial connection established: {PORT}")
        time.sleep(1)

    def send_acquisition_start(self) -> None:
        self.serial_connection.write("S".encode())
        self.logger.info("Acquisition start trigger sent.")

    def send_acquisition_end(self) -> None:
        self.serial_connection.write("T".encode())
        self.logger.info("Acquisition end trigger sent.")

    def send_stim_start(self) -> None:
        self.serial_connection.write("A".encode())
        self.logger.info("Stim start trigger sent.")

    def send_stim_end(self) -> None:
        self.serial_connection.write("B".encode())
        self.logger.info("Stim end trigger sent.")

    def send_trial_type(self, trial_character: str) -> None:
        self.serial_connection.write(trial_character.encode())
        self.logger.info(f"Trial type trigger {trial_character} sent.")

    def close(self) -> None:
        self.serial_connection.close()
        self.logger.info(f"Serial connection closed: {PORT}")