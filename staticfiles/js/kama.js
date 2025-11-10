// JavaScript to handle the Kama Interest Form submission
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('kamaInterestForm');
    const messageDiv = document.getElementById('form-message');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const submitButton = form.querySelector('button[type="submit"]');
        const originalText = submitButton.textContent;
        
        // Show loading state
        submitButton.textContent = 'Sending...';
        submitButton.disabled = true;
        messageDiv.style.display = 'none';

        try {
            const formData = {
                full_name: form.querySelector('input[name="full_name"]').value,
                email: form.querySelector('input[name="email"]').value,
                phone: form.querySelector('input[name="phone"]').value,
                message: form.querySelector('textarea[name="message"]').value
            };

            const response = await fetch('{% url "ministries:kama_interest" %}', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token }}'
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (data.status === 'success') {
                showMessage(data.message, 'success');
                form.reset();
            } else {
                showMessage(data.message, 'error');
            }

        } catch (error) {
            showMessage('Network error. Please try again.', 'error');
        } finally {
            submitButton.textContent = originalText;
            submitButton.disabled = false;
        }
    });

    function showMessage(text, type) {
        messageDiv.textContent = text;
        messageDiv.style.display = 'block';
        messageDiv.className = type === 'success' ? 
            'alert alert-success' : 'alert alert-error';
    }
});


// JavaScript to handle the expand/collapse functionality
function toggleEventDetails(button) {
    const eventCard = button.closest('.event-card');
    const isExpanded = eventCard.classList.contains('expanded');
    
    // Close all other expanded cards
    const expandedCards = document.querySelectorAll('.event-card.expanded');
    expandedCards.forEach(card => {
        if (card !== eventCard) {
            card.classList.remove('expanded');
            const otherButton = card.querySelector('.event-button');
            if (otherButton) {
                const btnText = otherButton.querySelector('.btn-text');
                if (btnText) btnText.textContent = 'Details';
            }
        }
    });
    
    // Toggle current card
    if (isExpanded) {
        eventCard.classList.remove('expanded');
        const btnText = button.querySelector('.btn-text');
        if (btnText) btnText.textContent = 'Details';
    } else {
        eventCard.classList.add('expanded');
        const btnText = button.querySelector('.btn-text');
        if (btnText) btnText.textContent = 'Less Info';
        
        // Scroll to ensure the expanded content is visible
        eventCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
}

// Close expanded cards when clicking outside
document.addEventListener('click', function(e) {
    const isEventButton = e.target.classList.contains('event-button') || 
                        e.target.closest('.event-button');
    const isInsideExpandedCard = e.target.closest('.event-card.expanded');
    
    if (!isInsideExpandedCard && !isEventButton) {
        const expandedCards = document.querySelectorAll('.event-card.expanded');
        expandedCards.forEach(card => {
            card.classList.remove('expanded');
            const button = card.querySelector('.event-button');
            if (button) {
                const btnText = button.querySelector('.btn-text');
                if (btnText) btnText.textContent = 'Details';
            }
        });
    }
});

// Close expanded cards on escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        const expandedCards = document.querySelectorAll('.event-card.expanded');
        expandedCards.forEach(card => {
            card.classList.remove('expanded');
            const button = card.querySelector('.event-button');
            if (button) {
                const btnText = button.querySelector('.btn-text');
                if (btnText) btnText.textContent = 'Details';
            }
        });
    }
});

// Mobile navigation functionality
document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    const dropdowns = document.querySelectorAll('.dropdown');

    // Check if elements exist before adding event listeners
    if (hamburger && navLinks) {
        // Toggle mobile menu
        hamburger.addEventListener('click', function() {
            this.classList.toggle('active');
            navLinks.classList.toggle('show');
            
            // Close dropdowns when closing mobile menu
            if (!navLinks.classList.contains('show')) {
                dropdowns.forEach(dropdown => {
                    const menu = dropdown.querySelector('.dropdown-menu');
                    if (menu) menu.classList.remove('show');
                });
            }
        });
    }

    // Toggle dropdowns on mobile
    if (dropdowns.length > 0) {
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

    // Close dropdowns when clicking outside on mobile
    document.addEventListener('click', function(e) {
        if (window.innerWidth <= 768) {
            const isHamburger = e.target.closest('.hamburger');
            const isNavLink = e.target.closest('.nav-links');
            const isDropdown = e.target.closest('.dropdown');
            
            if (!isHamburger && !isNavLink && !isDropdown && navLinks && navLinks.classList.contains('show')) {
                navLinks.classList.remove('show');
                if (hamburger) hamburger.classList.remove('active');
                
                // Close all dropdowns
                dropdowns.forEach(dropdown => {
                    const menu = dropdown.querySelector('.dropdown-menu');
                    if (menu) menu.classList.remove('show');
                });
            }
        }
    });

    // Close mobile menu on resize to desktop
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768 && navLinks && navLinks.classList.contains('show')) {
            navLinks.classList.remove('show');
            if (hamburger) hamburger.classList.remove('active');
            
            // Close all dropdowns
            dropdowns.forEach(dropdown => {
                const menu = dropdown.querySelector('.dropdown-menu');
                if (menu) menu.classList.remove('show');
            });
        }
    });
});

// Smooth scrolling for anchor links
document.addEventListener('DOMContentLoaded', function() {
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
                        navLinks.classList.remove('show');
                        if (hamburger) hamburger.classList.remove('active');
                    }
                }
            }
        });
    });
});




