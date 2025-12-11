// recognize.js - Sign language recognition interface

document.addEventListener('DOMContentLoaded', function() {
    // ======================
    // Camera Controls
    // ======================
    const startCameraBtn = document.getElementById('start-camera');
    const captureBtn = document.getElementById('capture-btn');
    const videoElement = document.getElementById('camera-feed');
    const canvasElement = document.getElementById('canvas');
    const resultContainer = document.getElementById('recognition-result');
    let stream = null;

    if (startCameraBtn) {
        startCameraBtn.addEventListener('click', toggleCamera);
    }

    if (captureBtn) {
        captureBtn.addEventListener('click', captureFrame);
        captureBtn.disabled = true;
    }

    // ======================
    // Recognition Mode Selector
    // ======================
    const modeSelector = document.getElementById('recognition-mode');
    if (modeSelector) {
        modeSelector.addEventListener('change', function() {
            updateRecognitionUI(this.value);
        });
    }

    // ======================
    // Sign Language Library
    // ======================
    const signLibraryBtn = document.getElementById('sign-library-btn');
    if (signLibraryBtn) {
        signLibraryBtn.addEventListener('click', showSignLibrary);
    }

    // ======================
    // History Navigation
    // ======================
    const historyBackBtn = document.getElementById('history-back');
    const historyForwardBtn = document.getElementById('history-forward');
    
    if (historyBackBtn && historyForwardBtn) {
        historyBackBtn.addEventListener('click', navigateHistory);
        historyForwardBtn.addEventListener('click', navigateHistory);
    }

    // ======================
    // Initialize UI
    // ======================
    updateRecognitionUI(modeSelector ? modeSelector.value : 'realtime');
});

// ======================
// Camera Functions
// ======================
async function toggleCamera() {
    const startCameraBtn = document.getElementById('start-camera');
    const captureBtn = document.getElementById('capture-btn');
    const videoElement = document.getElementById('camera-feed');
    
    if (startCameraBtn.textContent.includes('Start')) {
        try {
            stream = await navigator.mediaDevices.getUserMedia({ 
                video: { 
                    width: 1280, 
                    height: 720,
                    facingMode: 'user' 
                }, 
                audio: false 
            });
            
            videoElement.srcObject = stream;
            videoElement.play();
            
            startCameraBtn.innerHTML = '<i class="fas fa-stop"></i> Stop Camera';
            startCameraBtn.classList.remove('btn-primary');
            startCameraBtn.classList.add('btn-danger');
            
            captureBtn.disabled = false;
            
            // Start recognition if in realtime mode
            if (document.getElementById('recognition-mode').value === 'realtime') {
                startRealtimeRecognition();
            }
        } catch (err) {
            console.error('Error accessing camera:', err);
            showAlert('Could not access camera: ' + err.message, 'error');
        }
    } else {
        stopCamera();
    }
}

function stopCamera() {
    const startCameraBtn = document.getElementById('start-camera');
    const captureBtn = document.getElementById('capture-btn');
    const videoElement = document.getElementById('camera-feed');
    
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
    }
    
    videoElement.srcObject = null;
    
    startCameraBtn.innerHTML = '<i class="fas fa-video"></i> Start Camera';
    startCameraBtn.classList.remove('btn-danger');
    startCameraBtn.classList.add('btn-primary');
    
    captureBtn.disabled = true;
    
    // Stop recognition
    stopRealtimeRecognition();
}

function captureFrame() {
    const videoElement = document.getElementById('camera-feed');
    const canvasElement = document.getElementById('canvas');
    const ctx = canvasElement.getContext('2d');
    
    // Draw video frame to canvas
    canvasElement.width = videoElement.videoWidth;
    canvasElement.height = videoElement.videoHeight;
    ctx.drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);
    
    // Process the captured frame
    processFrame(canvasElement);
}

// ======================
// Recognition Functions
// ======================
let recognitionActive = false;
let recognitionInterval;

