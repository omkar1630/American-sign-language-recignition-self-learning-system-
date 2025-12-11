// main.js - Core functionality for SignPro application

document.addEventListener('DOMContentLoaded', function() {
    // ======================
    // Mobile Menu Toggle
    // ======================
    const mobileMenuBtn = document.querySelector('.mobile-menu');
    const navMenu = document.querySelector('nav ul');
    
    if (mobileMenuBtn && navMenu) {
        mobileMenuBtn.addEventListener('click', function() {
            navMenu.classList.toggle('show');
            this.querySelector('i').classList.toggle('fa-times');
            this.querySelector('i').classList.toggle('fa-bars');
        });
    }

    // ======================
    // Smooth Scrolling
    // ======================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });
            }
        });
    });

    // ======================
    // Current Year in Footer
    // ======================
    const currentYear = document.getElementById('current-year');
    if (currentYear) {
        currentYear.textContent = new Date().getFullYear();
    }

    // ======================
    // Dashboard Sidebar Toggle (Mobile)
    // ======================
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');
    
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('show');
        });
    }

    // ======================
    // Notification Dropdown
    // ======================
    const notificationBtn = document.querySelector('.notifications');
    const notificationDropdown = document.querySelector('.notification-dropdown');
    
    if (notificationBtn && notificationDropdown) {
        notificationBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            notificationDropdown.classList.toggle('show');
        });
    }

    // Close dropdowns when clicking outside
    document.addEventListener('click', function() {
        if (notificationDropdown) notificationDropdown.classList.remove('show');
    });

    // ======================
    // User Profile Dropdown
    // ======================
    const userProfile = document.querySelector('.user-profile');
    const profileDropdown = document.querySelector('.profile-dropdown');
    
    if (userProfile && profileDropdown) {
        userProfile.addEventListener('click', function(e) {
            e.stopPropagation();
            profileDropdown.classList.toggle('show');
        });
    }

    // ======================
    // Camera Preview Functionality
    // ======================
    const startCameraBtn = document.querySelector('.start-camera-btn');
    const cameraPreview = document.querySelector('.camera-preview');
    
    if (startCameraBtn && cameraPreview) {
        startCameraBtn.addEventListener('click', function() {
            initCamera();
        });
    }

    // ======================
    // Sign Language Recognition Demo
    // ======================
    const demoVideo = document.querySelector('.demo-video video');
    if (demoVideo) {
        demoVideo.addEventListener('play', function() {
            // Simulate recognition when demo plays
            simulateRecognition();
        });
    }

    // ======================
    // Animation on Scroll
    // ======================
    const animateOnScroll = function() {
        const elements = document.querySelectorAll('.feature-card, .about-content, .about-image');
        
        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            if (elementPosition < windowHeight - 100) {
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }
        });
    };
    
    // Set initial state for animated elements
    document.querySelectorAll('.feature-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    });
    
    document.querySelectorAll('.about-content, .about-image').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateX(' + (el.classList.contains('about-content') ? '-20px' : '20px') + ')';
        el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    });
    
    window.addEventListener('scroll', animateOnScroll);
    animateOnScroll(); // Run once on load
});

// ======================
// Camera Initialization
// ======================
function initCamera() {
    const cameraPreview = document.querySelector('.camera-preview');
    const cameraPlaceholder = document.querySelector('.camera-placeholder');
    const startCameraBtn = document.querySelector('.start-camera-btn');
    
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        alert('Camera access is not supported in your browser');
        return;
    }

    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function(stream) {
            cameraPlaceholder.style.display = 'none';
            
            const videoElement = document.createElement('video');
            videoElement.srcObject = stream;
            videoElement.autoplay = true;
            videoElement.playsInline = true;
            videoElement.style.width = '100%';
            videoElement.style.height = '100%';
            videoElement.style.objectFit = 'cover';
            
            cameraPreview.appendChild(videoElement);
            startCameraBtn.textContent = 'Stop Camera';
            startCameraBtn.classList.remove('btn-primary');
            startCameraBtn.classList.add('btn-danger');
            startCameraBtn.innerHTML = '<i class="fas fa-stop"></i> Stop Camera';
            
            // Change click handler to stop camera
            startCameraBtn.onclick = function() {
                stopCamera(stream, videoElement);
            };
            
            // Start recognition process
            startRecognition(videoElement);
        })
        .catch(function(error) {
            console.error('Error accessing camera:', error);
            alert('Could not access camera: ' + error.message);
        });
}

