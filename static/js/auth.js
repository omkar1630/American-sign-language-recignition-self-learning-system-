// auth.js - Authentication functionality for SignPro

document.addEventListener('DOMContentLoaded', function() {
    // ======================
    // Form Validation
    // ======================
    const loginForm = document.getElementById('login-form');
    const signupForm = document.getElementById('signup-form');
    
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
    
    if (signupForm) {
        signupForm.addEventListener('submit', handleSignup);
        
        // Password strength indicator
        const passwordInput = signupForm.querySelector('input[name="password"]');
        if (passwordInput) {
            passwordInput.addEventListener('input', updatePasswordStrength);
        }
    }

    // ======================
    // Toggle Password Visibility
    // ======================
    document.querySelectorAll('.toggle-password').forEach(button => {
        button.addEventListener('click', function() {
            const input = this.parentElement.querySelector('input');
            const icon = this.querySelector('i');
            
            if (input.type === 'password') {
                input.type = 'text';
                icon.classList.remove('fa-eye');
                icon.classList.add('fa-eye-slash');
            } else {
                input.type = 'password';
                icon.classList.remove('fa-eye-slash');
                icon.classList.add('fa-eye');
            }
        });
    });

    // ======================
    // Social Login Buttons
    // ======================
    document.querySelectorAll('.btn-social').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const provider = this.classList.contains('btn-google') ? 'google' : 'facebook';
            socialLogin(provider);
        });
    });

    // ======================
    // Forgot Password
    // ======================
    const forgotPasswordLink = document.querySelector('.forgot-password');
    if (forgotPasswordLink) {
        forgotPasswordLink.addEventListener('click', function(e) {
            e.preventDefault();
            showForgotPasswordModal();
        });
    }
});

// ======================
// Login Handler
// ======================
async function handleLogin(e) {
    e.preventDefault();
    
    const form = e.target;
    const email = form.email.value;
    const password = form.password.value;
    const submitBtn = form.querySelector('button[type="submit"]');
    
    // Validate inputs
    if (!email || !password) {
        showAlert('Please fill in all fields', 'error');
        return;
    }
    
    // Disable button during submission
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Signing In...';
    
    try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        // In a real app, you would make an actual API call here:
        // const response = await fetch('/api/login', {
        //     method: 'POST',
        //     headers: { 'Content-Type': 'application/json' },
        //     body: JSON.stringify({ email, password })
        // });
        // const data = await response.json();
        
        // For demo purposes, we'll simulate a successful login
        const data = { success: true, token: 'demo-token', user: { name: 'Demo User' } };
        
        if (data.success) {
            // Store token in localStorage (in a real app)
            localStorage.setItem('authToken', data.token);
            
            // Redirect to dashboard
            window.location.href = 'dashboard.html';
        } else {
            showAlert('Invalid email or password', 'error');
        }
    } catch (error) {
        console.error('Login error:', error);
        showAlert('An error occurred during login', 'error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Sign In';
    }
}

// ======================
// Signup Handler
// ======================
async function handleSignup(e) {
    e.preventDefault();
    
    const form = e.target;
    const name = form.name.value;
    const email = form.email.value;
    const password = form.password.value;
    const confirmPassword = form.confirmPassword.value;
    const submitBtn = form.querySelector('button[type="submit"]');
    
    // Validate inputs
    if (!name || !email || !password || !confirmPassword) {
        showAlert('Please fill in all fields', 'error');
        return;
    }
    
    if (password !== confirmPassword) {
        showAlert('Passwords do not match', 'error');
        return;
    }
    
    if (password.length < 8) {
        showAlert('Password must be at least 8 characters', 'error');
        return;
    }
    
    // Disable button during submission
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Creating Account...';
    
    try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        // In a real app, you would make an actual API call here:
        // const response = await fetch('/api/signup', {
        //     method: 'POST',
        //     headers: { 'Content-Type': 'application/json' },
        //     body: JSON.stringify({ name, email, password })
        // });
        // const data = await response.json();
        
        // For demo purposes, we'll simulate a successful signup
        const data = { success: true, token: 'demo-token', user: { name } };
        
        if (data.success) {
            // Store token in localStorage (in a real app)
            localStorage.setItem('authToken', data.token);
            
            // Redirect to dashboard
            window.location.href = 'dashboard.html';
        } else {
            showAlert('Registration failed. Please try again.', 'error');
        }
    } catch (error) {
        console.error('Signup error:', error);
        showAlert('An error occurred during registration', 'error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Sign Up';
    }
}

