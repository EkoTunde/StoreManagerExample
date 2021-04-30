from django import forms

from product.models import Product

class CreateProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = ['name','manufacturer', 'category', 'model', 'price','specifications','stock','discount']
        
        
class UpdateProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = ['name','manufacturer', 'category', 'model', 'price','specifications','stock','discount']
        
    def save(self, commit=True):
        product = self.instance
        product.name = self.cleaned_data['name']
        product.manufacturer = self.cleaned_data['manufacturer']
        product.category = self.cleaned_data['category']
        product.model = self.cleaned_data['model']
        product.price = self.cleaned_data['price']
        product.specifications = self.cleaned_data['specifications']
        product.stock = self.cleaned_data['stock']
        product.discount = self.cleaned_data['discount']
            
        if commit:
            product.save()
        
        return product


# class DeleteProductForm(forms.ModelForm):
    
#     class Meta:
#         model = Product
#         fields = ['name','manufacturer', 'category', 'model', 'price','specifications','stock','discount']

#     def delete(self):
#         product = self.instance
#         product.delete()
#         return True