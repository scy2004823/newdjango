document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ JS connected");

    // =============================
    // Step 1: Customer Form Validation
    // =============================
    const customerForm = document.querySelector("form[action='']");
    if (customerForm && document.getElementById("mobile")) {
        customerForm.addEventListener("submit", function (e) {
            const name = document.getElementById("name").value.trim();
            const mobile = document.getElementById("mobile").value.trim();

            if (!name || !mobile) {
                alert("Please fill in all fields!");
                e.preventDefault();
                return;
            }

            if (isNaN(mobile) || mobile.length < 7) {
                alert("Please enter a valid mobile number!");
                e.preventDefault();
            }
        });
    }

    // =============================
    // Step 3: Product Form Validation
    // =============================
    const productForm = document.querySelector("form[action='']");
    if (productForm && document.getElementById("quantity")) {
        productForm.addEventListener("submit", function (e) {
            const pname = document.getElementById("name").value.trim();
            const qty = document.getElementById("quantity").value.trim();
            const price = document.getElementById("price").value.trim();

            if (!pname || !qty || !price) {
                alert("Please fill in all product details!");
                e.preventDefault();
                return;
            }

            if (isNaN(qty) || qty <= 0) {
                alert("Quantity must be a positive number!");
                e.preventDefault();
                return;
            }

            if (isNaN(price) || price <= 0) {
                alert("Price must be a positive number!");
                e.preventDefault();
            }
        });
    }
});
