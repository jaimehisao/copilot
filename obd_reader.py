import time
import psycopg2
import obd


def get_speed(connection):
    """
    Queries the OBD sensor for the car´s speed.
    :param connection: OBD Sensor connection object
    :return: Returns the speed of the car
    """
    response = connection.query(obd.commands.SPEED)
    return (
        response.value.magnitude
    )  # TODO might need to extract only the number from this


def get_rpm(connection):
    """
    Queries the OBD sensor for the engine´s RPM.
    :param connection: OBD Sensor connection object
    :return: Returns the RPM of the car´s engine.
    """
    response = connection.query(obd.commands.RPM)
    return (
        response.value.magnitude
    )  # TODO might need to extract only the number from this


def get_coolant_temp(connection):
    """
    Queries the OBD sensor for Coolant Temperature
    :param connection: OBD Sensor connection object
    :return: Engine load percentage
    """
    response = connection.query(obd.commands.COOLANT_TEMP)
    return (
        response.value.magnitude
    )  # TODO might need to extract only the number from this


def get_engine_load(connection):
    """
    Queries the OBD sensor for engine load percentage
    :param connection: OBD Sensor connection object
    :return: Engine load percentage
    """
    response = connection.query(obd.commands.ENGINE_LOAD)
    return (
        response.value.magnitude
    )  # TODO might need to extract only the number from this


def get_intake_temp(connection):
    """
    Queries the OBD sensor for the Air Intake Temperature
    :param connection: OBD Sensor connection object
    :return: Returns the intake temp in celsius
    """
    response = connection.query(obd.commands.INTAKE_TEMP)
    return (
        response.value.magnitude
    )  # TODO might need to extract only the number from this


def get_throttle_position(connection):
    """
    Queries the OBD sensor for the Throttle Position
    :param connection: OBD Sensor connection object
    :return: Throttle pedal percentage
    """
    response = connection.query(obd.commands.THROTTLE_POS)
    return (
        response.value.magnitude
    )  # TODO might need to extract only the number from this


def get_engine_run_time(connection):
    """
    Queries the OBD sensor for engine run time
    :param connection: OBD Sensor connection object
    :return Engine run time in seconds
    """
    response = connection.query(obd.commands.RUN_TIME)
    return (
        response.value.magnitude
    )  # TODO might need to extract only the number from this


conn = psycopg2.connect("dbname=driving user=pi")
cur = conn.cursor()
obd.logger.setLevel(obd.logging.DEBUG)

connected = False
connection = None
data = []
while not connected:
    connection = obd.OBD(fast=False, timeout=30)
    connected = connection.is_connected()

while connection.is_connected():
    try:
        curr_stat = {
            "rpm": get_rpm(connection),
            "speed": get_speed(connection),
            "coolant_temp": get_coolant_temp(connection),
            "engine_load": get_engine_load(connection),
            "get_engine_runtime": get_engine_run_time(connection),
            "intake_temp": get_intake_temp(connection),
            "throttle_position": get_throttle_position(connection),
        }
        data.append(curr_stat)
        cur.execute(
            "INSERT INTO driving_stats (timestamp, speed, rpm, coolant_temp, engine_load, engine_runtime, intake_temp, throttle_position) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (
                time.time(),
                get_speed(connection),
                get_rpm(connection),
                get_coolant_temp(connection),
                get_engine_load(connection),
                get_engine_run_time(connection),
                get_intake_temp(connection),
                get_throttle_position(connection),
            ),
        )
        time.sleep(5)
    except Exception:
        break


"""
def __init__():
    connection = None
    try:
        connection = obd.OBD(fast=False, timeout=30)  # Connects to the OBD adapter
        supported_variables = connection.supported_commands  # debug
        connection.supports(obd.commands.RUN_TIME)  # Checks if such command is supported by the car.
        # Could either retrieve all useful information or just the specific commands
        print(supported_variables)  # debug
    except Exception as e:
        print(e)
"""

# Make script to check if wifi is connected by asserting the hostname of the DB


# Maybe instead of doing a per-component query, do a query based on all of the available commands.
# Check if an acceptable message was recieved (response.value == None)
