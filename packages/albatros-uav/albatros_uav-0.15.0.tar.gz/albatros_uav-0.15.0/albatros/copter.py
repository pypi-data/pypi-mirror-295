import logging
import math
import time
from typing import Literal, Optional, overload

from pymavlink.dialects.v20.ardupilotmega import (
    MAV_CMD_CONDITION_YAW,
    MAV_CMD_DO_SET_MODE,
    MAV_CMD_NAV_LAND,
    MAV_CMD_NAV_TAKEOFF,
    MAVLINK_MSG_ID_POSITION_TARGET_LOCAL_NED,
    MAVLink_landing_target_message,
)

from albatros.enums import (
    CommandResult,
    ConnectionType,
    CopterFlightModes,
    Direction,
    LandingTargetType,
    MavFrame,
)
from albatros.nav.position import PositionGPS, convert_raw_path_to_gps
from albatros.telem import ComponentAddress
from albatros.telem.message_models import PositionTargetLocalNED
from albatros.uav import UAV

from .outgoing.commands import (
    get_command_long_message,
    get_mission_item_int,
    get_set_position_target_local_ned_message,
)

logger = logging.getLogger(__name__)


def get_current_time_us() -> int:
    """Get epoch time in microseconds."""
    return int(time.time() * 1e6)


