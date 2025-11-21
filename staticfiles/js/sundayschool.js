// Main initialization when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeAllFunctions();
});

function initializeAllFunctions() {
    // Initialize all components
    initializeFormHandlers();
    initializeTabFunctionality();
    initializeMobileNavigation();
    initializeSmoothScrolling();
    initializeEventCards();
}

// FORM HANDLERS =============================================================
function initializeFormHandlers() {
    // Sunday School Registration Form
    const sundaySchoolForm = document.getElementById('sundaySchoolRegistrationForm');
    if (sundaySchoolForm) {
        // Use Django template tag for URL - FIXED
        setupFormHandler(sundaySchoolForm, '/ministries/submit_sunday_school_registration/', 'registration-message');
    }

    // Add other form handlers here as needed
    // Example: Youth registration, general contact forms, etc.
}

function setupFormHandler(form, submitUrl, messageDivId) {
    const messageDiv = document.getElementById(messageDivId);
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const submitButton = this.querySelector('button[type="submit"]');
        const originalText = submitButton.textContent;
        
        // Show loading state
        submitButton.textContent = 'Sending...';
        submitButton.disabled = true;
        if (messageDiv) messageDiv.style.display = 'none';

        try {
            const formData = new FormData(this);
            const formObject = {};
            
            // Convert FormData to object
            for (let [key, value] of formData.entries()) {
                formObject[key] = value;
            }

            console.log('Submitting to:', submitUrl); // Debug log
            console.log('Form data:', formObject); // Debug log

            const response = await fetch(submitUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify(formObject)
            });

            console.log('Response status:', response.status); // Debug log

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            console.log('Response data:', data); // Debug log

            if (data.success || data.status === 'success') {
                showMessage(data.message || 'Thank you! We will contact you soon.', 'success', messageDiv);
                this.reset();
            } else {
                showMessage(data.message || 'There was an error. Please try again.', 'error', messageDiv);
            }

            // Scroll to message if it exists
            if (messageDiv) {
                messageDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }

        } catch (error) {
            console.error('Full error details:', error);
            showMessage(`Network error: ${error.message}. Please check the console for details.`, 'error', messageDiv);
        } finally {
            // Restore button state
            submitButton.textContent = originalText;
            submitButton.disabled = false;
        }
    });
}

function getCSRFToken() {
    // Try to get CSRF token from template tag or form input
    const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
    if (csrfInput) {
        console.log('CSRF token found in input');
        return csrfInput.value;
    }
    
    // Fallback to cookie method
    const csrfCookie = getCookie('csrftoken');
    if (csrfCookie) {
        console.log('CSRF token found in cookie');
        return csrfCookie;
    }
    
    console.log('No CSRF token found');
    return '';
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function showMessage(text, type, messageDiv) {
    if (!messageDiv) return;
    
    messageDiv.textContent = text;
    messageDiv.style.display = 'block';
    
    // Apply styles based on message type
    if (type === 'success') {
        messageDiv.style.backgroundColor = '#d4edda';
        messageDiv.style.color = '#155724';
        messageDiv.style.border = '1px solid #c3e6cb';
    } else {
        messageDiv.style.backgroundColor = '#f8d7da';
        messageDiv.style.color = '#721c24';
        messageDiv.style.border = '1px solid #f5c6cb';
    }
    
    // Auto-hide success messages after 8 seconds
    if (type === 'success') {
        setTimeout(() => {
            messageDiv.style.display = 'none';
        }, 8000);
    }
}

// TAB FUNCTIONALITY =========================================================
function initializeTabFunctionality() {
    const tabs = document.querySelectorAll('.age-tab');
    const contents = document.querySelectorAll('.age-content');

    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const ageGroup = this.getAttribute('data-age');
            
            // Remove active class from all tabs and contents
            tabs.forEach(t => t.classList.remove('active'));
            contents.forEach(c => c.classList.remove('active'));
            
            // Add active class to clicked tab and corresponding content
            this.classList.add('active');
            const targetContent = document.getElementById(`${ageGroup}-content`);
            if (targetContent) targetContent.classList.add('active');
        });
    });
}

// EVENT CARDS FUNCTIONALITY =================================================
function initializeEventCards() {
    // Event cards are handled by the global toggleEventDetails function
}

