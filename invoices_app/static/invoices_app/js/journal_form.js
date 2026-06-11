
console.log("JS FILE LOADED");


document.addEventListener("DOMContentLoaded", function () {

    const journalType = document.getElementById("id_type");

    const invoiceSection = document.getElementById("invoice-section");

    function toggleInvoiceSection() {

        if (journalType.value === "invoice") {

            invoiceSection.style.display = "block";

        } else {

            invoiceSection.style.display = "none";

        }

    }

    journalType.addEventListener("change", toggleInvoiceSection);

    toggleInvoiceSection();

});


document.addEventListener("DOMContentLoaded", function () {

    const fileInput = document.getElementById("id_file");

    const imagePreview = document.getElementById("invoice-preview");

    const pdfPreview = document.getElementById("pdf-preview");

    if (!fileInput) return;

    fileInput.addEventListener("change", function () {

        const file = this.files[0];

        if (!file) return;

        const fileURL = URL.createObjectURL(file);

        // Reset both
        imagePreview.style.display = "none";
        pdfPreview.style.display = "none";

        // IMAGE
        if (file.type.startsWith("image/")) {

            imagePreview.src = fileURL;
            imagePreview.style.display = "block";

        }

        // PDF
        else if (file.type === "application/pdf") {

            pdfPreview.src = fileURL;
            pdfPreview.style.display = "block";

        }

    });

});


const loadingOverlay = document.getElementById("ai-loading-overlay");

function showLoading() {
    loadingOverlay.style.display = "flex";
}

function hideLoading() {
    loadingOverlay.style.display = "none";
}


document.addEventListener("DOMContentLoaded", function () {

    const fileInput = document.getElementById("id_file");  // your invoice file field

    if (!fileInput) return;

    fileInput.addEventListener("change", async function () {

        const file = this.files[0];

        if (!file) return;

        const formData = new FormData();
        formData.append("file", file);

        // CSRF token
        const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

        try {

            showLoading();

            const response = await fetch(AI_URL, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken
                },
                body: formData
            });

            const data = await response.json();

            console.log("AI Response:", data);
            

            // Autofill JOURNAL FORM

            if (data.invoice_number) {
                document.getElementById("id_invoice_number").value = data.invoice_number;
            }

            if (data.supplier_name) {
                document.getElementById("id_supplier").value = data.supplier_name;
            }

            if (data.invoice_date) {
                document.getElementById("id_invoice_date").value = data.invoice_date;
            }
            
            if (data.due_date) {
                document.getElementById("id_due_date").value = data.due_date;
            }


            if (data.total_amount) {
                document.getElementById("id_total_amount").value = data.total_amount;
            }

            if (data.vat_amount) {
                document.getElementById("id_vat_amount").value = data.vat_amount;
            }

            if (data.description) {
                document.getElementById("id_description").value = data.description;
            }


            // Autofill ACCOUNTING LINES (example first row)
            if (data.accounting_entries) {

                data.accounting_entries.forEach((line, index) => {

                    const accountField = document.getElementById(
                        `id_accounting_lines-${index}-account_number`
                    );

                    const descriptionField = document.getElementById(
                        `id_accounting_lines-${index}-description`
                    );            

                    const debitField = document.getElementById(
                        `id_accounting_lines-${index}-debit`
                    );

                    const creditField = document.getElementById(
                        `id_accounting_lines-${index}-credit`
                    );

                    if (accountField) {
                        accountField.value = line.account;
                    }

                    if (debitField) {
                        debitField.value = line.debit;
                    }

                    if (creditField) {
                        creditField.value = line.credit;
                    }

                    if (descriptionField) {
                        descriptionField.value = line.description;
                    }

                    

                });

            }

        } catch (error) {
            console.error("AI extraction failed:", error);
        } finally {
        
        hideLoading();
    }

    });

});


document.addEventListener("DOMContentLoaded", function () {

    const table = document.querySelector("table");

    const totalForms = document.getElementById("id_accounting_lines-TOTAL_FORMS");

    function getFormCount() {
        return parseInt(totalForms.value);
    }

    function addRow() {

        let formIdx = getFormCount();

        const tableBody = table.querySelector("tbody");

        const newRow = tableBody.rows[0].cloneNode(true);

        // Update all inputs inside the new row
        newRow.querySelectorAll("input").forEach(input => {

            if (input.name) {
                input.name = input.name.replace(/-\d+-/, `-${formIdx}-`);
                input.id = input.id.replace(/-\d+-/, `-${formIdx}-`);
            }

            if (input.type !== "checkbox") {
                input.value = "";
            }

            if (input.type === "checkbox") {
                input.checked = false;
            }

        });

        tableBody.appendChild(newRow);

        totalForms.value = formIdx + 1;

    }

    // Detect last row input focus
    table.addEventListener("focusin", function (e) {

        const inputs = Array.from(table.querySelectorAll("tbody input"));

        const lastInput = inputs[inputs.length - 1];

        if (e.target === lastInput) {
            addRow();
        }

    });

});


// Account number description API fetching code

document.addEventListener("DOMContentLoaded", function () {

    async function lookupAccount(params) {

        const query = new URLSearchParams(params);

        const response = await fetch(
            `${ACCOUNT_LOOKUP_URL}?${query.toString()}`
        );

        if (!response.ok) {
            return null;
        }

        return await response.json();
    }

    document.addEventListener("change", async function (event) {

        const row = event.target.closest("tr");

        if (!row) return;

        const accountNumberInput =
            row.querySelector(".account-number-field");

        const descriptionInput =
            row.querySelector(".account-description-field");

        // Account number changed
        if (event.target.classList.contains("account-number-field")) {

            if (!accountNumberInput.value.trim()) return;

            const data = await lookupAccount({
                account_number: accountNumberInput.value.trim()
            });

            if (data) {
                descriptionInput.value = data.description;
            }
        }

        // Description changed
        if (event.target.classList.contains("account-description-field")) {

            if (!descriptionInput.value.trim()) return;

            const data = await lookupAccount({
                description: descriptionInput.value.trim()
            });

            if (data) {
                accountNumberInput.value = data.account_number;
            }
        }

    });

});