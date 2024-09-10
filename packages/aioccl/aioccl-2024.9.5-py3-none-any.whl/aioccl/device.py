"""Mapping to create a CCL Device copy."""
from __future__ import annotations

import logging
import time
from typing import Callable

from .sensor import CCLSensor, CCL_SENSORS

_LOGGER = logging.getLogger(__name__)

CCL_DEVICE_INFO_TYPES = ("serial_no", "mac_address", "model", "fw_ver")

class CCLDevice:
    def __init__(self, passkey: str):
        """Initialize a CCL device."""
        _LOGGER.debug('Initializing CCL Device: %s', self)
        self._passkey = passkey
        
        self._serial_no: str | None
        self._mac_address: str | None
        self._model: str | None
        self._fw_ver: str | None
        self._binary_sensors: dict[str, CCLSensor] | None = {}
        self._sensors: dict[str, CCLSensor] | None = {}
        self._last_updated_time: float | None

        self._new_sensors: list[CCLSensor] | None = []
        
        self._update_callbacks = set() 
        self._new_binary_sensor_callbacks = set()
        self._new_sensor_callbacks = set()
    
    @property
    def passkey(self) -> str:
        return self._passkey
    
    @property
    def device_id(self) -> str | None:
        return self._mac_address.replace(":", "").lower()[-6:]
    
    @property
    def name(self) -> str | None:
        return self._model + " - " + self.device_id
    
    @property
    def mac_address(self) -> str | None:
        return self._mac_address
    
    @property
    def model(self) -> str | None:
        return self._model
    
    @property
    def fw_ver(self) -> str | None:
        return self._fw_ver
    
    @property
    def binary_sensors(self) -> dict[str, CCLSensor] | None:
        return self._binary_sensors
    
    @property
    def sensors(self) -> dict[str, CCLSensor] | None:
        return self._sensors
    
    def update_info(self, info: dict[str, None | str]) -> None:
        """Add or update device info."""
        self._mac_address = info.get('mac_address')
        self._model = info.get('model')
        self._fw_ver = info.get('fw_ver')
    
    def update_sensors(self, sensors: dict[str, None | str | int | float]) -> None:
        """Add or update all sensor values."""
        for key, value in sensors.items():
            if CCL_SENSORS.get(key).binary:
                if not key in self._binary_sensors:
                    self._binary_sensors[key] = CCLSensor(key)
                    self._new_sensors.append(self._binary_sensors[key])
                self._binary_sensors[key].value = value
            else:
                if not key in self._sensors:
                    self._sensors[key] = CCLSensor(key)
                    self._new_sensors.append(self._sensors[key])
                self._sensors[key].value = value
        self._publish_new_sensors()
        self._publish_updates()
        self._last_updated_time = time.monotonic()
        _LOGGER.debug("Sensors Updated: %s", self._last_updated_time)

    def register_update_cb(self, callback: Callable[[], None]) -> None:
        """Register callback, called when Sensor changes state."""
        self._update_callbacks.add(callback)

    def remove_update_cb(self, callback: Callable[[], None]) -> None:
        """Remove previously registered callback."""
        self._update_callbacks.discard(callback)

    def _publish_updates(self) -> None:
        """Schedule call all registered callbacks."""
        try:
            for callback in self._update_callbacks:
                callback()
        except Exception as err:
            _LOGGER.warning("Error while publishing sensor updates: %s", err)

    def register_new_binary_sensor_cb(self, callback: Callable[[], None]) -> None:
        """Register callback, called when Sensor changes state."""
        self._new_binary_sensor_callbacks.add(callback)

    def remove_new_binary_sensor_cb(self, callback: Callable[[], None]) -> None:
        """Remove previously registered callback."""
        self._new_binary_sensor_callbacks.discard(callback)

    def register_new_sensor_cb(self, callback: Callable[[], None]) -> None:
        """Register callback, called when Sensor changes state."""
        self._new_sensor_callbacks.add(callback)

    def remove_new_sensor_cb(self, callback: Callable[[], None]) -> None:
        """Remove previously registered callback."""
        self._new_sensor_callbacks.discard(callback)

    def _publish_new_sensors(self) -> None:
        """Schedule call all registered callbacks."""
        for sensor in self._new_sensors[:]:
            try:
                _LOGGER.debug("Publishing new sensor: %s", sensor)
                if sensor.binary:
                    for callback in self._new_binary_sensor_callbacks:
                        callback(sensor)
                else:
                    for callback in self._new_sensor_callbacks:
                        callback(sensor)
                self._new_sensors.remove(sensor)
            except Exception as err:
                _LOGGER.warning("Error while publishing new sensors: %s", err)