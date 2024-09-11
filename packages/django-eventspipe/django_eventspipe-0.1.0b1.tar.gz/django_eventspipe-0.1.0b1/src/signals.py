from django.dispatch import Signal, receiver
from .models import Pipeline

event_signal = Signal()

@receiver(event_signal)
def create_pipelines(
    sender: object, 
    event: dict[str, object], 
    **kwargs
) -> None:
    """
    Signal handler to create `Pipeline` objects from an event
    """
    Pipeline.new_from_event(event)
