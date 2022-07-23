
from actions.iot import hue_lightoff, hue_lightup
from actions.misc import apologize
from .misc import create_logger


logger = create_logger('Controller', 'homeio.log')

actions = {
    "iot": {
        "hue_lightoff": hue_lightoff,
        "hue_lightup": hue_lightup,
    },
    "timer": None,
    "sensor": None
}


class Controller:
    def __init__(self):
        logger.info('Controller Initialized')

    def parse(self, command):
        try:
            scenario = command['scenario']['class']
            intent = command['intent']['class']
            entities = command['entities']
            logger.info('Scenario: {} Intent: {}'.format(scenario, intent))
            action = actions[scenario][intent]
            action(entities)
        except:
            logger.error('Error in parsing command')
            apologize()