// ======================
// Social Login
// ======================
function socialLogin(provider) {
    // In a real app, this would redirect to the provider's auth page
    // or use their SDK for authentication
    
    console.log(`Attempting ${provider} login`);
    showAlert(`Redirecting to ${provider} login...`, 'info');
    
    // Simulate social login success after delay
    setTimeout(() => {
        localStorage.setItem('authToken', `${provider}-demo-token`);
        window.location.href = 'dashboard.html';
    }, 2000);
}

// ======================
// Password Strength Meter
// ======================
function updatePasswordStrength() {
    const password = this.value;
    const strengthMeter = document.getElementById('password-strength');
    
    if (!strengthMeter) return;
    
    // Calculate strength (simplified for demo)
    let strength = 0;
    if (password.length >= 8) strength += 1;
    if (password.match(/[A-Z]/)) strength += 1;
    if (password.match(/[0-9]/)) strength += 1;
    if (password.match(/[^A-Za-z0-9]/)) strength += 1;
    
    // Update UI
    strengthMeter.style.width = `${strength * 25}%`;
    
    if (strength < 2) {
        strengthMeter.style.backgroundColor = '#dc3545'; // Red
    } else if (strength < 4) {
        strengthMeter.style.backgroundColor = '#fd7e14'; // Orange
    } else {
        strengthMeter.style.backgroundColor = '#28a745'; // Green
    }
}

// ======================
// Forgot Password Modal
// ======================
function showForgotPasswordModal() {
    const modalHTML = `
        <div class="modal-overlay">
            <div class="modal">
                <div class="modal-header">
                    <h3>Reset Password</h3>
                    <button class="close-modal">&times;</button>
                </div>
                <div class="modal-body">
                    <p>Enter your email to receive a password reset link</p>
                    <form id="reset-password-form">
                        <div class="form-group">
                            <input type="email" placeholder="Your email" required>
                        </div>
                        <button type="submit" class="btn btn-primary btn-block">Send Reset Link</button>
                    </form>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    
    // Add event listeners
    const modalOverlay = document.querySelector('.modal-overlay');
    const closeBtn = document.querySelector('.close-modal');
    const resetForm = document.getElementById('reset-password-form');
    
    closeBtn.addEventListener('click', () => {
        modalOverlay.remove();
    });
    
    modalOverlay.addEventListener('click', (e) => {
        if (e.target === modalOverlay) {
            modalOverlay.remove();
        }
    });
    
    if (resetForm) {
        resetForm.addEventListener('submit', (e) => {
            e.preventDefault();
            handlePasswordReset(resetForm);
        });
    }
}

async function handlePasswordReset(form) {
    const email = form.querySelector('input').value;
    const submitBtn = form.querySelector('button[type="submit"]');
    
    if (!email) {
        showAlert('Please enter your email', 'error');
        return;
    }
    
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
    
    try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        // In a real app, you would make an actual API call here
        showAlert('Password reset link sent to your email', 'success');
        document.querySelector('.modal-overlay').remove();
    } catch (error) {
        showAlert('Failed to send reset link. Please try again.', 'error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Send Reset Link';
    }
}

// ======================
// Helper Functions
// ======================
function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    
    document.body.appendChild(alertDiv);
    
    setTimeout(() => {
        alertDiv.classList.add('fade-out');
        setTimeout(() => alertDiv.remove(), 500);
    }, 3000);
}

// Check authentication status
function checkAuth() {
    const authToken = localStorage.getItem('authToken');
    const authPages = ['login.html', 'signup.html'];
    const currentPage = window.location.pathname.split('/').pop();
    
    if (authToken && authPages.includes(currentPage)) {
        window.location.href = 'dashboard.html';
    } else if (!authToken && !authPages.includes(currentPage)) {
        window.location.href = 'login.html';
    }
}

// Initialize auth check when page loads
checkAuth();