function toggleEventDetails(button) {
    const eventCard = button.closest('.event-card');
    const isExpanded = eventCard.classList.contains('expanded');
    
    // Close all other expanded cards
    const expandedCards = document.querySelectorAll('.event-card.expanded');
    expandedCards.forEach(card => {
        if (card !== eventCard) {
            closeEventCard(card);
        }
    });
    
    // Toggle current card
    if (isExpanded) {
        closeEventCard(eventCard);
    } else {
        openEventCard(eventCard, button);
    }
}

function closeEventCard(card) {
    card.classList.remove('expanded');
    const button = card.querySelector('.event-button');
    if (button) {
        const btnText = button.querySelector('.btn-text');
        if (btnText) btnText.textContent = 'Details';
    }
}

function openEventCard(card, button) {
    card.classList.add('expanded');
    const btnText = button.querySelector('.btn-text');
    if (btnText) btnText.textContent = 'Less Info';
    
    // Scroll to ensure the expanded content is visible
    card.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Close expanded cards when clicking outside
document.addEventListener('click', function(e) {
    const isEventButton = e.target.classList.contains('event-button') || 
                        e.target.closest('.event-button');
    const isInsideExpandedCard = e.target.closest('.event-card.expanded');
    
    if (!isInsideExpandedCard && !isEventButton) {
        const expandedCards = document.querySelectorAll('.event-card.expanded');
        expandedCards.forEach(card => {
            closeEventCard(card);
        });
    }
});

// Close expanded cards on escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        const expandedCards = document.querySelectorAll('.event-card.expanded');
        expandedCards.forEach(card => {
            closeEventCard(card);
        });
    }
});



// SMOOTH SCROLLING ==========================================================
function initializeSmoothScrolling() {
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            if (href !== '#' && href.startsWith('#')) {
                e.preventDefault();
                const target = document.querySelector(href);
                
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                    
                    // Close mobile menu if open
                    const navLinks = document.querySelector('.nav-links');
                    const hamburger = document.querySelector('.hamburger');
                    if (navLinks && navLinks.classList.contains('show')) {
                        closeMobileMenu(navLinks, hamburger, document.querySelectorAll('.dropdown'));
                    }
                }
            }
        });
    });
}
<<<<<<< Updated upstream
=======

// SCROLL ANIMATIONS =========================================================
function initializeScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe elements for scroll animations
    document.querySelectorAll('.activity-card, .teacher-card, .schedule-card').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

// FORM ENHANCEMENTS =========================================================
function initializeFormEnhancements() {
    const formInputs = document.querySelectorAll('.interest-form input, .interest-form select, .interest-form textarea');
    
    formInputs.forEach(input => {
        // Add focus/blur effects
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            if (!this.value) {
                this.parentElement.classList.remove('focused');
            }
        });

        // Add character counter for textareas
        if (input.tagName === 'TEXTAREA') {
            const counter = document.createElement('div');
            counter.className = 'char-counter';
            counter.style.fontSize = '0.8rem';
            counter.style.color = 'var(--gray)';
            counter.style.textAlign = 'right';
            counter.style.marginTop = '0.5rem';
            input.parentNode.appendChild(counter);

            input.addEventListener('input', function() {
                const maxLength = this.getAttribute('maxlength') || 500;
                const currentLength = this.value.length;
                counter.textContent = `${currentLength}/${maxLength}`;
                
                if (currentLength > maxLength * 0.8) {
                    counter.style.color = 'var(--accent)';
                } else {
                    counter.style.color = 'var(--gray)';
                }
            });
        }
    });

    // Age validation and group suggestion
    const ageInput = document.querySelector('input[name="child_age"]');
    const ageGroupSelect = document.querySelector('select[name="age_group"]');

    if (ageInput && ageGroupSelect) {
        ageInput.addEventListener('input', function() {
            const age = parseInt(this.value);
            if (age >= 3 && age <= 12) {
                let suggestedGroup = '';
                if (age >= 3 && age <= 5) suggestedGroup = 'nursery';
                else if (age >= 6 && age <= 9) suggestedGroup = 'primary';
                else if (age >= 10 && age <= 12) suggestedGroup = 'juniors';
                
                ageGroupSelect.value = suggestedGroup;
            }
        });
    }
}

// IMAGE LOADING =============================================================
// Sunday School JavaScript - Fixed with image loading solutions

