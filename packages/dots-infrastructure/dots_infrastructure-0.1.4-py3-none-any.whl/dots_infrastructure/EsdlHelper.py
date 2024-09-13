from base64 import b64decode
from typing import List
from esdl.esdl_handler import EnergySystemHandler

from esdl import esdl
from esdl import EnergySystem
from dots_infrastructure.DataClasses import CalculationServiceInput, EsdlId, SubscriptionDescription

class EsdlHelper:

    def __init__(self, esdl_string_base64):
        self.energy_system = self._get_energy_system_from_base64_encoded_esdl_string(esdl_string_base64)
        self.non_connected_esdl_ids = []
        self.esdl_object_mapping : dict = self._get_esdl_id_object_mapping(self.energy_system, self.non_connected_esdl_ids)

    def _get_energy_system_from_base64_encoded_esdl_string(self, esdl_string_base64) -> EnergySystem:
        esdl_string = b64decode(esdl_string_base64 + b"==".decode("utf-8")).decode("utf-8")
        esh = EnergySystemHandler()
        esh.load_from_string(esdl_string)
        return esh.get_energy_system()
    
    def _get_esdl_id_object_mapping(self, energy_system : EnergySystem, non_connected_esdl_ids : List) -> esdl:
        ret_val = {}
        for obj in energy_system.eAllContents():
            if hasattr(obj, "id"):
                ret_val[obj.id] = obj
                if not isinstance(obj, esdl.EnergyAsset):
                    non_connected_esdl_ids.append(obj.id)
        return ret_val
    
    def extract_calculation_service_name(self, calculation_services: List[str], esdl_obj) -> str:
        esdl_obj_type_name = type(esdl_obj).__name__
        name = next(
            (
                calc_service_name
                for calc_service_name in calculation_services
                if calc_service_name == esdl_obj_type_name
            ),
            None,
        )
        
        return name
    
    def add_connected_esdl_object(self, subscriptions: List[SubscriptionDescription], calculation_services: List[str], input_descriptions : List[SubscriptionDescription], connected_asset: esdl, simulator_asset: esdl.EnergyAsset):
        calc_service_name = self.extract_calculation_service_name(calculation_services, connected_asset)
    
        if calc_service_name:
            input_description = next((input_description for input_description in input_descriptions if input_description.esdl_type == calc_service_name), None)
            if input_description:
                subscriptions.append(CalculationServiceInput(input_description.esdl_type, input_description.input_name, connected_asset.id, input_description.input_unit, input_description.input_type, simulator_asset.id))
    
    def add_calc_services_from_ports(
        self,
        calculation_services: List[str],
        connected_input_esdl_objects: List[SubscriptionDescription],
        input_descriptions : List[SubscriptionDescription],
        model_esdl_asset: esdl.EnergyAsset,
    ):
        for port in model_esdl_asset.port:
            if isinstance(port, esdl.InPort):
                for connected_port in port.connectedTo:
                    connected_asset = connected_port.eContainer()
                    self.add_connected_esdl_object(
                        connected_input_esdl_objects, calculation_services, input_descriptions, connected_asset, model_esdl_asset
                    )
    
    def add_calc_services_from_non_connected_objects(
        self,
        calculation_services: List[str],
        connected_input_esdl_objects: List[SubscriptionDescription],
        input_descriptions : List[SubscriptionDescription],
        model_esdl_asset: esdl.EnergyAsset
    ):
        for esdl_id in self.non_connected_esdl_ids:
            self.add_connected_esdl_object(
                connected_input_esdl_objects, calculation_services, input_descriptions, self.esdl_object_mapping[esdl_id], model_esdl_asset
            )
        self.add_connected_esdl_object(connected_input_esdl_objects, calculation_services, input_descriptions, self.energy_system, model_esdl_asset)
    
    def add_calc_services_from_all_objects(
        self,
        calculation_services: List[str],
        connected_input_esdl_objects: List[SubscriptionDescription],
        input_descriptions : List[SubscriptionDescription],
        model_esdl_asset: esdl.EnergyAsset
    ):
        for esdl_obj in self.esdl_object_mapping.values():
            self.add_connected_esdl_object(
                connected_input_esdl_objects, calculation_services, input_descriptions, esdl_obj, model_esdl_asset
            )
    
    def get_connected_input_esdl_objects(
        self,
        esdl_id: EsdlId,
        calculation_services: List[str],
        input_descriptions : List[SubscriptionDescription]
    ) -> List[CalculationServiceInput]:
        model_esdl_obj = self.esdl_object_mapping[esdl_id]
    
        connected_input_esdl_objects: List[CalculationServiceInput] = []
        if isinstance(model_esdl_obj, esdl.EnergyAsset):
            self.add_calc_services_from_ports(
                calculation_services, connected_input_esdl_objects, input_descriptions, model_esdl_obj
            )
            self.add_calc_services_from_non_connected_objects(
                calculation_services, connected_input_esdl_objects, input_descriptions, model_esdl_obj
            )
        else:
            self.add_calc_services_from_all_objects(
                calculation_services, connected_input_esdl_objects, input_descriptions, model_esdl_obj
            )
        return connected_input_esdl_objects