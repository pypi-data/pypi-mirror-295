import json
import helics as h

from dots_infrastructure.Constants import Command

def terminate_requested_at_commands_endpoint(commands_message_endpoint : h.HelicsEndpoint):
    terminate_requested = False
    if h.helicsEndpointHasMessage(commands_message_endpoint):
        command = h.helicsMessageGetString(h.helicsEndpointGetMessage(commands_message_endpoint))
        if command == Command.TERMINATE:
            terminate_requested = True
    return terminate_requested

def terminate_simulation(federate : h.HelicsFederate, commands_message_endpoint : h.HelicsEndpoint):
    query = h.helicsCreateQuery("broker", "endpoint_details")
    endpoint_details_json = h.helicsQueryExecute(query, federate)
    endpoints_details = json.loads(str(endpoint_details_json).replace("'", '"'))
    termination_message = h.helicsEndpointCreateMessage(commands_message_endpoint)
    h.helicsMessageSetString(termination_message, "0")
    for endpoint in endpoints_details["endpoints"]:
        endpoint_name = str(endpoint["name"])
        if endpoint_name.endswith("commands"):
            h.helicsMessageSetDestination(termination_message, endpoint_name)
            h.helicsEndpointSendMessage(commands_message_endpoint, termination_message)

def destroy_federate(fed):
    h.helicsFederateDisconnect(fed)
    h.helicsFederateDestroy(fed)