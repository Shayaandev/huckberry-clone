
async function verifyToken() {
    const token = localStorage.getItem('token');
    if (!token) {
        showLoginLink();
        hideAdminLink();  // ← Hide admin link
        return false;
    }
    
    try {
        const res = await fetch(`${API_URL}/auth/me`, {
            headers: { "Authorization": `Bearer ${token}` }
        });
        
        if (res.ok) {
            const userData = await res.json();
            showLogoutLink();
            
            // Show/hide admin link based on user role
            if (userData.is_admin) {
                showAdminLink();
            } else {
                hideAdminLink();
            }
            
            return userData;
        } else {
            localStorage.removeItem('token');
            showLoginLink();
            hideAdminLink();
            return false;
        }
    } catch (error) {
        localStorage.removeItem('token');
        showLoginLink();
        hideAdminLink();
        return false;
    }
}

function showLoginLink() {
    const loginLink = document.getElementById('login-link');
    const logoutLink = document.getElementById('logout-link');
    if (loginLink) loginLink.style.display = 'inline';
    if (logoutLink) logoutLink.style.display = 'none';
}

function showLogoutLink() {
    const loginLink = document.getElementById('login-link');
    const logoutLink = document.getElementById('logout-link');
    if (loginLink) loginLink.style.display = 'none';
    if (logoutLink) logoutLink.style.display = 'inline';
}

function showAdminLink() {
    const adminLink = document.getElementById('admin-link');
    if (adminLink) adminLink.style.display = 'inline';
}

function hideAdminLink() {
    const adminLink = document.getElementById('admin-link');
    if (adminLink) adminLink.style.display = 'none';
}

function setupLogout() {
    const logoutLink = document.getElementById('logout-link');
    if (logoutLink) {
        logoutLink.onclick = (e) => {
            e.preventDefault();
            localStorage.removeItem('token');
            alert("Logged out successfully");
            window.location.href = '/';
        };
    }
}

// Initialize auth on page load
document.addEventListener('DOMContentLoaded', () => {
    verifyToken();
    setupLogout();
});