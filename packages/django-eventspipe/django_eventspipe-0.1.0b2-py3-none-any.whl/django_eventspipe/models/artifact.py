import hashlib
from django.db import models

class Artifact(models.Model):
    name       = models.CharField(max_length=1024)
    data       = models.BinaryField(blank=True)
    timestamp  = models.DateTimeField(auto_now_add=True)
    md5sum     = models.CharField(max_length=32, blank=True, editable=False, unique=True)  # Unique MD5 checksum

    @classmethod
    def get_or_create(cls, name:str, data:bytes) -> object:
        # Compute the MD5 checksum of the data
        md5sum = hashlib.md5(data).hexdigest()

        if cls.objects.filter(md5sum=md5sum).exists():
            return cls.objects.get(md5sum=md5sum)

        file = cls(name=name,data=data,md5sum=md5sum)
        file.save()

        return file
        
    def get_size(self) -> float:
        """
        Get size in KB of a file
        """
        return len(self.data) / 1000


