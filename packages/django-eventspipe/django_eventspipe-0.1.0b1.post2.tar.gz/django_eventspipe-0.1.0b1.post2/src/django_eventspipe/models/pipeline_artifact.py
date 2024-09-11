from django.db import models
from django.apps import apps

class PipelineArtifact(models.Model):
    """
    Artifact -> Pipeline association
    """
    pipeline = models.ForeignKey("django_eventspipe.Pipeline", on_delete=models.CASCADE)
    artifact = models.ForeignKey("django_eventspipe.Artifact", on_delete=models.CASCADE)

    @classmethod
    def add_artifact(cls, pipeline: object, file_name: str, file_data: bytes) -> bool:
        """
        Add a new artifact to the database
        """
        Artifact = apps.get_model("django_eventspipe.Artifact")

        artifact = Artifact.get_or_create(name=file_name, data=file_data)

        pipeline_artifact = cls(pipeline=pipeline, artifact=artifact)
        pipeline_artifact.save()

        return True

    @classmethod
    def get_artifacts(cls, pipeline: object) -> dict[str, object]:
        """
        Get stored artifacts for a Pipeline
        """

        out = {}
        artifacts = cls.objects.filter(pipeline=pipeline)

        for artifact in artifacts:
            out[artifact.artifact.name] = bytes(artifact.artifact.data)

        return out
