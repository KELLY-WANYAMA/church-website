function filterEvents(eventType) {
    let url = new URL(window.location.href);
    
    // Get the current path correctly
    const currentPath = window.location.pathname;
    
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
        
        // Update active class - fix comparison logic
        if ((currentFilter === 'all' && btnFilter === 'all') || 
            (currentFilter === btnFilter)) {
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