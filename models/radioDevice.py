from datetime import datetime


class RadioDevice:
    def __init__(
        self,
        device_id: int,
        frequency: int | float,
        power: int | float,
        last_measurement: datetime | None = None,
        is_connected: bool = False,
    ) -> None:
        self.id = device_id
        self.frequency = frequency
        self.power = power
        self.last_measurement = last_measurement
        self.is_connected = is_connected

    def set_frequency(self, frequency: int | float) -> None:
        self.frequency = frequency

    def connect(self) -> None:
        self.is_connected = True

    def disconnect(self) -> None:
        self.is_connected = False

    def set_last_measurement(self) -> None:
        self.last_measurement = datetime.now()
