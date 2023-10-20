from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from typing import Any, Text, Dict, List
import re
import random

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
            # Simulamos mostrar una o dos multas de manera aleatoria
            if random.random() < 0.5:
                # Mostrar una multa
                mensaje = f"Multas para la placa {placa}:\n{random.choice(multas)}"
            else:
                mensaje = f"No se encontraron multas para la placa {placa}."
        else:
            mensaje = "No se proporcionó una placa válida para la consulta de multas."

        dispatcher.utter_message(text=mensaje)

        return []

class ActionRespuestaPreguntaFrecuente(Action):
    def name(self) -> Text:
        return "action_respuesta_pregunta_frecuente"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: List[Text]) -> List[Dict[Text, Any]]:
        pregunta = tracker.latest_message.get("text")
        
        # Aquí puedes implementar la lógica para seleccionar la respuesta adecuada según la pregunta detectada.
        if "requisitos para renovar la licencia de conducir" in pregunta:
            dispatcher.utter_message("Los requisitos para renovar la licencia de conducir incluyen https://www.runt.gov.co. Puedes obtener más detalles en [sitio web].")
        elif "plazos para registrar un vehículo" in pregunta:
            dispatcher.utter_message("El plazo para registrar un vehículo es 60 dias apartir de la adquisición del mismo. Asegúrate de hacerlo a tiempo para evitar sanciones.")
        # Agrega más condiciones para otras preguntas frecuentes
        
        return []

class ActionSolicitarCita(Action):
    def name(self) -> Text:
        return "action_solicitar_cita"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Puedes proporcionar aquí detalles sobre cómo los usuarios pueden solicitar una cita, por ejemplo, un enlace al sitio web de citas del RUNT.
        mensaje = "Puedes solicitar una cita para visitar el RUNT a través de nuestro sitio web https://www.runt.gov.co. Simplemente selecciona la opción de programar cita e ingresa tus datos."
        dispatcher.utter_message(text=mensaje)

        return []
    