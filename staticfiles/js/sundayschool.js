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
    initializeScrollAnimations();
    initializeFormEnhancements();
    initializeImageLoading();
}

// FORM HANDLERS =============================================================
function initializeFormHandlers() {
    // Sunday School Registration Form
    const sundaySchoolForm = document.getElementById('sundaySchoolRegistrationForm');
    if (sundaySchoolForm) {
        setupFormHandler(sundaySchoolForm, '/ministries/submit_sunday_school_registration/', 'registration-message');
    }

    // Add other form handlers here as needed
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

            console.log('Submitting to:', submitUrl);
            console.log('Form data:', formObject);

            const response = await fetch(submitUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify(formObject)
            });

            console.log('Response status:', response.status);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            console.log('Response data:', data);

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
        return csrfInput.value;
    }
    
    // Fallback to cookie method
    const csrfCookie = getCookie('csrftoken');
    if (csrfCookie) {
        return csrfCookie;
    }
    
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
    
    // Apply modern styles based on message type
    if (type === 'success') {
        messageDiv.className = 'message-success';
        messageDiv.style.backgroundColor = '#d4edda';
        messageDiv.style.color = '#155724';
        messageDiv.style.border = '1px solid #c3e6cb';
    } else {
        messageDiv.className = 'message-error';
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
    const ageTabs = document.querySelectorAll('.age-tab');
    const ageContents = document.querySelectorAll('.age-content');

    ageTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const ageGroup = this.getAttribute('data-age');
            
            // Remove active class from all tabs and contents
            ageTabs.forEach(t => t.classList.remove('active'));
            ageContents.forEach(c => c.classList.remove('active'));
            
            // Add active class to clicked tab and corresponding content
            this.classList.add('active');
            const targetContent = document.getElementById(`${ageGroup}-content`);
            if (targetContent) targetContent.classList.add('active');
        });
    });

    // Keyboard navigation for age tabs
    document.addEventListener('keydown', function(e) {
        if (e.target.classList.contains('age-tab')) {
            if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
                e.preventDefault();
                const nextTab = e.target.nextElementSibling || ageTabs[0];
                nextTab.click();
                nextTab.focus();
            } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
                e.preventDefault();
                const prevTab = e.target.previousElementSibling || ageTabs[ageTabs.length - 1];
                prevTab.click();
                prevTab.focus();
            }
        }
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

// MOBILE NAVIGATION =========================================================
function initializeMobileNavigation() {
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    const dropdowns = document.querySelectorAll('.dropdown');

    // Mobile menu toggle
    if (hamburger && navLinks) {
        hamburger.addEventListener('click', function() {
            this.classList.toggle('active');
            navLinks.classList.toggle('show');
            
            // Close dropdowns when closing mobile menu
            if (!navLinks.classList.contains('show')) {
                closeAllDropdowns(dropdowns);
            }
        });
    }

    // Dropdown functionality for mobile
    setupMobileDropdowns(dropdowns);

    // Close mobile menu when clicking outside
    setupClickOutsideHandler(hamburger, navLinks, dropdowns);

    // Close mobile menu on resize to desktop
    setupResizeHandler(navLinks, hamburger, dropdowns);
}

function setupMobileDropdowns(dropdowns) {
    dropdowns.forEach(dropdown => {
        const link = dropdown.querySelector('a');
        if (link) {
            link.addEventListener('click', function(e) {
                if (window.innerWidth <= 768) {
                    e.preventDefault();
                    const menu = this.nextElementSibling;
                    if (menu && menu.classList.contains('dropdown-menu')) {
                        menu.classList.toggle('show');
                        
                        // Close other dropdowns
                        dropdowns.forEach(otherDropdown => {
                            if (otherDropdown !== dropdown) {
                                const otherMenu = otherDropdown.querySelector('.dropdown-menu');
                                if (otherMenu) otherMenu.classList.remove('show');
                            }
                        });
                    }
                }
            });
        }
    });
}

function setupClickOutsideHandler(hamburger, navLinks, dropdowns) {
    document.addEventListener('click', function(e) {
        if (window.innerWidth <= 768) {
            const isHamburger = e.target.closest('.hamburger');
            const isNavLink = e.target.closest('.nav-links');
            const isDropdown = e.target.closest('.dropdown');
            
            if (!isHamburger && !isNavLink && !isDropdown && navLinks && navLinks.classList.contains('show')) {
                closeMobileMenu(navLinks, hamburger, dropdowns);
            }
        }
    });
}

function setupResizeHandler(navLinks, hamburger, dropdowns) {
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768 && navLinks && navLinks.classList.contains('show')) {
            closeMobileMenu(navLinks, hamburger, dropdowns);
        }
    });
}

function closeMobileMenu(navLinks, hamburger, dropdowns) {
    navLinks.classList.remove('show');
    if (hamburger) hamburger.classList.remove('active');
    closeAllDropdowns(dropdowns);
}

function closeAllDropdowns(dropdowns) {
    dropdowns.forEach(dropdown => {
        const menu = dropdown.querySelector('.dropdown-menu');
        if (menu) menu.classList.remove('show');
    });
}

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
function initializeImageLoading() {
    document.querySelectorAll('img').forEach(img => {
        img.addEventListener('load', function() {
            this.style.opacity = '1';
        });
        
        img.style.opacity = '0';
        img.style.transition = 'opacity 0.3s ease';
    });
}

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