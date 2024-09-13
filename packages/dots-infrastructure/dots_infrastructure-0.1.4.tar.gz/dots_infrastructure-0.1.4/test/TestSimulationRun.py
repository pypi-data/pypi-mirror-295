import base64
from datetime import datetime
import random
from threading import Thread
import unittest
import helics as h

from unittest.mock import MagicMock

from dots_infrastructure import CalculationServiceHelperFunctions
from dots_infrastructure.DataClasses import EsdlId, HelicsCalculationInformation, PublicationDescription, SimulatorConfiguration, SubscriptionDescription, TimeStepInformation
from dots_infrastructure.EsdlHelper import EsdlHelper
from dots_infrastructure.HelicsFederateHelpers import HelicsSimulationExecutor
from dots_infrastructure.Logger import LOGGER
from dots_infrastructure.test_infra.InfluxDBMock import InfluxDBMock
from esdl.esdl import EnergySystem

BROKER_TEST_PORT = 23404
START_DATE_TIME = datetime(2024, 1, 1, 0, 0, 0)
SIMULATION_DURATION_IN_SECONDS = 960

with open("test.esdl", mode="r") as esdl_file:
    encoded_base64_esdl = base64.b64encode(esdl_file.read().encode('utf-8')).decode('utf-8')

HelicsSimulationExecutor._get_esdl_from_so = MagicMock(return_value=EsdlHelper(encoded_base64_esdl))

MS_TO_BROKER_DISCONNECT = 60000

def start_helics_broker(federates):
    broker = h.helicsCreateBroker("zmq", "helics_broker_test", f"-f {federates} --loglevel=debug --timeout='60s'")
    broker.wait_for_disconnect(MS_TO_BROKER_DISCONNECT)

def simulator_environment_e_pv():
    return SimulatorConfiguration("PVInstallation", ['176af591-6d9d-4751-bb0f-fac7e99b1c3d','b8766109-5328-416f-9991-e81a5cada8a6'], "Mock-PV", "127.0.0.1", BROKER_TEST_PORT, "test-id", SIMULATION_DURATION_IN_SECONDS, START_DATE_TIME, "test-host", "test-port", "test-username", "test-password", "test-database-name", h.HelicsLogLevel.DEBUG, ["PVInstallation", "EConnection"])

class CalculationServicePVDispatch(HelicsSimulationExecutor):

    def __init__(self):
        CalculationServiceHelperFunctions.get_simulator_configuration_from_environment = simulator_environment_e_pv
        super().__init__()
        self.influx_connector = InfluxDBMock()
        publictations_values = [
            PublicationDescription(True, "PVInstallation", "PV_Dispatch", "W", h.HelicsDataType.DOUBLE)
        ]
        subscriptions_values = []
        self.i = 0

        pv_installation_period_in_seconds = 30
        info = HelicsCalculationInformation(pv_installation_period_in_seconds, 0, False, False, True, "pvdispatch_calculation", subscriptions_values, publictations_values, self.pvdispatch_calculation)
        self.add_calculation(info)


    def pvdispatch_calculation(self, param_dict : dict, simulation_time : datetime, time_step_number : int, esdl_id : EsdlId, energy_system : EnergySystem):
        ret_val = {}
        LOGGER.info(f"Executing pvdispatch_calculation")
        ret_val["PV_Dispatch"] = self.i
        self.i += 1
        self.influx_connector.set_time_step_data_point(esdl_id, "PV_Dispatch", simulation_time, ret_val["PV_Dispatch"])
        return ret_val

def simulator_environment_e_connection():
    return SimulatorConfiguration("EConnection", ["f006d594-0743-4de5-a589-a6c2350898da"], "Mock-Econnection", "127.0.0.1", BROKER_TEST_PORT, "test-id", SIMULATION_DURATION_IN_SECONDS, START_DATE_TIME, "test-host", "test-port", "test-username", "test-password", "test-database-name", h.HelicsLogLevel.DEBUG, ["PVInstallation", "EConnection"])

