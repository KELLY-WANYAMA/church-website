function filterEvents(eventType) {
    let url = new URL(window.location.href);
    
    if (eventType === 'all') {
        url.searchParams.delete('type');
    } else {
        url.searchParams.set('type', eventType);
    }
    
    window.location.href = url.toString();
}

// Add active class to current filter button and click handlers
document.addEventListener('DOMContentLoaded', function() {
    const currentFilter = '{{ current_filter }}' || 'all';
    const filterButtons = document.querySelectorAll('.filter-btn');
    
    // Add click event listeners to all filter buttons
    filterButtons.forEach(btn => {
        const filterType = btn.getAttribute('data-filter');
        
        btn.addEventListener('click', function() {
            filterEvents(filterType);
        });
        
        // Update active class
        if ((currentFilter === 'all' && filterType === 'all') || 
            (currentFilter === filterType)) {
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
    
    // Add loading state to filter buttons
    filterButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
            this.disabled = true;
        });
    });
});