// youth.js - Conflict-free youth ministry functionality
document.addEventListener('DOMContentLoaded', function() {
    console.log('Youth Ministry JS loaded');

    // Parent subscription form handling
    function initializeParentSubscription() {
        const subscriptionForm = document.getElementById('parent-subscription-form');
        const messageDiv = document.getElementById('subscription-message');
        
        if (!subscriptionForm) return;

        subscriptionForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const email = formData.get('email');
            
            fetch('/youth/subscribe/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                },
                body: JSON.stringify({ email: email })
            })
            .then(response => response.json())
            .then(data => {
                messageDiv.textContent = data.message;
                messageDiv.style.display = 'block';
                
                if (data.success) {
                    messageDiv.className = 'success-message';
                    subscriptionForm.reset();
                } else {
                    messageDiv.className = 'error-message';
                }
                
                // Hide message after 5 seconds
                setTimeout(() => {
                    messageDiv.style.display = 'none';
                }, 5000);
            })
            .catch(error => {
                console.error('Error:', error);
                messageDiv.textContent = 'An error occurred. Please try again.';
                messageDiv.className = 'error-message';
                messageDiv.style.display = 'block';
            });
        });
    }

    // Event details toggle functionality
    function initializeEventToggles() {
        const eventButtons = document.querySelectorAll('.event-button');
        
        eventButtons.forEach(button => {
            // Remove any existing event listeners to prevent duplicates
            button.replaceWith(button.cloneNode(true));
        });

        // Re-select buttons after cloning
        const freshButtons = document.querySelectorAll('.event-button');
        
        freshButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                toggleEventDetails(this);
            });
        });

        console.log(`Initialized ${freshButtons.length} event buttons`);
    }

    // Single event toggle function
    function toggleEventDetails(button) {
        console.log('Toggle event details called for:', button);
        
        const eventCard = button.closest('.event-card');
        if (!eventCard) {
            console.error('No event card found for button:', button);
            return;
        }

        const btnText = button.querySelector('.btn-text');
        const chevron = button.querySelector('.fa-chevron-down, .fa-chevron-up');
        
        // Check if current card is already expanded
        const isCurrentlyExpanded = eventCard.classList.contains('expanded');
        
        // Close all other expanded cards first
        closeAllExpandedCards();
        
        // Toggle current card
        if (isCurrentlyExpanded) {
            // Close current card
            eventCard.classList.remove('expanded');
            if (btnText) btnText.textContent = 'Details';
            if (chevron) {
                chevron.classList.remove('fa-chevron-up');
                chevron.classList.add('fa-chevron-down');
            }
        } else {
            // Open current card
            eventCard.classList.add('expanded');
            if (btnText) btnText.textContent = 'Less Info';
            if (chevron) {
                chevron.classList.remove('fa-chevron-down');
                chevron.classList.add('fa-chevron-up');
            }
            
            // Smooth scroll to ensure the expanded content is visible
            setTimeout(() => {
                eventCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }, 100);
        }
    }

    // Close all expanded cards
    function closeAllExpandedCards() {
        const expandedCards = document.querySelectorAll('.event-card.expanded');
        expandedCards.forEach(card => {
            card.classList.remove('expanded');
            const button = card.querySelector('.event-button');
            if (button) {
                const btnText = button.querySelector('.btn-text');
                const chevron = button.querySelector('.fa-chevron-down, .fa-chevron-up');
                if (btnText) btnText.textContent = 'Details';
                if (chevron) {
                    chevron.classList.remove('fa-chevron-up');
                    chevron.classList.add('fa-chevron-down');
                }
            }
        });
    }

    // Close expanded cards when clicking outside
    function initializeOutsideClickHandler() {
        document.addEventListener('click', function(e) {
            const isEventButton = e.target.closest('.event-button');
            const isEventCard = e.target.closest('.event-card');
            
            if (!isEventButton && !isEventCard) {
                closeAllExpandedCards();
            }
        });
    }

    // Close expanded cards on escape key
    function initializeEscapeKeyHandler() {
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                closeAllExpandedCards();
            }
        });
    }

    // Smooth scrolling for internal anchor links (only for youth page)
    function initializeYouthSmoothScrolling() {
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
                    }
                }
            });
        });
    }

    // Initialize all youth-specific functionality
    function initYouthPage() {
        initializeParentSubscription();
        initializeEventToggles();
        initializeOutsideClickHandler();
        initializeEscapeKeyHandler();
        initializeYouthSmoothScrolling();
        
        console.log('Youth ministry page initialized successfully');
    }

    // Only initialize if we're on a youth page
    const youthSection = document.querySelector('.youth-section, .youth-hero');
    if (youthSection) {
        initYouthPage();
    }
});