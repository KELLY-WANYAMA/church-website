document.addEventListener('DOMContentLoaded', function() {
    // Mother's Union Form Submission
    const mothersUnionForm = document.getElementById('mothersUnionForm');
    if (mothersUnionForm) {
        mothersUnionForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const form = this;
            const formData = new FormData(form);
            const messageDiv = document.getElementById('form-message');
            const submitButton = form.querySelector('button[type="submit"]');
            const originalText = submitButton.textContent;
            
            // Show loading state
            submitButton.textContent = 'Sending...';
            submitButton.disabled = true;
            messageDiv.style.display = 'none';

            
            // In your JavaScript, use absolute path
            fetch("/ministries/submit-membership-interest/", {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'success') {
                    showMessage(data.message, 'success');
                    form.reset();
                } else {
                    showMessage(data.message, 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showMessage('Network error. Please try again.', 'error');
            })
            .finally(() => {
                submitButton.textContent = originalText;
                submitButton.disabled = false;
            });
        });

        function showMessage(text, type) {
            const messageDiv = document.getElementById('form-message');
            messageDiv.textContent = text;
            messageDiv.style.display = 'block';
            
            if (type === 'success') {
                messageDiv.style.backgroundColor = '#d4edda';
                messageDiv.style.color = '#155724';
                messageDiv.style.border = '1px solid #c3e6cb';
            } else {
                messageDiv.style.backgroundColor = '#f8d7da';
                messageDiv.style.color = '#721c24';
                messageDiv.style.border = '1px solid #f5c6cb';
            }
        }
    }

    // Event Cards Expand/Collapse
    function toggleEventDetails(button) {
        const eventCard = button.closest('.event-card');
        const isExpanded = eventCard.classList.contains('expanded');
        
        // Close all other expanded cards
        document.querySelectorAll('.event-card.expanded').forEach(card => {
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
            eventCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
    }

    // Attach event listeners to all event buttons
    document.querySelectorAll('.event-button').forEach(button => {
        button.addEventListener('click', function() {
            toggleEventDetails(this);
        });
    });

    // Close expanded cards when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.event-card') && !e.target.classList.contains('event-button')) {
            document.querySelectorAll('.event-card.expanded').forEach(card => {
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
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    const dropdowns = document.querySelectorAll('.dropdown');

    if (hamburger && navLinks) {
        hamburger.addEventListener('click', function() {
            this.classList.toggle('active');
            navLinks.classList.toggle('show');
        });
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#' && document.querySelector(href)) {
                e.preventDefault();
                document.querySelector(href).scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});




