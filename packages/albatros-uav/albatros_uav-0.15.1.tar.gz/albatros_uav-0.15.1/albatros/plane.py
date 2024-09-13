import logging
from typing import Optional

from pymavlink.dialects.v20.ardupilotmega import (
    MAV_CMD_DO_SET_MODE,
    MAV_CMD_NAV_LOITER_TIME,
    MAV_CMD_NAV_LOITER_UNLIM,
    MAV_CMD_NAV_TAKEOFF,
)

from albatros.enums import ConnectionType
from albatros.telem import ComponentAddress

from .enums import CommandResult, PlaneFlightModes
from .nav.position import PositionGPS
from .outgoing.commands import get_command_long_message, get_mission_item_int
from .uav import UAV

logger = logging.getLogger(__name__)


class Plane(UAV):
    """Class that provides actions the plane can perform."""

    def __init__(
        self,
        uav_addr: ComponentAddress = ComponentAddress(system_id=1, component_id=1),
        my_addr: ComponentAddress = ComponentAddress(system_id=1, component_id=191),
        connection_type: ConnectionType = ConnectionType.DIRECT,
        device: Optional[str] = "udpin:0.0.0.0:14550",
        baud_rate: Optional[int] = 115200,
        host: Optional[str] = None,
        port: Optional[int] = None,
    ) -> None:
        super().__init__(
            uav_addr,
            my_addr,
            connection_type,
            device,
            baud_rate,
            host,
            port,
        )

    def get_flight_mode(self) -> PlaneFlightModes:
        """Get flight mode."""
        if self.data.heartbeat.less_than(time_ms=2_000):
            return PlaneFlightModes(self.data.heartbeat.custom_mode)
        return PlaneFlightModes.UNKNOWN

    def set_mode(self, mode: PlaneFlightModes) -> bool:
        """Set flight mode.

        Parameters:
            mode: ardupilot flight mode you want to set.
        """
        msg = get_command_long_message(
            target_system=self._uav_addr.system_id,
            target_component=self._uav_addr.component_id,
            command=MAV_CMD_DO_SET_MODE,
            param1=1,
            param2=mode.value,
        )

        self._driver.send(msg)
        logger.info("Set mode command sent")

        try:
            return self.wait_command_ack().result == CommandResult.ACCEPTED
        except TimeoutError:
            return False

    def send_mission_takeoff_item(
        self,
        pitch: float,
        altitude: float,
        yaw: float = float("NaN"),
    ) -> None:
        """Send takeoff item.

        Parameters:
            pitch: Minimum pitch (if airspeed sensor present), desired pitch without sensor.
            yaw: Yaw angle (if magnetometer present), ignored without magnetometer.
                NaN to use the current system yaw heading mode (e.g. yaw towards next waypoint, yaw to home, etc.).
            altitude: target altitude in meters
        """
        seq = self.wait_next_mission_item_id()

        msg = get_mission_item_int(
            target_system=self._uav_addr.system_id,
            target_component=self._uav_addr.component_id,
            seq=seq,
            command=MAV_CMD_NAV_TAKEOFF,
            param1=pitch,
            param4=yaw,
            z=altitude,
        )

        self._driver.send(msg)
        logger.info("mission_takeoff message sent.")

    def send_mission_loiter_unlim_item(
        self,
        lat: float,
        lon: float,
        alt_m: float,
        radius_m: float,
        yaw_deg: float = 0,
    ) -> None:
        """Loiter around this waypoint an unlimited amount of time

        Parameters:
            lat: Latitude.
            lon: Longitude.
            alt_m: Altitude in meters.
            radius_m: Loiter radius around waypoint for forward-only moving vehicles (not multicopters).
                If positive loiter clockwise, else counter-clockwise
            yaw_deg: Desired yaw angle at the waypoint for rotary-wing vehicles.
                Set to NaN to use the current system yaw heading mode. Defaults to None.
        """
        seq = self.wait_next_mission_item_id()

        wp = PositionGPS(lat, lon, alt_m)
        msg = get_mission_item_int(
            target_system=self._uav_addr.system_id,
            target_component=self._uav_addr.component_id,
            seq=seq,
            command=MAV_CMD_NAV_LOITER_UNLIM,
            param3=radius_m,
            param4=yaw_deg,
            x=wp.lat_int,
            y=wp.lon_int,
            z=wp.alt_m,
        )

        self._driver.send(msg)
        logger.info("mission_loiter_unlim message sent.")

    def send_mission_loiter_time_item(
        self,
        time_s: float,
        lat: float,
        lon: float,
        alt_m: float,
        radius_m: float,
        straight_to_wp: bool = True,
    ) -> None:
        """Loiter around this waypoint an unlimited amount of time

        Parameters:
            time_s: Loiter time in seconds.
            lat: Latitude.
            lon: Longitude.
            alt_m: Altitude in meters.
            radius_m: Loiter radius around waypoint for forward-only moving vehicles (not multicopters).
                If positive loiter clockwise, else counter-clockwise.
            straight_to_wp: Quit the loiter while on the straight to the next waypoint.
        """
        seq = self.wait_next_mission_item_id()

        wp = PositionGPS(lat, lon, alt_m)
        msg = get_mission_item_int(
            target_system=self._uav_addr.system_id,
            target_component=self._uav_addr.component_id,
            seq=seq,
            command=MAV_CMD_NAV_LOITER_TIME,
            param1=time_s,
            param2=0,
            param3=radius_m,
            param4=straight_to_wp,
            x=wp.lat_int,
            y=wp.lon_int,
            z=wp.alt_m,
        )

        self._driver.send(msg)
        logger.info("mission_loiter_time message sent.")
