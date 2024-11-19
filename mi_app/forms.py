from django import forms
from .models import Compra

class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['nombre', 'email', 'metodo_pago', 'comentarios']
        widgets = {
            'comentarios': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
