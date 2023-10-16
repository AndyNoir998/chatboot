from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from typing import Any, Text, Dict, List
import re

class ActionCapturePlaca(Action):
    def name(self) -> Text:
        return "action_capture_placa"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        placa = next(tracker.get_latest_entity_values("placa"), None)

        if not placa:
            # Si no se detectó la entidad "placa" directamente, intenta buscarla en el mensaje del usuario
            message_text = tracker.latest_message.get("text")
            if message_text:
                # Aquí puedes usar expresiones regulares o lógica personalizada para extraer la placa
                # Por ejemplo, si la placa siempre está en un formato de ABC123, puedes hacer:
                placa_match = re.search(r'[A-Z]{3}\d{3}', message_text)
                if placa_match:
                    placa = placa_match.group()

        if placa:
            return [SlotSet("placa", placa)]
        else:
            dispatcher.utter_message("No se proporcionó una placa válida.")
            return [SlotSet("placa", None)]
        
class ActionConsultarMultas(Action):
    def name(self) -> Text:
        return "action_consultar_multas"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Datos simulados de multas (puede ser una lista de multas)
        multas = ["Multa de velocidad excesiva", "Multa por estacionamiento en lugar prohibido", "Multa por semáforo en rojo"]

        # Puedes acceder a las entidades capturadas desde el tracker
        placa = tracker.get_slot("placa")

        if placa:
            mensaje = f"Multas para la placa {placa}:\n{', '.join(multas)}"
        else:
            mensaje = "No se proporcionó una placa válida para la consulta de multas."

        dispatcher.utter_message(text=mensaje)

        return []

