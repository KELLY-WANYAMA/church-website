document.addEventListener('DOMContentLoaded', function() {
    
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