// Image preloading and cache busting
function preloadSundaySchoolImages() {
    console.log('Preloading Sunday School images...');
    
    const imageUrls = [
        '{% static "image/hero.jpg" %}',
        '{% static "image/KAMA.png" %}'
    ];
    
    imageUrls.forEach(url => {
        const img = new Image();
        // Add cache busting parameter
        img.src = url + '?v=1.2&t=' + new Date().getTime();
        img.onload = function() {
            console.log('Successfully loaded:', url);
        };
        img.onerror = function() {
            console.warn('Failed to load:', url);
            // Try without cache busting as fallback
            this.src = url;
        };
    });
}

// Reload images if they fail to load
function setupImageErrorHandling() {
    document.querySelectorAll('.sunday-school-page img').forEach(img => {
        const originalSrc = img.src;
        
        img.onerror = function() {
            console.warn('Image failed to load:', this.src);
            // Retry with cache busting
            if (!this.src.includes('?')) {
                this.src = originalSrc + '?t=' + new Date().getTime();
            } else if (!this.src.includes('t=')) {
                this.src = originalSrc + '&t=' + new Date().getTime();
            }
        };
        
        // Force reload if image is broken
        if (img.complete && img.naturalHeight === 0) {
            console.log('Reloading broken image:', img.src);
            img.src = img.src.split('?')[0] + '?t=' + new Date().getTime();
        }
    });
}

// Age group tabs functionality
function setupAgeTabs() {
    const tabs = document.querySelectorAll('.sunday-school-page .age-tab');
    const contents = document.querySelectorAll('.sunday-school-page .age-content');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const targetAge = this.getAttribute('data-age');
            
            // Remove active class from all tabs and contents
            tabs.forEach(t => t.classList.remove('active'));
            contents.forEach(c => c.classList.remove('active'));
            
            // Add active class to clicked tab and corresponding content
            this.classList.add('active');
            document.getElementById(`${targetAge}-content`).classList.add('active');
        });
    });
}

// Form submission handling
function setupRegistrationForm() {
    const form = document.getElementById('sundaySchoolRegistrationForm');
    const messageDiv = document.getElementById('registration-message');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const submitButton = this.querySelector('button[type="submit"]');
            
            // Disable submit button
            submitButton.disabled = true;
            submitButton.textContent = 'Registering...';
            
            // Simulate form submission (replace with actual AJAX call)
            setTimeout(() => {
                // Show success message
                showMessage('Registration submitted successfully! We will contact you soon.', 'success');
                
                // Reset form
                form.reset();
                
                // Re-enable submit button
                submitButton.disabled = false;
                submitButton.textContent = 'Register Now';
            }, 2000);
        });
    }
    
    function showMessage(text, type) {
        if (messageDiv) {
            messageDiv.textContent = text;
            messageDiv.className = type === 'success' ? 'message-success' : 'message-error';
            messageDiv.style.display = 'block';
            
            // Hide message after 5 seconds
            setTimeout(() => {
                messageDiv.style.display = 'none';
            }, 5000);
        }
    }
}

// Smooth scrolling for anchor links
function setupSmoothScrolling() {
    document.querySelectorAll('.sunday-school-page a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('Initializing Sunday School page...');
    
    // Preload images first
    preloadSundaySchoolImages();
    
    // Setup image error handling
    setupImageErrorHandling();
    
    // Initialize components
    setupAgeTabs();
    setupRegistrationForm();
    setupSmoothScrolling();
    
    // Force reload of hero background if needed
    const hero = document.querySelector('.sunday-school-page .sunday-hero');
    if (hero) {
        const currentBg = hero.style.backgroundImage;
        if (currentBg) {
            hero.style.backgroundImage = currentBg.replace(/\?v=([^&]*)/, '?v=1.2');
        }
    }
    
    console.log('Sunday School page initialized successfully');
});

// Additional image loading fallback
window.addEventListener('load', function() {
    console.log('Window loaded, final image check...');
    
    // Check for any images that might still be broken
    document.querySelectorAll('.sunday-school-page img').forEach(img => {
        if (img.complete && img.naturalHeight === 0) {
            console.log('Final attempt to load broken image:', img.src);
            const newSrc = img.src.split('?')[0] + '?final=' + new Date().getTime();
            img.src = newSrc;
        }
    });
});




// UTILITY FUNCTIONS =========================================================
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Export functions for global access if needed
window.toggleEventDetails = toggleEventDetails;
window.debounce = debounce;
>>>>>>> Stashed changes
