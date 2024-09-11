from django.db import models
from django.apps import apps
from django.utils.module_loading import import_string

class PipelineDefinition(models.Model):
    event     = models.CharField(max_length=256)
    filters   = models.JSONField(blank=True, null=True, default=dict)
    options   = models.JSONField(blank=True, null=True, default=dict)
    enabled   = models.BooleanField(default=True)

    @classmethod
    def get_definitions(cls, event):
        """
        Get pipeline definitions for a given event.
        """
        event_name = event.get("name")

        # Use ORM to fetch enabled definitions for the event in one query
        all_definitions = cls.objects.filter(event=event_name, enabled=True)

        # Separate generic and custom definitions
        generic_definitions = []
        custom_definitions = []

        for definition in all_definitions:
            filters = definition.filters or {}
            
            # Check if filters exist, otherwise it's a generic definition
            if filters:
                match = all(
                    event.get(key) == value 
                    for key, value in filters.items()
                    if key in event
                )
                if match:
                    custom_definitions.append(definition)
            else:
                generic_definitions.append(definition)

        # Return custom definitions if available, otherwise return generic ones
        return custom_definitions if custom_definitions else generic_definitions

    def get_defined_tasks(self) -> list:
        """
        Get Tasks defined for this PipelineDefinition
        """
        PipelineDefinitionTaskDefinition = apps.get_model('django_eventspipe.PipelineDefinitionTaskDefinition')

        tasks = []
        for definition in PipelineDefinitionTaskDefinition.objects.filter(pipeline_definition=self, enabled=True).order_by('order'):
            tasks.append(definition)

        return tasks

    def get_tasks_chain(self, context) -> list:
        """
        Get Tasks defined for this PipelineDefinition as a celery chain
        """
        PipelineDefinitionTaskDefinition = apps.get_model('django_eventspipe.PipelineDefinitionTaskDefinition')

        chain = []
        first = True

        for task_function in PipelineDefinitionTaskDefinition.objects.filter(
            pipeline_definition=self, 
            enabled=True
        ).order_by('order').values_list('task_definition__function'):

            if first:
                signature = import_string(task_function[0]).s(context)
                first = False
            else:
                signature = import_string(task_function[0]).s()

            chain.append(signature)

        return chain
