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

    def set_power(self, power: int | float) -> None:
        self.power = power

    def connect(self) -> None:
        self.is_connected = True

    def disconnect(self) -> None:
        self.is_connected = False

    def get_status(self) -> bool:
        return self.is_connected

    def measure_signal(self) -> None:
        self.last_measurement = datetime.now()
