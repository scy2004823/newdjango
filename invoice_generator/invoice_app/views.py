from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from .models import Customer, Product, Invoice, InvoiceItem
from xhtml2pdf import pisa


# -------------------------
# Step 1: Customer Form
# -------------------------
def step1_customer_form(request):
    if request.method == "POST":
        name = request.POST.get("name")
        mobile = request.POST.get("mobile")
        if name and mobile:
            Customer.objects.create(name=name, mobile=mobile)
            return redirect("step2")  # go to customer list
    return render(request, "invoice_app/customer_form.html")


# -------------------------
# Step 2: Customer List
# -------------------------
def step2_customer_list(request):
    customers = Customer.objects.all()
    return render(request, "invoice_app/customer_list.html", {"customers": customers})


# -------------------------
# Step 3: Product Form
# -------------------------
def step3_product_form(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    invoice, _ = Invoice.objects.get_or_create(customer=customer)

    if request.method == "POST":
        product_name = request.POST.get("name")
        price = request.POST.get("price")
        quantity = request.POST.get("quantity")

        if product_name and price and quantity:
            product, created = Product.objects.get_or_create(
                name=product_name,
                defaults={"price": price}
            )
            if not created and str(product.price) != price:
                product.price = price
                product.save()

            InvoiceItem.objects.create(
                invoice=invoice,
                product=product,
                quantity=quantity
            )
            return redirect("step4", invoice_id=invoice.id)  # go to summary

    return render(request, "invoice_app/product_form.html", {"customer": customer})


# -------------------------
# Step 4: Invoice Summary
# -------------------------
def step4_invoice_summary(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    items = invoice.items.all()
    return render(request, "invoice_app/invoice_summary.html", {"invoice": invoice, "items": items})


# -------------------------
# Step 5: Final Invoice
# -------------------------
def step5_final_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    items = invoice.items.all()
    total_amount = invoice.total_amount()
    total_products = invoice.total_products()

    context = {
        "invoice": invoice,
        "items": items,
        "total_amount": total_amount,
        "total_products": total_products,
    }
    return render(request, "invoice_app/final_invoice.html", context)


# -------------------------
# Download Final Invoice PDF (xhtml2pdf)
# -------------------------
def download_invoice_pdf(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    items = invoice.items.all()
    total_amount = invoice.total_amount()
    total_products = invoice.total_products()

    template = get_template("invoice_app/final_invoice_pdf.html")
    html = template.render({
        "invoice": invoice,
        "items": items,
        "total_amount": total_amount,
        "total_products": total_products,
    })

    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.id}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse("Error generating PDF")
    return response
