from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.name} ({self.mobile})"


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.price}"


class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_amount(self):
        return sum(item.subtotal() for item in self.items.all())

    def total_products(self):
        return sum(item.quantity for item in self.items.all())

    def __str__(self):
        return f"Invoice #{self.id} - {self.customer.name}"


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def subtotal(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
