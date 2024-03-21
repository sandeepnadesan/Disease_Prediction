document.addEventListener("DOMContentLoaded", function() {
    const registrationForm = document.getElementById("registrationForm");
    const registerButton = document.getElementById("registerButton");

    registerButton.addEventListener("click", function(event) {
        event.preventDefault();

        // Retrieve form data
        const username = document.getElementById("username").value;
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;
        const confirmPassword = document.getElementById("confirmPassword").value;

        // Perform validation
        if (password !== confirmPassword) {
            alert("Passwords do not match!");
            return;
        }

        // Perform registration (You can make AJAX request here to your backend)

        // Assuming registration is successful, redirect to the next page
        window.location.href = "/home/sandeep/Desktop/HACK/NEW/chatpdf.py"; // Change "next_page.html" to your desired next page
    });
});
