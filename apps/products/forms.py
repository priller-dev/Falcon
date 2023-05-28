from django import forms

from apps.products import models


class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=models.Category.objects,
        empty_label=None,
        to_field_name='id'
    )

    class Meta:
        model = models.Product
        exclude = ('created_at',)

    def is_valid(self):
        return super().is_valid()


class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        exclude = ('created_at',)


