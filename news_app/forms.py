from django import forms
from .models import Contact, Comments

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['body']