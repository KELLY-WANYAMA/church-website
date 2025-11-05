// Main JavaScript for ACK ST. JUDE'S HURUMA Website

document.addEventListener('DOMContentLoaded', function() {
    // Navigation functionality
    initNavigation();
    
    // Event functionality
    initEvents();
    
    // Form functionality
    initForms();
    
    // Gallery functionality
    initGallery();
});

// Navigation Functions
function initNavigation() {
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    const dropdowns = document.querySelectorAll('.dropdown');

    // Toggle mobile menu
    if (hamburger) {
        hamburger.addEventListener('click', function() {
            this.classList.toggle('active');
            navLinks.classList.toggle('show');
            
            // Prevent body scrolling when menu is open
            document.body.style.overflow = navLinks.classList.contains('show') ? 'hidden' : '';
        });
    }

    // Toggle dropdowns on mobile
    dropdowns.forEach(dropdown => {
        const link = dropdown.querySelector('a');
        if (link) {
            link.addEventListener('click', function(e) {
                if (window.innerWidth <= 768) {
                    e.preventDefault();
                    const menu = this.nextElementSibling;
                    if (menu) {
                        menu.classList.toggle('show');
                    }
                }
            });
        }
    });

    // Close mobile menu when clicking outside
    document.addEventListener('click', function(e) {
        if (window.innerWidth <= 768 && navLinks.classList.contains('show')) {
            if (!e.target.closest('.navbar') && !e.target.closest('.nav-links')) {
                hamburger.classList.remove('active');
                navLinks.classList.remove('show');
                document.body.style.overflow = '';
            }
        }
    });

    // Close dropdowns when clicking outside on desktop
    document.addEventListener('click', function(e) {
        if (window.innerWidth > 768) {
            dropdowns.forEach(dropdown => {
                if (!dropdown.contains(e.target)) {
                    const menu = dropdown.querySelector('.dropdown-menu');
                    if (menu) {
                        menu.style.display = 'none';
                    }
                }
            });
        }
    });

    // Handle dropdown hover on desktop
    dropdowns.forEach(dropdown => {
        dropdown.addEventListener('mouseenter', function() {
            if (window.innerWidth > 768) {
                const menu = this.querySelector('.dropdown-menu');
                if (menu) {
                    menu.style.display = 'block';
                }
            }
        });

        dropdown.addEventListener('mouseleave', function() {
            if (window.innerWidth > 768) {
                const menu = this.querySelector('.dropdown-menu');
                if (menu) {
                    menu.style.display = 'none';
                }
            }
        });
    });
}

// Event Functions
function initEvents() {
    // Youth events expansion functionality
    const eventButtons = document.querySelectorAll('.event-button');
    
    eventButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const eventCard = this.closest('.event-card');
            if (eventCard) {
                toggleEventCard(eventCard);
            }
        });
    });

    // Event category filtering
    const filterButtons = document.querySelectorAll('.filter-btn, .category-btn');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            const category = this.getAttribute('data-category') || 'all';
            filterEvents(category, this);
        });
    });

    // Age tabs functionality for Sunday School
    const ageTabs = document.querySelectorAll('.age-tab');
    
    ageTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const target = this.getAttribute('data-target');
            switchAgeTab(target, this);
        });
    });
}

function toggleEventCard(card) {
    const isExpanded = card.classList.contains('expanded');
    
    // Close all other expanded cards
    document.querySelectorAll('.event-card.expanded').forEach(expandedCard => {
        if (expandedCard !== card) {
            expandedCard.classList.remove('expanded');
            document.body.classList.remove('no-scroll');
        }
    });
    
    // Toggle current card
    card.classList.toggle('expanded');
    
    if (card.classList.contains('expanded')) {
        document.body.classList.add('no-scroll');
    } else {
        document.body.classList.remove('no-scroll');
    }
}

function filterEvents(category, clickedButton) {
    // Update active button
    document.querySelectorAll('.filter-btn, .category-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    clickedButton.classList.add('active');
    
    // Filter logic would go here
    // This would depend on your specific event structure
    console.log('Filtering events by category:', category);
}

function switchAgeTab(target, clickedTab) {
    // Update active tab
    document.querySelectorAll('.age-tab').forEach(tab => {
        tab.classList.remove('active');
    });
    clickedTab.classList.add('active');
    
    // Show target content
    document.querySelectorAll('.age-content').forEach(content => {
        content.classList.remove('active');
    });
    
    const targetContent = document.getElementById(target);
    if (targetContent) {
        targetContent.classList.add('active');
    }
}

// Form Functions
function initForms() {
    const forms = document.querySelectorAll('.interest-form, .reg-form, .membership-form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            handleFormSubmission(this);
        });
    });
}

