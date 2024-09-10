from typing import List

from dash import Dash, Input, Output
from dash.development.base_component import Component
from .GetAPIKey import GetAPIKey

class ApiKey:
    def __init__(self, id: str = 'po-api-key'):
        self.id = id

    @property
    def component(self):
        return GetAPIKey(id=self.id)
    
    def create_api_key_callback(self, app: Dash, component_ids: List[str]):
        input = Input(component_id='po-api-key', component_property='apiKey')
        outputs = [Output(component_id=component_id, component_property='apiKey') for component_id in component_ids]

        def callback(apiKey):
            return [apiKey for _ in range(len(outputs))]
        
        app.callback(outputs, input)(callback)

    def inject_components(self, app: Dash, components: List[Component]):
        self.create_api_key_callback(app=app, component_ids=[c.id for c in components])