from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Artifact

@login_required
def get_artifact(request: HttpRequest, artifact_id: int) -> HttpResponse:
    """
    Get a file from Database
    """
    file = Artifact.objects.get(pk=artifact_id)

    response = HttpResponse(file.data, content_type='application/octet-stream')
    response['Content-Disposition']='attachment;filename=%s' % file.name

    return response
