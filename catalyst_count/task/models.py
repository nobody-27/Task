from django.db import models
# Create your models here.
import uuid
from django.contrib.auth import get_user_model
User = get_user_model()

def generate_upload_id():
    return uuid.uuid4().hex


class ChunkedUpload(models.Model):
    upload_id = models.CharField(max_length=32, unique=True, editable=False, default=generate_upload_id)
    filename = models.CharField(max_length=255)
    file_path = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)

    def __str__(self) -> str:
        return self.filename
    

class Company(models.Model):
    name = models.CharField(max_length=100,default="Test")
    domain = models.CharField(max_length=300,null=True)
    year_founded = models.CharField(max_length=300,null=True)
    industory = models.CharField(max_length=300,null=True)
    size_range = models.CharField(max_length=300,null=True)
    locality = models.CharField(max_length=300,null=True)
    country = models.CharField(max_length=300,null=True)
    linkedin_url = models.CharField(max_length=300,null=True)
    current_employee_estimate = models.CharField(max_length=300,null=True)
    total_employee_estimate = models.CharField(max_length=300,null=True)

    def __str__(self) -> str:
        return self.name    