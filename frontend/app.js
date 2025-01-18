const API_BASE = "http://localhost:3000";

// Validate Password on the Client Side
function validatePassword(password) {
    const regex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_]).{8,}$/;
    return regex.test(password);
}

// Handle Registration
if (document.getElementById("registerForm")) {
    document.getElementById("registerForm").addEventListener("submit", async (e) => {
        e.preventDefault();
        const email = document.getElementById("registerEmail").value;
        const password = document.getElementById("registerPassword").value;
        const registerMessage = document.getElementById("registerMessage");

        try {
            const response = await fetch('http://localhost:3000/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password }),
            });
    
            const data = await response.json();
    
            if (!response.ok) {
                // Display backend error message
                registerMessage.textContent = data.error;
            } else {
                registerMessage.style.color = "green";
                registerMessage.textContent = data.message;
                setTimeout(() => {
                    window.location.href = "index.html"; // Redirect to login page
                }, 2000);
            }
        } catch (err) {
            console.error('Error during registration:', err);
            registerMessage.textContent = 'An error occurred. Please try again.';
        }
    
    });
    
    // Show/Hide Password
    document.getElementById("showPassword").addEventListener("change", (e) => {
        const passwordField = document.getElementById("registerPassword");
        const type = e.target.checked ? "text" : "password";
        passwordField.type = type;    
    });
}

// Handle Login
if (document.getElementById("loginForm")) {
    document.getElementById("loginForm").addEventListener("submit", async (e) => {
        e.preventDefault();
        const email = document.getElementById("loginEmail").value;
        const password = document.getElementById("loginPassword").value;
        const loginMessage = document.getElementById("loginMessage");

        try {
            const response = await fetch(`${API_BASE}/login`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password }),
            });
            const data = await response.json();
            if (data.token) {
                localStorage.setItem("token", data.token);
                window.location.href = "dashboard.html";
            } else {
                loginMessage.style.color = "red";
                loginMessage.textContent = data.error || "Login failed. Please try again.";            }
        } catch (error) {
            loginMessage.style.color = "red";
            loginMessage.textContent = "An error occurred while logging in. Please try again.";        }
    });
    // Show/Hide Password
    document.getElementById("showPassword").addEventListener("change", (e) => {
        const passwordFieldLogin = document.getElementById("loginPassword");
        const type = e.target.checked ? "text" : "password";
        passwordFieldLogin.type = type;
    });
}

// Handle Dashboard
if (document.getElementById("dashboardData")) {
    const token = localStorage.getItem("token");
    if (!token) {
        window.location.href = "index.html";
    } else {
        fetch(`${API_BASE}/dashboard`, {
            headers: { Authorization: `Bearer ${token}` },
        })
            .then((response) => response.json())
            .then((data) => {
                document.getElementById("dashboardData").innerText = data.message || "Welcome to the dashboard!";
            })
            .catch(() => {
                document.getElementById("dashboardData").innerText = "Error loading dashboard.";
            });

        document.getElementById("logoutButton").addEventListener("click", () => {
            localStorage.removeItem("token");
            window.location.href = "index.html";
        });
    }
}
