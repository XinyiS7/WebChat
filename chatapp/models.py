from django.db import models

class TextSubmission(models.Model):
    MODE_CHOICES = [
        ('chat', 'Chat Mode'),
        ('coder', 'Coder Mode'),
    ]

    input_text = models.TextField()
    processed_text = models.TextField(blank=True)
    mode = models.CharField(
        max_length=5,
        choices=MODE_CHOICES,
        default='chat'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'webchat_app_textsubmission'
