import base64
from datetime import datetime
import unittest
from unittest.mock import MagicMock

from esdl.esdl_handler import EnergySystemHandler
from esdl import EnergySystem
import helics as h

from dots_infrastructure import CalculationServiceHelperFunctions
from dots_infrastructure.DataClasses import EsdlId, HelicsCalculationInformation, PublicationDescription, SimulatorConfiguration, SubscriptionDescription, TimeStepInformation
from dots_infrastructure.EsdlHelper import EsdlHelper
from dots_infrastructure.HelicsFederateHelpers import HelicsSimulationExecutor
from dots_infrastructure.test_infra.InfluxDBMock import InfluxDBMock

def simulator_environment_e_connection():
    return SimulatorConfiguration("EConnection", ["f006d594-0743-4de5-a589-a6c2350898da"], "Mock-Econnection", "127.0.0.1", 2000, "test-id", 900, datetime(2024,1,1), "test-host", "test-port", "test-username", "test-password", "test-database-name", h.HelicsLogLevel.DEBUG, ["PVInstallation", "EConnection"])

class CalculationServiceEConnection(HelicsSimulationExecutor):

    def __init__(self):
        CalculationServiceHelperFunctions.get_simulator_configuration_from_environment = simulator_environment_e_connection
        super().__init__()

        subscriptions_values = [
            SubscriptionDescription("PVInstallation", "PV_Dispatch", "W", h.HelicsDataType.DOUBLE)
        ]

        e_connection_period_in_seconds = 60

        calculation_information = HelicsCalculationInformation(time_period_in_seconds=e_connection_period_in_seconds, 
                                                               offset=0, 
                                                               wait_for_current_time_update=False, 
                                                               uninterruptible=False, 
                                                               terminate_on_error=True, 
                                                               calculation_name="EConnectionDispatch", 
                                                               inputs=subscriptions_values, 
                                                               outputs=None, 
                                                               calculation_function=self.e_connection_dispatch)
        self.add_calculation(calculation_information)

        publication_values = [
            PublicationDescription(True, "EConnection", "Schedule", "W", h.HelicsDataType.VECTOR)
        ]

        e_connection_period_scedule_in_seconds = 120

        calculation_information_schedule = HelicsCalculationInformation(time_period_in_seconds=e_connection_period_scedule_in_seconds,
                                                                        offset=0, 
                                                                        wait_for_current_time_update=False, 
                                                                        uninterruptible=False, 
                                                                        terminate_on_error=True, 
                                                                        calculation_name="EConnectionSchedule", 
                                                                        inputs=None, 
                                                                        outputs=publication_values, 
                                                                        calculation_function=self.e_connection_da_schedule)
        self.add_calculation(calculation_information_schedule)

    def e_connection_dispatch(self, param_dict : dict, simulation_time : datetime, time_step_number : TimeStepInformation, esdl_id : EsdlId, energy_system : EnergySystem):

        return 0
    
    def e_connection_da_schedule(self, param_dict : dict, simulation_time : datetime, time_step_number : TimeStepInformation, esdl_id : EsdlId, energy_system : EnergySystem):
        return [1.0,2.0,3.0]

class TestLogicAddingCalculations(unittest.TestCase):
    def test_simulation_none_input_output_sets_empty_inputs_and_outputs(self):

        # Execute
        cs_econnection = CalculationServiceEConnection()

        # Assert
        self.assertEqual(len(cs_econnection.calculations), 2)
        self.assertEqual(len(cs_econnection.calculations[0].helics_value_federate_info.inputs), 1)
        self.assertEqual(len(cs_econnection.calculations[0].helics_value_federate_info.outputs), 0)
        self.assertEqual(len(cs_econnection.calculations[1].helics_value_federate_info.inputs), 0)
        self.assertEqual(len(cs_econnection.calculations[1].helics_value_federate_info.outputs), 1)

if __name__ == '__main__':
    unittest.main()