function stopCamera(stream, videoElement) {
    const tracks = stream.getTracks();
    tracks.forEach(track => track.stop());
    
    videoElement.remove();
    document.querySelector('.camera-placeholder').style.display = 'flex';
    
    const startCameraBtn = document.querySelector('.start-camera-btn');
    startCameraBtn.textContent = 'Start Camera';
    startCameraBtn.classList.remove('btn-danger');
    startCameraBtn.classList.add('btn-primary');
    startCameraBtn.innerHTML = '<i class="fas fa-video"></i> Start Camera';
    
    // Reset click handler
    startCameraBtn.onclick = function() {
        initCamera();
    };
    
    // Stop recognition process
    stopRecognition();
}

// ======================
// Sign Language Recognition
// ======================
let recognitionInterval;

function startRecognition(videoElement) {
    // This would be replaced with actual recognition API calls
    console.log('Starting sign language recognition');
    
    recognitionInterval = setInterval(() => {
        // Simulate recognition results
        const signs = ['Hello', 'Thank you', 'Help', 'Water', 'Friend'];
        const randomSign = signs[Math.floor(Math.random() * signs.length)];
        const confidence = Math.floor(Math.random() * 30) + 70; // 70-100%
        
        updateRecognitionResult(randomSign, confidence);
    }, 3000);
}

function stopRecognition() {
    console.log('Stopping sign language recognition');
    clearInterval(recognitionInterval);
}

function updateRecognitionResult(sign, confidence) {
    const resultContainer = document.querySelector('.recognition-result');
    if (!resultContainer) return;
    
    resultContainer.innerHTML = `
        <div class="result-card">
            <h3>Recognized Sign</h3>
            <div class="sign-display">${sign}</div>
            <div class="confidence ${getConfidenceClass(confidence)}">
                Confidence: ${confidence}%
            </div>
        </div>
    `;
    
    // Add to history table if on dashboard
    addToHistory(sign, confidence);
}

function getConfidenceClass(confidence) {
    if (confidence >= 90) return 'high';
    if (confidence >= 70) return 'medium';
    return 'low';
}

function addToHistory(sign, confidence) {
    const historyTable = document.querySelector('.history-table tbody');
    if (!historyTable) return;
    
    const now = new Date();
    const timeString = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    
    const newRow = document.createElement('tr');
    newRow.innerHTML = `
        <td>Today, ${timeString}</td>
        <td><span class="sign-badge">${sign}</span></td>
        <td>"${sign}"</td>
        <td><span class="confidence ${getConfidenceClass(confidence)}">${confidence}%</span></td>
    `;
    
    historyTable.insertBefore(newRow, historyTable.firstChild);
    
    // Limit to 50 entries
    if (historyTable.children.length > 50) {
        historyTable.removeChild(historyTable.lastChild);
    }
}

// ======================
// Demo Simulation
// ======================
function simulateRecognition() {
    const demoResults = [
        { sign: 'Hello', confidence: 98 },
        { sign: 'How are you', confidence: 95 },
        { sign: 'Thank you', confidence: 97 },
        { sign: 'Goodbye', confidence: 92 }
    ];
    
    let currentIndex = 0;
    const demoInterval = setInterval(() => {
        if (currentIndex >= demoResults.length) {
            clearInterval(demoInterval);
            return;
        }
        
        const result = demoResults[currentIndex];
        updateRecognitionResult(result.sign, result.confidence);
        currentIndex++;
    }, 3000);
    
}