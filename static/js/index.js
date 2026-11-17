const input = document.getElementById("imagens");
const preview = document.getElementById("preview-imagens");

input.addEventListener("change", function () {

    preview.innerHTML = "";

    const files = Array.from(this.files);

    if (files.length > 3) {
        alert("Você pode enviar no máximo 3 imagens.");
        input.value = "";
        return;
    }

    files.forEach(file => {

        const reader = new FileReader();

        reader.onload = function(e) {

            const img = document.createElement("img");

            img.src = e.target.result;

            img.style.width = "120px";
            img.style.height = "120px";
            img.style.objectFit = "cover";
            img.classList.add("rounded", "border");

            preview.appendChild(img);

        };

        reader.readAsDataURL(file);

    });

});