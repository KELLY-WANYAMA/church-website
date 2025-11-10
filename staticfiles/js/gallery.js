// gallery.js - Conflict-free gallery functionality
document.addEventListener('DOMContentLoaded', function() {
    // Only run if we're on a gallery page
    const gallerySection = document.querySelector('.gallery-section');
    if (!gallerySection) return;

    console.log('Gallery JS loaded');

    // Gallery filter functionality
    function handleGalleryFilter(category) {
        const baseUrl = window.location.pathname;
        let url = baseUrl;
        
        if (category !== 'all') {
            url += `?category=${category}`;
        }
        
        console.log('Filtering gallery to:', category);
        window.location.href = url;
    }

    // Set active category button
    function setActiveCategory() {
        const urlParams = new URLSearchParams(window.location.search);
        const currentCategory = urlParams.get('category') || 'all';
        const categoryButtons = document.querySelectorAll('.category-btn');
        
        categoryButtons.forEach(btn => {
            const btnCategory = btn.dataset.category;
            btn.classList.remove('active');
            
            if (btnCategory === currentCategory) {
                btn.classList.add('active');
            }
        });
    }

    // Initialize gallery
    function initGallery() {
        // Set active category on page load
        setActiveCategory();
        
        // Add click handlers to category buttons
        const categoryButtons = document.querySelectorAll('.category-btn');
        categoryButtons.forEach(btn => {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                const category = this.dataset.category;
                handleGalleryFilter(category);
            });
        });

        // Load more functionality (if needed)
        const loadMoreBtn = document.getElementById('loadMore');
        if (loadMoreBtn) {
            loadMoreBtn.addEventListener('click', function() {
                // Implement AJAX loading here if needed
                console.log('Load more clicked - implement AJAX loading');
            });
        }

        // Add smooth animations to gallery items
        const galleryItems = document.querySelectorAll('.gallery-item');
        galleryItems.forEach((item, index) => {
            item.style.animationDelay = `${index * 0.1}s`;
        });
    }

    // Initialize the gallery
    initGallery();
});