from django.db import models

class EmailLog(models.Model):
    to_email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='simulated')

    def __str__(self):
        return f"Email to {self.to_email} - {self.subject}"