class Copter(UAV):
    """Provides copter specific actions."""

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

    def get_flight_mode(self) -> CopterFlightModes:
        """Get flight mode."""
        if self.data.heartbeat.less_than(time_ms=2_000):
            return CopterFlightModes(self.data.heartbeat.custom_mode)
        return CopterFlightModes.UNKNOWN

    def set_mode(self, mode: CopterFlightModes) -> bool:
        """Set system mode.

        Parameters:
            mode: ardupilot flight mode you want to set.

        Returns:
            `True` if command was accepted
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

    def takeoff(self, alt_m: float, yaw: float = float("NaN")) -> bool:
        """Takeoff copter. Set `GUIDED` mode and send takeoff command.

        Parameters:
            alt_m: The altitude to which the Copter is to ascend
            yaw: Yaw angle (if magnetometer present), ignored without magnetometer.
                NaN to use the current system yaw heading mode (e.g. yaw towards next waypoint,
                yaw to home, etc.).

        Returns:
            `True` if command was accepted
        """
        msg = get_command_long_message(
            self._uav_addr.system_id,
            self._uav_addr.component_id,
            MAV_CMD_NAV_TAKEOFF,
            param4=yaw,
            param7=alt_m,
        )

        self._driver.send(msg)
        logger.info("Takeoff command sent")

        try:
            return self.wait_command_ack().result == CommandResult.ACCEPTED
        except TimeoutError:
            return False

    def land(self) -> bool:
        """Land copter in the place where it is currently located. Works only in `GUIDED` mode.

        Returns:
            `True` if command was accepted
        """

        msg = get_command_long_message(
            self._uav_addr.system_id,
            self._uav_addr.component_id,
            MAV_CMD_NAV_LAND,
        )

        self._driver.send(msg)
        logger.info("Land command sent")

        try:
            return self.wait_command_ack().result == CommandResult.ACCEPTED
        except TimeoutError:
            return False

    def set_yaw(
        self,
        yaw_deg: float,
        angular_speed: float,
        direction: Direction = Direction.SHORTEST,
        relative: bool = False,
    ) -> bool:
        """Set yaw angle.

        Parameters:
            yaw_deg: `0` is north for absolute angle and initial yaw for relative angle
            angular_speed: rotation speed in deg/s
            direction: rotation direction
            relative: `True` for relative, `False` for absolute

        Returns:
            `True` if command was accepted
        """
        msg = get_command_long_message(
            target_system=self._uav_addr.system_id,
            target_component=self._uav_addr.component_id,
            command=MAV_CMD_CONDITION_YAW,
            param1=yaw_deg,
            param2=angular_speed,
            param3=direction.value,
            param4=relative,
        )

        self._driver.send(msg)
        logger.info("Set yaw command sent")

        try:
            return self.wait_command_ack().result == CommandResult.ACCEPTED
        except TimeoutError:
            return False

    def fly_to_local_position(
        self,
        north_m: float,
        east_m: float,
        alt_m: float,
        yaw_rad: float = 0,
        yaw_rate_rad: float = 0,
    ) -> bool:
        """Move copter to the NED location relative to origin of the coordinate system.

        Works only in `GUIDED` mode.

        Parameters:
            north_m: meters to the north,
            east_m: meters to the east,
            alt_m: altitude in meters relative to start point.
            yaw_rad: yaw setpoint (rad)
            yaw_rate_rad: yaw rate setpoint (rad/s)

        Returns:
            `True` if command was accepted
        """

        msg = get_set_position_target_local_ned_message(
            self._uav_addr.system_id,
            self._uav_addr.component_id,
            north_m,
            east_m,
            alt_m,
            yaw_rad,
            yaw_rate_rad,
            MavFrame.LOCAL_NED,
        )

        self._driver.send(msg)
        logger.info("Flight to point command sent.")

        try:
            if (
                self.request_message(MAVLINK_MSG_ID_POSITION_TARGET_LOCAL_NED)
                != CommandResult.ACCEPTED
            ):
                return False

            target = self.wait_message(PositionTargetLocalNED())
            if target.x == north_m and target.y == east_m:
                return True
            return False

        except TimeoutError:
            return False

    def fly_to_local_offset_position(
        self,
        north_m: float,
        east_m: float,
        relative_alt_m: float,
        yaw_rad: float = 0,
        yaw_rate_rad: float = 0,
    ) -> bool:
        """Move copter to the NED location relative to the current position.

        Works only in `GUIDED` mode.

        Parameters:
            north_m: meters to the north,
            east_m: meters to the east,
            relative_alt_m: altitude in meters relative to current altitude.
            yaw_rad: yaw setpoint (rad)
            yaw_rate_rad: yaw rate setpoint (rad/s)

        Returns:
            `True` if command was accepted
        """

        msg = get_set_position_target_local_ned_message(
            self._uav_addr.system_id,
            self._uav_addr.component_id,
            north_m,
            east_m,
            relative_alt_m,
            yaw_rad,
            yaw_rate_rad,
            MavFrame.LOCAL_OFFSET_NED,
        )

        self._driver.send(msg)
        logger.info("Flight to point command sent.")

        try:
            if (
                self.request_message(MAVLINK_MSG_ID_POSITION_TARGET_LOCAL_NED)
                != CommandResult.ACCEPTED
            ):
                return False

            target = self.wait_message(PositionTargetLocalNED())
            if target.x == north_m and target.y == east_m:
                return True
            return False

        except TimeoutError:
            return False

    def fly_along_path_raw(
        self,
        raw_path: list[tuple[float, float, float]],
        precision: float = 1.0,
    ) -> None:
        """This function will fly the copter along the given path of GPS positions.
        The point is reached when the distance to the target is less than the precision.

        Parameters:
            raw_path: list of (lat, lon, alt) points to fly to in provided order.
            precision: Minimal distance between copter and target to consider
                the target as visited.  Defaults to 1.0.
        """
        flight_path = convert_raw_path_to_gps(raw_path)
        self.fly_along_path(flight_path, precision)

    def fly_along_path(
        self, flight_path: list[PositionGPS], precision: float = 1.0
    ) -> None:
        """This function will fly the copter along the given path of GPS positions.
        The point is reached when the distance to the target is less than the precision.

        Parameters:
            flight_path: list of PositionGPS points to fly to in provided order.
            precision: Minimal distance between copter and target to consider the
                target as visited. Defaults to 1.0.
        """
        for target in flight_path:
            self.fly_to_gps_position(target.lat, target.lon, target.alt_m)
            while (
                distance := target.distance_to_point(self.get_corrected_position())
            ) > precision:
                logger.debug("distance to next point: %f", distance)
                time.sleep(1)
        self.set_mode(CopterFlightModes.RTL)

    @overload
    def send_landing_target(
        self,
        distance_m: float,
        _type: LandingTargetType,
        angle_x_deg: float,
        angle_y_deg: float,
        size_x_deg: float,
        size_y_deg: float,
        x: Literal[None] = None,
        y: Literal[None] = None,
        z: Literal[None] = None,
        q: Literal[None] = None,
        target_num: int = 0,
    ) -> None: ...

    @overload
    def send_landing_target(
        self,
        distance_m: float,
        _type: LandingTargetType,
        angle_x_deg: Literal[None] = None,
        angle_y_deg: Literal[None] = None,
        size_x_deg: Literal[None] = None,
        size_y_deg: Literal[None] = None,
        x: float = ...,
        y: float = ...,
        z: float = ...,
        q: tuple[float, float, float, float] = ...,
        target_num: int = 0,
    ) -> None: ...

    def send_landing_target(
        self,
        distance_m: float,
        _type: LandingTargetType,
        angle_x_deg: Optional[float] = None,
        angle_y_deg: Optional[float] = None,
        size_x_deg: Optional[float] = None,
        size_y_deg: Optional[float] = None,
        x: Optional[float] = None,
        y: Optional[float] = None,
        z: Optional[float] = None,
        q: Optional[tuple[float, float, float, float]] = None,
        target_num: int = 0,
    ) -> None:
        """Send the location of a landing target."""
        if angle_x_deg and angle_y_deg and size_x_deg and size_y_deg:
            msg = MAVLink_landing_target_message(
                time_usec=get_current_time_us(),
                target_num=target_num,
                frame=MavFrame.BODY_FRD.value,
                angle_x=math.radians(angle_x_deg),
                angle_y=math.radians(angle_y_deg),
                distance=distance_m,
                size_x=math.radians(size_x_deg),
                size_y=math.radians(size_y_deg),
                x=0,
                y=0,
                z=0,
                q=(0.0, 0.0, 0.0, 0.0),
                type=_type,
                position_valid=0,
            )
        elif x and y and z and q:
            msg = MAVLink_landing_target_message(
                time_usec=get_current_time_us(),
                target_num=target_num,
                frame=MavFrame.BODY_FRD.value,  # ArduPilot supports this form of positioning.
                angle_x=0,
                angle_y=0,
                distance=distance_m,
                size_x=0,
                size_y=0,
                x=x,
                y=y,
                z=z,
                q=q,
                type=_type,
                position_valid=1,
            )
        else:
            raise NotImplementedError

        self._driver.send(msg)

    def send_mission_takeoff_item(
        self,
        altitude: float,
        yaw: float = float("NaN"),
    ) -> None:
        """Send takeoff item.

        Parameters:
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
            param4=yaw,
            z=altitude,
        )

        self._driver.send(msg)
        logger.info("mission_takeoff message sent.")
