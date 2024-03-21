import streamlit as st

registration_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registration</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <h2>Registration Form</h2>
        <form id="registrationForm">
            <label for="username">Username:</label>
            <input type="text" id="username" required>
            <label for="email">Email:</label>
            <input type="email" id="email" required>
            <label for="password">Password:</label>
            <input type="password" id="password" required>
            <label for="confirmPassword">Confirm Password:</label>
            <input type="password" id="confirmPassword" required>
            <button type="submit" id="registerButton">Register</button>
        </form>
    </div>
    <script>
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

                // Redirect to Streamlit page
                window.location.href = "http://localhost:8501"; // Change the URL to your Streamlit app's URL
            });
        });
    </script>
</body>
</html>

"""

# Display the registration form
st.markdown(registration_html, unsafe_allow_html=True)