function handleFormSubmission(form) {
    const formData = new FormData(form);
    const submitButton = form.querySelector('button[type="submit"]');
    
    // Show loading state
    if (submitButton) {
        submitButton.disabled = true;
        submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
        form.classList.add('form-loading');
    }
    
    // Simulate form submission (replace with actual AJAX call)
    setTimeout(() => {
        showFormMessage(form, 'Thank you for your submission! We will get back to you soon.', 'success');
        
        // Reset form and button
        form.reset();
        if (submitButton) {
            submitButton.disabled = false;
            submitButton.innerHTML = 'Send Message <i class="fas fa-paper-plane"></i>';
            form.classList.remove('form-loading');
        }
    }, 2000);
}

function showFormMessage(form, message, type) {
    // Remove existing messages
    const existingMessage = form.querySelector('.alert');
    if (existingMessage) {
        existingMessage.remove();
    }
    
    // Create new message
    const messageDiv = document.createElement('div');
    messageDiv.className = `alert alert-${type}`;
    messageDiv.textContent = message;
    
    form.insertBefore(messageDiv, form.firstChild);
    
    // Auto-remove message after 5 seconds
    setTimeout(() => {
        messageDiv.remove();
    }, 5000);
}

// Gallery Functions
function initGallery() {
    // Lightbox functionality would go here
    // This is a basic implementation - you might want to use a library like Lightbox2
    
    const galleryItems = document.querySelectorAll('.gallery-item');
    
    galleryItems.forEach(item => {
        item.addEventListener('click', function() {
            const imgSrc = this.querySelector('img').src;
            openLightbox(imgSrc);
        });
    });
}

function openLightbox(imgSrc) {
    // Create lightbox overlay
    const lightbox = document.createElement('div');
    lightbox.className = 'lightbox';
    lightbox.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
        cursor: pointer;
    `;
    
    // Create image
    const img = document.createElement('img');
    img.src = imgSrc;
    img.style.cssText = `
        max-width: 90%;
        max-height: 90%;
        object-fit: contain;
    `;
    
    // Close button
    const closeBtn = document.createElement('button');
    closeBtn.innerHTML = '&times;';
    closeBtn.style.cssText = `
        position: absolute;
        top: 20px;
        right: 20px;
        background: none;
        border: none;
        color: white;
        font-size: 2rem;
        cursor: pointer;
    `;
    
    lightbox.appendChild(img);
    lightbox.appendChild(closeBtn);
    document.body.appendChild(lightbox);
    
    // Close lightbox
    lightbox.addEventListener('click', function(e) {
        if (e.target === lightbox || e.target === closeBtn) {
            document.body.removeChild(lightbox);
        }
    });
}

// Utility Functions
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

// Handle window resize
window.addEventListener('resize', debounce(function() {
    // Close mobile menu on resize to larger screens
    if (window.innerWidth > 768) {
        const hamburger = document.querySelector('.hamburger');
        const navLinks = document.querySelector('.nav-links');
        
        if (hamburger && navLinks) {
            hamburger.classList.remove('active');
            navLinks.classList.remove('show');
            document.body.style.overflow = '';
        }
    }
}, 250));





// Mobile menu functionality
const hamburger = document.querySelector('.hamburger');
const navLinks = document.querySelector('.nav-links');
const body = document.body;

hamburger.addEventListener('click', function() {
    this.classList.toggle('active');
    navLinks.classList.toggle('show');
    body.classList.toggle('menu-open');
});

// Close menu when<clicking>
    function filterEvents(filter) {
        if (filter === 'all') {
            window.location.href = '{% url "events" %}';
        } else {
            window.location.href = '{% url "events" %}?filter=' + filter;
        }
    }
    
    // Add active class to current filter button
    document.addEventListener('DOMContentLoaded', function() {
        const currentFilter = '{{ current_filter }}'.toLowerCase();
        const filterButtons = document.querySelectorAll('.filter-btn');
        
        filterButtons.forEach(btn => {
            const btnFilter = btn.textContent.toLowerCase().includes('all') ? 'all' : 
                            btn.getAttribute('onclick').match(/'([^']+)'/)[1];
            if (btnFilter === currentFilter || 
                (currentFilter === 'all' && btnFilter === 'all')) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });
    });
    
document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
        hamburger.classList.remove('active');
        navLinks.classList.remove('show');
        body.classList.remove('menu-open');
    });
});

// Close menu when clicking outside
document.addEventListener('click', function(event) {
    if (!event.target.closest('.navbar') && navLinks.classList.contains('show')) {
        hamburger.classList.remove('active');
        navLinks.classList.remove('show');
        body.classList.remove('menu-open');
    }
});




// Mobile dropdown functionality
document.querySelectorAll('.dropdown > a').forEach(dropdownToggle => {
    dropdownToggle.addEventListener('click', function(e) {
        if (window.innerWidth <= 768) {
            e.preventDefault();
            const dropdownMenu = this.nextElementSibling;
            dropdownMenu.classList.toggle('show');
        }
    });
});


    function filterEvents(filter) {
        if (filter === 'all') {
            window.location.href = '{% url "events" %}';
        } else {
            window.location.href = '{% url "events" %}?filter=' + filter;
        }
    }
    
    