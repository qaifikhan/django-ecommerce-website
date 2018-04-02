from django import forms
from .models import Cart


class CartForm(forms.ModelForm):
	class Meta(object):
		model = Cart
		fields = [
			"ordered_quantity"
		]