        // Form Handler for Music Ministry Registration
    function initializeMusicMinistryForm() {
        const form = document.getElementById('musicMinistryForm');
        const messageDiv = document.getElementById('form-message');
        const submitBtn = document.getElementById('submitBtn');

        if (form) {
            form.addEventListener('submit', async function(e) {
                e.preventDefault();
                
                // Disable submit button
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
                
                // Get form data
                const formData = new FormData(form);
                const data = {
                    full_name: formData.get('full_name'),
                    phone: formData.get('phone'),
                    email: formData.get('email'),
                    team: formData.get('team'),
                    experience: formData.get('experience'),
                    instrument: formData.get('instrument'),
                    message: formData.get('message')
                };

                try {
                    const response = await fetch('/ministries/submit_music_ministry_registration/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
                        },
                        body: JSON.stringify(data)
                    });

                    const result = await response.json();

                    if (result.success) {
                        showMessage(messageDiv, result.message, 'success');
                        form.reset();
                    } else {
                        showMessage(messageDiv, result.message, 'error');
                    }
                } catch (error) {
                    showMessage(messageDiv, 'Network error. Please try again.', 'error');
                } finally {
                    // Re-enable submit button
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = '<i class="fab fa-whatsapp"></i> Send Registration';
                }
            });
        }
    }

    function showMessage(element, message, type) {
        element.textContent = message;
        element.className = `alert alert-${type}`;
        element.style.display = 'block';
        
        setTimeout(() => {
            element.style.display = 'none';
        }, 5000);
    }

    // Initialize when DOM is loaded
    document.addEventListener('DOMContentLoaded', function() {
        initializeMusicMinistryForm();
    });







    document.addEventListener('DOMContentLoaded', function() {
    // Mobile navigation functionality
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    const dropdowns = document.querySelectorAll('.dropdown');

    // Toggle mobile menu
    if (hamburger && navLinks) {
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

    // Smooth scrolling for anchor links
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
                    if (navLinks && navLinks.classList.contains('show')) {
                        navLinks.classList.remove('show');
                        if (hamburger) hamburger.classList.remove('active');
                    }
                }
            }
        });
    });

    // Tab functionality for age groups (if exists)
    const tabs = document.querySelectorAll('.age-tab');
    const contents = document.querySelectorAll('.age-content');

    if (tabs.length > 0) {
        tabs.forEach(tab => {
            tab.addEventListener('click', function() {
                const ageGroup = this.getAttribute('data-age');
                
                // Remove active class from all tabs and contents
                tabs.forEach(t => t.classList.remove('active'));
                contents.forEach(c => c.classList.remove('active'));
                
                // Add active class to clicked tab and corresponding content
                this.classList.add('active');
                document.getElementById(`${ageGroup}-content`).classList.add('active');
            });
        });
    }

    // Music Ministry form handling
    const musicForm = document.getElementById('musicMinistryForm');
    if (musicForm) {
        const messageDiv = document.getElementById('form-message');
        
        musicForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = {
                full_name: this.querySelector('input[name="full_name"]').value,
                phone: this.querySelector('input[name="phone"]').value,
                email: this.querySelector('input[name="email"]').value,
                team: this.querySelector('select[name="team"]').value,
                experience: this.querySelector('select[name="experience"]').value,
                instrument: this.querySelector('select[name="instrument"]').value,
                message: this.querySelector('textarea[name="message"]').value
            };

            // Validate phone number
            if (!isValidPhoneNumber(formData.phone)) {
                showMessage('Please enter a valid phone number', 'error');
                return;
            }

            // Create WhatsApp message
            const whatsappMessage = createWhatsAppMessage(formData);
            
            // Encode message for URL
            const encodedMessage = encodeURIComponent(whatsappMessage);
            
            // Replace with actual WhatsApp number of chairperson (remove spaces and special characters)
            const whatsappNumber = "254791675625"; // Example: 254712345678
            
            // Create WhatsApp link
            const whatsappUrl = `https://wa.me/${whatsappNumber}?text=${encodedMessage}`;
            
            // Open WhatsApp
            window.open(whatsappUrl, '_blank');
            
            // Show success message
            showMessage('Thank you! Opening WhatsApp to send your information to our chairperson.', 'success');
            
            // Reset form after a delay
            setTimeout(() => {
                this.reset();
                if (messageDiv) messageDiv.style.display = 'none';
            }, 5000);
        });

        function createWhatsAppMessage(data) {
            return `
Hello ACK Music Ministry Chairperson!

I would like to join the Music Ministry:

*Name:* ${data.full_name}
*Phone:* ${data.phone}
*Email:* ${data.email || 'Not provided'}
*Team:* ${getTeamName(data.team)}
*Experience Level:* ${data.experience}
*Instrument/Voice:* ${data.instrument}

*Message:*
${data.message}

Thank you!
            `.trim();
        }

        function getTeamName(teamValue) {
            const teams = {
                'choir': 'Choir Team',
                'praise': 'Praise & Worship Team',
                'both': 'Both Teams'
            };
            return teams[teamValue] || teamValue;
        }

        function showMessage(text, type) {
            if (messageDiv) {
                messageDiv.textContent = text;
                messageDiv.className = `alert alert-${type}`;
                messageDiv.style.display = 'block';
            }
        }
    }

    // Mother's Union form handling
    const mothersUnionForm = document.getElementById('mothersUnionForm');
    if (mothersUnionForm) {
        const messageDiv = document.getElementById('form-message');

        mothersUnionForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const submitButton = this.querySelector('button[type="submit"]');
            const originalText = submitButton.textContent;
            
            // Show loading state
            submitButton.textContent = 'Sending...';
            submitButton.disabled = true;
            if (messageDiv) messageDiv.style.display = 'none';

            try {
                const formData = {
                    full_name: this.querySelector('input[name="full_name"]').value,
                    email: this.querySelector('input[name="email"]').value,
                    phone: this.querySelector('input[name="phone"]').value,
                    message: this.querySelector('textarea[name="message"]').value
                };

                const response = await fetch('/ministries/mu/interest/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.querySelector('[name=csrfmiddlewaretoken]').value
                    },
                    body: JSON.stringify(formData)
                });

                const data = await response.json();

                if (data.status === 'success') {
                    showMUMessage(data.message, 'success');
                    this.reset();
                } else {
                    showMUMessage(data.message, 'error');
                }

            } catch (error) {
                showMUMessage('Network error. Please try again.', 'error');
            } finally {
                submitButton.textContent = originalText;
                submitButton.disabled = false;
            }
        });

        function showMUMessage(text, type) {
            if (messageDiv) {
                messageDiv.textContent = text;
                messageDiv.style.display = 'block';
                messageDiv.className = type === 'success' ? 
                    'alert alert-success' : 'alert alert-error';
            }
        }
    }

    // Event card expand/collapse functionality
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

    // Attach event listeners to all event buttons
    const eventButtons = document.querySelectorAll('.event-button');
    eventButtons.forEach(button => {
        button.addEventListener('click', function() {
            toggleEventDetails(this);
        });
    });

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

    // Phone validation function (used by multiple forms)
    function isValidPhoneNumber(phone) {
        // Basic validation for Kenyan numbers
        const phoneRegex = /^(\+?254|0)?[7][0-9]{8}$/;
        return phoneRegex.test(phone.replace(/\s/g, ''));
    }
});




