// Main JavaScript for ACK ST. JUDE'S HURUMA Website

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all functionality
    initNavigation();
    initEvents();
    initForms();
    initGallery();
    initEventFilters();
});

// ===== NAVIGATION FUNCTIONS =====
function initNavigation() {
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    const dropdowns = document.querySelectorAll('.dropdown');
    const body = document.body;

    // Mobile menu toggle
    if (hamburger) {
        hamburger.addEventListener('click', function(e) {
            e.stopPropagation();
            this.classList.toggle('active');
            navLinks.classList.toggle('show');
            body.classList.toggle('menu-open');
            
            // Prevent body scrolling when menu is open
            document.body.style.overflow = navLinks.classList.contains('show') ? 'hidden' : '';
        });
    }

    // Close menu when clicking on regular nav links (not dropdown toggles)
    document.querySelectorAll('.nav-links a:not(.dropdown > a)').forEach(link => {
        link.addEventListener('click', () => {
            hamburger.classList.remove('active');
            navLinks.classList.remove('show');
            body.classList.remove('menu-open');
            document.body.style.overflow = '';
        });
    });

    // Mobile dropdown functionality - FIXED VERSION
    document.querySelectorAll('.dropdown > a').forEach(dropdownToggle => {
        dropdownToggle.addEventListener('click', function(e) {
            if (window.innerWidth <= 768) {
                e.preventDefault();
                e.stopPropagation();
                
                const dropdownMenu = this.nextElementSibling;
                const isShowing = dropdownMenu.classList.contains('show');
                
                // Close all other dropdowns first
                document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
                    if (menu !== dropdownMenu) {
                        menu.classList.remove('show');
                    }
                });
                
                document.querySelectorAll('.dropdown > a.active').forEach(link => {
                    if (link !== this) {
                        link.classList.remove('active');
                    }
                });
                
                // Toggle current dropdown
                dropdownMenu.classList.toggle('show');
                this.classList.toggle('active');
                
                // Prevent the click from bubbling to document click handler
                return false;
            }
        });
    });

    // Close dropdowns when clicking on dropdown menu items
    document.querySelectorAll('.dropdown-menu a').forEach(dropdownLink => {
        dropdownLink.addEventListener('click', function(e) {
            if (window.innerWidth <= 768) {
                // Close the mobile menu when a dropdown item is clicked
                hamburger.classList.remove('active');
                navLinks.classList.remove('show');
                body.classList.remove('menu-open');
                document.body.style.overflow = '';
                
                // Close all dropdowns
                document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
                    menu.classList.remove('show');
                });
                document.querySelectorAll('.dropdown > a.active').forEach(link => {
                    link.classList.remove('active');
                });
            }
        });
    });

    // Close mobile menu when clicking outside - DELAYED for mobile dropdowns
    document.addEventListener('click', function(e) {
        if (window.innerWidth <= 768) {
            // Check if click is outside navbar and menu is open
            if (!e.target.closest('.navbar') && navLinks.classList.contains('show')) {
                // Small delay to ensure dropdown clicks are processed first
                setTimeout(() => {
                    hamburger.classList.remove('active');
                    navLinks.classList.remove('show');
                    body.classList.remove('menu-open');
                    document.body.style.overflow = '';
                    
                    // Close all dropdowns
                    document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
                        menu.classList.remove('show');
                    });
                    document.querySelectorAll('.dropdown > a.active').forEach(link => {
                        link.classList.remove('active');
                    });
                }, 10);
            }
            
            // Close dropdowns when clicking outside dropdown area (with delay)
            if (!e.target.closest('.dropdown') && !e.target.closest('.dropdown-menu')) {
                setTimeout(() => {
                    document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
                        menu.classList.remove('show');
                    });
                    document.querySelectorAll('.dropdown > a.active').forEach(link => {
                        link.classList.remove('active');
                    });
                }, 10);
            }
        }
    });

    // Desktop dropdown hover functionality
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

    // Close desktop dropdowns when clicking outside
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

    // Handle window resize
    window.addEventListener('resize', debounce(function() {
        if (window.innerWidth > 768) {
            // Close mobile menu when resizing to desktop
            hamburger.classList.remove('active');
            navLinks.classList.remove('show');
            body.classList.remove('menu-open');
            document.body.style.overflow = '';
            
            // Reset all dropdown menus to CSS control
            document.querySelectorAll('.dropdown-menu').forEach(menu => {
                menu.style.display = '';
                menu.classList.remove('show');
            });
            document.querySelectorAll('.dropdown > a.active').forEach(link => {
                link.classList.remove('active');
            });
        } else {
            // Ensure dropdowns are hidden on mobile resize
            document.querySelectorAll('.dropdown-menu').forEach(menu => {
                menu.style.display = '';
            });
        }
    }, 250));
}

// ===== EVENT FUNCTIONS =====
function initEvents() {
    // Event card expansion functionality
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
    // Close all other expanded cards
    document.querySelectorAll('.event-card.expanded').forEach(expandedCard => {
        if (expandedCard !== card) {
            expandedCard.classList.remove('expanded');
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

// ===== FORM FUNCTIONS =====
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

// ===== GALLERY FUNCTIONS =====
function initGallery() {
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
        border-radius: 8px;
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
        z-index: 10001;
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

// ===== EVENT FILTER FUNCTIONS =====
function initEventFilters() {
    // Add active class to current filter button
    const currentFilter = typeof current_filter !== 'undefined' ? current_filter.toLowerCase() : 'all';
    const filterButtons = document.querySelectorAll('.filter-btn');
    
    filterButtons.forEach(btn => {
        const btnFilter = btn.textContent.toLowerCase().includes('all') ? 'all' : 
                        btn.getAttribute('onclick') ? btn.getAttribute('onclick').match(/'([^']+)'/)[1] : 'all';
        if (btnFilter === currentFilter || 
            (currentFilter === 'all' && btnFilter === 'all')) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
}

// Global event filter function
function filterEvents(filter) {
    if (filter === 'all') {
        window.location.href = '{% url "events" %}';
    } else {
        window.location.href = '{% url "events" %}?filter=' + filter;
    }
}

// ===== UTILITY FUNCTIONS =====
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

// ===== GLOBAL EVENT LISTENERS =====
// Handle window resize for all components
window.addEventListener('resize', debounce(function() {
    // Close mobile menu on resize to larger screens
    if (window.innerWidth > 768) {
        const hamburger = document.querySelector('.hamburger');
        const navLinks = document.querySelector('.nav-links');
        const body = document.body;
        
        if (hamburger && navLinks) {
            hamburger.classList.remove('active');
            navLinks.classList.remove('show');
            body.classList.remove('menu-open');
            document.body.style.overflow = '';
        }
    }
}, 250));

// Escape key to close modals and menus
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        // Close mobile menu
        const hamburger = document.querySelector('.hamburger');
        const navLinks = document.querySelector('.nav-links');
        if (navLinks && navLinks.classList.contains('show')) {
            hamburger.classList.remove('active');
            navLinks.classList.remove('show');
            document.body.classList.remove('menu-open');
            document.body.style.overflow = '';
        }
        
        // Close lightbox
        const lightbox = document.querySelector('.lightbox');
        if (lightbox) {
            document.body.removeChild(lightbox);
        }
        
        // Close expanded event cards
        document.querySelectorAll('.event-card.expanded').forEach(card => {
            card.classList.remove('expanded');
            document.body.classList.remove('no-scroll');
        });
    }
});