class CalculationServiceEConnection(HelicsSimulationExecutor):

    def __init__(self):
        CalculationServiceHelperFunctions.get_simulator_configuration_from_environment = simulator_environment_e_connection
        super().__init__()
        self.influx_connector = InfluxDBMock()
        self.calculation_service_initialized = False

        subscriptions_values = [
            SubscriptionDescription("PVInstallation", "PV_Dispatch", "W", h.HelicsDataType.DOUBLE)
        ]

        publication_values = [
            PublicationDescription(True, "EConnection", "EConnectionDispatch", "W", h.HelicsDataType.DOUBLE)
        ]

        e_connection_period_in_seconds = 60

        calculation_information = HelicsCalculationInformation(e_connection_period_in_seconds, 0, False, False, True, "EConnectionDispatch", subscriptions_values, publication_values, self.e_connection_dispatch)
        self.add_calculation(calculation_information)

        publication_values = [
            PublicationDescription(True, "EConnection", "Schedule", "W", h.HelicsDataType.VECTOR)
        ]

        e_connection_period_scedule_in_seconds = 120

        calculation_information_schedule = HelicsCalculationInformation(e_connection_period_scedule_in_seconds, 0, False, False, True, "EConnectionSchedule", [], publication_values, self.e_connection_da_schedule)
        self.add_calculation(calculation_information_schedule)

    def init_calculation_service(self, energy_system: EnergySystem):
        self.calculation_service_initialized = True
        LOGGER.info("init calculation service")

    def e_connection_dispatch(self, param_dict : dict, simulation_time : datetime, time_step_number : TimeStepInformation, esdl_id : EsdlId, energy_system : EnergySystem):
        pv_dispatch = CalculationServiceHelperFunctions.get_single_param_with_name(param_dict, "PV_Dispatch")
        ret_val = {}
        LOGGER.info(f"Executing e_connection_dispatch with pv dispatch value {pv_dispatch}")
        ret_val["EConnectionDispatch"] = pv_dispatch * random.randint(1,3)
        self.influx_connector.set_time_step_data_point(esdl_id, "EConnectionDispatch", simulation_time, ret_val["EConnectionDispatch"])
        return ret_val
    
    def e_connection_da_schedule(self, param_dict : dict, simulation_time : datetime, time_step_number : TimeStepInformation, esdl_id : EsdlId, energy_system : EnergySystem):
        ret_val = {}
        ret_val["Schedule"] = [1.0,2.0,3.0]
        LOGGER.info(f"Executing e_connection_da_schedule")
        self.influx_connector.set_time_step_data_point(esdl_id, "DAScedule", simulation_time, ret_val["Schedule"])
        return ret_val

class CalculationServiceEConnectionException(HelicsSimulationExecutor):

    def __init__(self):
        CalculationServiceHelperFunctions.get_simulator_configuration_from_environment = simulator_environment_e_connection
        super().__init__()
        self.influx_connector = InfluxDBMock()

        subscriptions_values = [
            SubscriptionDescription("PVInstallation", "PV_Dispatch", "W", h.HelicsDataType.DOUBLE)
        ]

        publication_values = [
            PublicationDescription(True, "EConnection", "EConnectionDispatch", "W", h.HelicsDataType.DOUBLE)
        ]

        e_connection_period_in_seconds = 60

        calculation_information = HelicsCalculationInformation(e_connection_period_in_seconds, 0, False, False, True, "EConnectionDispatch", subscriptions_values, publication_values, self.e_connection_dispatch)
        self.add_calculation(calculation_information)

    def e_connection_dispatch(self, param_dict : dict, simulation_time : datetime, time_step_number : TimeStepInformation, esdl_id : EsdlId, energy_system : EnergySystem):
        Exception("Test-exception")

class TestSimulation(unittest.TestCase):

    def start_broker(self, n_federates):
        self.broker_thread = Thread(target = start_helics_broker, args = (n_federates, ))
        self.broker_thread .start()

    def stop_broker(self):
        self.broker_thread.join()

    def test_simulation_run_starts_correctly(self):
        # Arrange 
        self.start_broker(3)

        e_connection_dispatch_period_in_seconds = 60
        e_connection_period_scedule_in_seconds = 120
        pv_period = 30

        # Execute
        cs_econnection = CalculationServiceEConnection()
        cs_dispatch = CalculationServicePVDispatch()

        cs_econnection.start_simulation()
        cs_dispatch.start_simulation()
        cs_econnection.stop_simulation()
        cs_dispatch.stop_simulation()
        self.stop_broker()

        # Assert
        self.assertEqual(len(cs_econnection.influx_connector.data_points), SIMULATION_DURATION_IN_SECONDS / e_connection_dispatch_period_in_seconds + SIMULATION_DURATION_IN_SECONDS / e_connection_period_scedule_in_seconds)
        self.assertEqual(len(cs_dispatch.influx_connector.data_points), SIMULATION_DURATION_IN_SECONDS / pv_period * 2)
        self.assertTrue(cs_econnection.calculation_service_initialized)

    def test_simulation_run_stops_upon_exception(self):
        # Arrange 
        self.start_broker(2)
        e_connection_dispatch_period_in_seconds = 60
        pv_period = 30

        # Execute
        cs_econnection = CalculationServiceEConnectionException()
        cs_dispatch = CalculationServicePVDispatch()

        cs_econnection.start_simulation()
        cs_dispatch.start_simulation()
        cs_econnection.stop_simulation()
        cs_dispatch.stop_simulation()
        self.stop_broker()

        # Assert
        # No data should be generated as exception is generated right away
        self.assertEqual(len(cs_econnection.influx_connector.data_points), 0) 
        # 2 pv panels produce data at most 3 times so
        self.assertLessEqual(len(cs_econnection.influx_connector.data_points), 2 * e_connection_dispatch_period_in_seconds / pv_period + 1)


if __name__ == '__main__':
    unittest.main()