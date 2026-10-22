from django import forms

# Simulamos los campos de una tarjeta
class PaymentForm(forms.Form):
  card_holder = forms.CharField(
      label='Titular de la tarjeta',
      max_length=100,
      widget=forms.TextInput(
          attrs={'class': 'form-control', 'placeholder': 'Ej. Juan Pérez'}
      ),
  )
  card_number = forms.CharField(
      label='Número de tarjeta',
      max_length=16,
      widget=forms.TextInput(
          attrs={'class': 'form-control', 'placeholder': '4532 •••• •••• ••••'}
      ),
  )
  expiry_date = forms.CharField(
      label='Fecha de caducidad',
      max_length=5,
      widget=forms.TextInput(
          attrs={'class': 'form-control', 'placeholder': 'MM/AA'}
      ),
  )
  cvv = forms.CharField(
      label='CVV',
      max_length=4,
      widget=forms.PasswordInput(
          attrs={'class': 'form-control', 'placeholder': '123'}
      ),
  )