function startRealtimeRecognition() {
    if (recognitionActive) return;
    
    recognitionActive = true;
    const videoElement = document.getElementById('camera-feed');
    const resultContainer = document.getElementById('recognition-result');
    
    console.log('Starting realtime recognition');
    resultContainer.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-spin"></i> Analyzing signs...</div>';
    
    // Simulate recognition with random results
    recognitionInterval = setInterval(() => {
        const signs = ['Hello', 'Thank you', 'Help', 'Water', 'Friend', 'Love', 'Yes', 'No'];
        const randomSign = signs[Math.floor(Math.random() * signs.length)];
        const confidence = Math.floor(Math.random() * 30) + 70; // 70-100%
        
        updateRecognitionResult(randomSign, confidence);
    }, 2000);
}

function stopRealtimeRecognition() {
    if (!recognitionActive) return;
    
    recognitionActive = false;
    clearInterval(recognitionInterval);
    console.log('Stopped realtime recognition');
}

function processFrame(canvas) {
    const resultContainer = document.getElementById('recognition-result');
    resultContainer.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-spin"></i> Processing image...</div>';
    
    // In a real app, you would send this to your recognition API
    // For demo purposes, we'll simulate processing
    setTimeout(() => {
        const signs = ['Hello', 'Thank you', 'Help', 'Water', 'Friend'];
        const randomSign = signs[Math.floor(Math.random() * signs.length)];
        const confidence = Math.floor(Math.random() * 30) + 70; // 70-100%
        
        updateRecognitionResult(randomSign, confidence);
    }, 1500);
}

function updateRecognitionResult(sign, confidence) {
    const resultContainer = document.getElementById('recognition-result');
    const confidenceClass = getConfidenceClass(confidence);
    
    resultContainer.innerHTML = `
        <div class="result-card">
            <h3>Recognized Sign</h3>
            <div class="sign-display">${sign}</div>
            <div class="confidence ${confidenceClass}">
                Confidence: ${confidence}%
            </div>
            <div class="result-actions">
                <button class="btn btn-outline" onclick="saveResult('${sign}', ${confidence})">
                    <i class="fas fa-save"></i> Save
                </button>
                <button class="btn btn-outline" onclick="shareResult('${sign}')">
                    <i class="fas fa-share-alt"></i> Share
                </button>
            </div>
        </div>
    `;
    
    // Add to history
    addToHistory(sign, confidence);
}

function getConfidenceClass(confidence) {
    if (confidence >= 90) return 'high';
    if (confidence >= 70) return 'medium';
    return 'low';
}

// ======================
// UI Update Functions
// ======================
function updateRecognitionUI(mode) {
    const realtimeSection = document.getElementById('realtime-section');
    const singleImageSection = document.getElementById('single-image-section');
    const videoUploadSection = document.getElementById('video-upload-section');
    
    // Hide all sections first
    if (realtimeSection) realtimeSection.style.display = 'none';
    if (singleImageSection) singleImageSection.style.display = 'none';
    if (videoUploadSection) videoUploadSection.style.display = 'none';
    
    // Show selected section
    switch (mode) {
        case 'realtime':
            if (realtimeSection) realtimeSection.style.display = 'block';
            break;
        case 'single':
            if (singleImageSection) singleImageSection.style.display = 'block';
            break;
        case 'video':
            if (videoUploadSection) videoUploadSection.style.display = 'block';
            break;
    }
    
    // Stop camera if switching from realtime mode
    if (mode !== 'realtime' && document.getElementById('start-camera').textContent.includes('Stop')) {
        stopCamera();
    }
}

