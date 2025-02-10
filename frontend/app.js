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
            const response = await fetch(`${API_BASE}/register`, {
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
                    window.location.href = "login.html"; // Redirect to login page
                }, 2000);
            }
        } catch (err) {
            console.error('Error during registration:', err);
            registerMessage.textContent = 'An error occurred. Please try again.';
        }
    });
}
// Handle Login
if (document.getElementById("loginForm")) {
    console.log("this is form",document.getElementById("loginForm"));
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
                localStorage.setItem("email", data.email || email); // Save username
                window.location.href = "dashboard.html";
            } else {
                loginMessage.style.color = "red";
                loginMessage.textContent = data.error || "Login failed. Please try again.";            }
        } catch (error) {
            loginMessage.style.color = "red";
            loginMessage.textContent = "An error occurred while logging in. Please try again.";        }
    });
}
// Handle Dashboard
document.addEventListener('DOMContentLoaded', function () {
    if (document.getElementById("dashboardData")) {
        const token = localStorage.getItem("token");

        if (!token) {
            console.log("No token");
            alert("You are not logged in. Please log in.");
            setTimeout(() => {
                window.location.href = "login.html";
            }, 100);  // Delay for 100 milliseconds
        } else {
            fetch(`${API_BASE}/dashboard`, {
                headers: { Authorization: `Bearer ${token}` },
            })
                .then((response) => {
                    if (response.status === 403) {
                        console.log("Token invalid");
                        alert("Your session has expired or the token is invalid. Please log in again.");
                        localStorage.removeItem("email");
                        localStorage.removeItem("token");
                        window.location.href = "login.html";
                        return;
                    } else {
                        return response.json();
                    }
                })
                .then((data) => {
                    if (data) {
                        document.getElementById("email").innerText = localStorage.getItem("email") || "Guest";
                    }
                })
                .catch(() => {
                    alert("Error loading dashboard data. Redirecting to login.");
                    localStorage.removeItem("email");
                    localStorage.removeItem("token");
                    window.location.href = "index.html";
                });

            document.getElementById("logoutButton").addEventListener("click", () => {
                console.log("Logout button clicked"); // Debugging statement
                localStorage.removeItem("email");
                localStorage.removeItem("token");
                console.log("Local storage after logout:", localStorage); // Debugging statement
                window.location.href = "index.html";
            });

            document.getElementById('fetchDataButton').addEventListener('click', () => {
                fetch(`${API_BASE}/start-producer`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.message) {
                            alert(data.message);
                        } else {
                            alert('Unexpected response from server');
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        alert('Failed to fetch real-time data');
                    });
            });
        }
    }
});
