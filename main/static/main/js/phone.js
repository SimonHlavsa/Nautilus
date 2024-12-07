document.addEventListener("DOMContentLoaded", function () {
    const phoneInput = document.querySelector("input[name='phone']");
    if (phoneInput) {
        // Set default value
        if (!phoneInput.value.startsWith("+420")) {
            phoneInput.value = "+420 ";
        }

        phoneInput.addEventListener("input", function () {
            // Ensure +420 is always at the start
            if (!phoneInput.value.startsWith("+420")) {
                phoneInput.value = "+420 ";
            }

            let value = phoneInput.value.replace("+420", "").replace(/\D/g, ""); // Remove +420 and all non-numeric characters
            
            // Format the number with spaces
            phoneInput.value = "+420 " + value.replace(/(\d{3})(\d{0,3})(\d{0,3})/, function (_, g1, g2, g3) {
                return [g1, g2, g3].filter(Boolean).join(" "); // Add spaces
            });

            // Set cursor at the end
            const cursorPosition = phoneInput.value.length;
            phoneInput.setSelectionRange(cursorPosition, cursorPosition);
        });
    }
});