function showSignLibrary() {
    // In a real app, this would fetch from an API
    const signs = [
        { sign: 'Hello', video: 'hello.mp4', image: 'hello.jpg', description: 'Open hand wave' },
        { sign: 'Thank you', video: 'thankyou.mp4', image: 'thankyou.jpg', description: 'Flat hand moves from chin outward' },
        { sign: 'Help', video: 'help.mp4', image: 'help.jpg', description: 'Thumb up with other hand on top' },
        { sign: 'Water', video: 'water.mp4', image: 'water.jpg', description: 'Wiggling fingers at chin' },
        { sign: 'Friend', video: 'friend.mp4', image: 'friend.jpg', description: 'Interlocking index fingers' }
    ];
    
    const libraryHTML = signs.map(sign => `
        <div class="sign-card">
            <div class="sign-media">
                <img src="assets/${sign.image}" alt="${sign.sign}">
                <button class="play-video" data-video="${sign.video}">
                    <i class="fas fa-play"></i>
                </button>
            </div>
            <div class="sign-info">
                <h4>${sign.sign}</h4>
                <p>${sign.description}</p>
            </div>
        </div>
    `).join('');
    
    const modalHTML = `
        <div class="modal-overlay">
            <div class="modal library-modal">
                <div class="modal-header">
                    <h3>Sign Language Library</h3>
                    <button class="close-modal">&times;</button>
                </div>
                <div class="modal-body">
                    <div class="signs-grid">
                        ${libraryHTML}
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    
    // Add event listeners
    const modalOverlay = document.querySelector('.modal-overlay');
    const closeBtn = document.querySelector('.close-modal');
    const playButtons = document.querySelectorAll('.play-video');
    
    closeBtn.addEventListener('click', () => {
        modalOverlay.remove();
    });
    
    modalOverlay.addEventListener('click', (e) => {
        if (e.target === modalOverlay) {
            modalOverlay.remove();
        }
    });
    
    playButtons.forEach(button => {
        button.addEventListener('click', function() {
            const videoFile = this.getAttribute('data-video');
            playSignVideo(videoFile);
        });
    });
}

function playSignVideo(videoFile) {
    const videoModalHTML = `
        <div class="video-modal-overlay">
            <div class="video-modal">
                <video controls autoplay>
                    <source src="assets/${videoFile}" type="video/mp4">
                </video>
                <button class="close-video-modal">&times;</button>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', videoModalHTML);
    
    const closeBtn = document.querySelector('.close-video-modal');
    closeBtn.addEventListener('click', () => {
        document.querySelector('.video-modal-overlay').remove();
    });
}

// ======================
// History Functions
// ======================
let historyIndex = -1;
let recognitionHistory = [];

function addToHistory(sign, confidence) {
    recognitionHistory.push({
        sign,
        confidence,
        timestamp: new Date()
    });
    
    historyIndex = recognitionHistory.length - 1;
    updateHistoryButtons();
}

function navigateHistory(e) {
    const direction = e.currentTarget.id.includes('back') ? -1 : 1;
    const newIndex = historyIndex + direction;
    
    if (newIndex >= 0 && newIndex < recognitionHistory.length) {
        historyIndex = newIndex;
        const item = recognitionHistory[historyIndex];
        updateRecognitionResult(item.sign, item.confidence);
        updateHistoryButtons();
    }
}

function updateHistoryButtons() {
    const historyBackBtn = document.getElementById('history-back');
    const historyForwardBtn = document.getElementById('history-forward');
    
    if (historyBackBtn) {
        historyBackBtn.disabled = historyIndex <= 0;
    }
    
    if (historyForwardBtn) {
        historyForwardBtn.disabled = historyIndex >= recognitionHistory.length - 1;
    }
}

// ======================
// Result Actions
// ======================
function saveResult(sign, confidence) {
    // In a real app, this would save to the user's account
    showAlert(`Saved "${sign}" to your history`, 'success');
    
    // Add to saved results list
    const savedList = document.getElementById('saved-results-list');
    if (savedList) {
        const now = new Date();
        const timeString = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        const newItem = document.createElement('div');
        newItem.className = 'saved-item';
        newItem.innerHTML = `
            <span class="sign">${sign}</span>
            <span class="time">${timeString}</span>
            <span class="confidence ${getConfidenceClass(confidence)}">${confidence}%</span>
            <button class="btn-icon" onclick="removeSavedItem(this)">
                <i class="fas fa-trash"></i>
            </button>
        `;
        
        savedList.appendChild(newItem);
    }
}

function shareResult(sign) {
    // In a real app, this would use the Web Share API or social media links
    if (navigator.share) {
        navigator.share({
            title: 'SignPro Recognition',
            text: `I just recognized the sign for "${sign}" using SignPro!`,
            url: window.location.href
        }).catch(err => {
            console.log('Error sharing:', err);
            showAlert('Could not share result', 'error');
        });
    } else {
        // Fallback for browsers without Share API
        showAlert('Share functionality not available in your browser', 'info');
    }
}

function removeSavedItem(button) {
    const item = button.closest('.saved-item');
    item.remove();
    showAlert('Removed from saved items', 'success');
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