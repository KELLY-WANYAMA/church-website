document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    const dropdowns = document.querySelectorAll('.dropdown');

    // Toggle mobile menu
    hamburger.addEventListener('click', function() {
        this.classList.toggle('active');
        navLinks.classList.toggle('show');
    });

    // Toggle dropdowns on mobile
    dropdowns.forEach(dropdown => {
        const link = dropdown.querySelector('a');
        link.addEventListener('click', function(e) {
            if (window.innerWidth <= 768) {
                e.preventDefault();
                const menu = this.nextElementSibling;
                menu.classList.toggle('show');
            }
        });
    });
});



function filterEvents(eventType) {
    let url = new URL(window.location.href);
    
    // Always start with the base events URL
    const basePath = '/events/';
    url.pathname = basePath;
    
    if (eventType === 'all') {
        url.searchParams.delete('type');
    } else {
        url.searchParams.set('type', eventType);
    }
    
    window.location.href = url.toString();
}

// Add active class to current filter button
document.addEventListener('DOMContentLoaded', function() {
    const currentFilter = '{{ current_filter }}'.toLowerCase();
    const filterButtons = document.querySelectorAll('.filter-btn');
    
    filterButtons.forEach(btn => {
        let btnFilter = 'all';
        const onclickAttr = btn.getAttribute('onclick');
        
        if (onclickAttr) {
            const match = onclickAttr.match(/'([^']+)'/);
            if (match && match[1]) {
                btnFilter = match[1].toLowerCase();
            }
        }
        
        // Update active class
        if (btnFilter === currentFilter) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
    
    // Add click handlers for video buttons to ensure they work
    const videoButtons = document.querySelectorAll('.video-btn');
    videoButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            // Allow default behavior (opening link)
            console.log('Video button clicked:', this.href);
        });
    });
});
