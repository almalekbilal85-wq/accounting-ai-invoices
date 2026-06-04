

document.addEventListener("DOMContentLoaded", function () {

    const fileContainer = document.getElementById("invoice-file-url");

    if (!fileContainer) return;

    const url = fileContainer.dataset.url;

    if (!url) return;

    const imageEl = document.getElementById("invoice-image");
    const pdfEl = document.getElementById("invoice-pdf");

    imageEl.style.display = "none";
    pdfEl.style.display = "none";
    imageEl.src = "";
    pdfEl.src = "";

    

    const extension = url.split('.').pop().toLowerCase();

    if (["jpg", "jpeg", "png", "webp"].includes(extension)) {

        imageEl.src = url;
        imageEl.style.display = "block";

    } else if (extension === "pdf") {

        pdfEl.src = url;
        pdfEl.style.display = "block";

        button_pdf = document.getElementById("pdf-button");
        button_pdf.style.display = "block";

    }

   

});

