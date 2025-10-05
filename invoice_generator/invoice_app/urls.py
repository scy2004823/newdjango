from django.urls import path
from . import views

urlpatterns = [
    path('', views.step1_customer_form, name="step1"),  # Homepage = Customer Form
    path('step2/', views.step2_customer_list, name="step2"),
    path('step3/<int:customer_id>/', views.step3_product_form, name="step3"),
    path('step4/<int:invoice_id>/', views.step4_invoice_summary, name="step4"),
    path('step5/<int:invoice_id>/', views.step5_final_invoice, name="step5"),
    path('invoice/<int:invoice_id>/download/', views.download_invoice_pdf, name="download_invoice_pdf"),
]
