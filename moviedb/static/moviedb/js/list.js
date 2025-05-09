document.addEventListener('DOMContentLoaded', function() {
    // Initialize variables
    const searchForm = document.querySelector('.search-form');
    const searchInput = document.querySelector('.search-input');
    const filterForm = document.querySelector('.filter-form');
    const movieGrid = document.querySelector('.movie-grid');
    const loadingOverlay = document.createElement('div');
    loadingOverlay.className = 'loading-overlay';
    loadingOverlay.innerHTML = '<div class="loading-spinner"></div>';
    document.body.appendChild(loadingOverlay);

    // Debounce function for search
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

    // Show loading overlay
    function showLoading() {
        loadingOverlay.classList.add('active');
    }

    // Hide loading overlay
    function hideLoading() {
        loadingOverlay.classList.remove('active');
    }

    // Handle search with debounce
    const handleSearch = debounce(function(e) {
        if (e.target.value.length >= 2 || e.target.value.length === 0) {
            showLoading();
            searchForm.submit();
        }
    }, 500);

    // Add event listeners
    if (searchInput) {
        searchInput.addEventListener('input', handleSearch);
    }

    // Handle filter form submission
    if (filterForm) {
        filterForm.addEventListener('submit', function(e) {
            showLoading();
        });
    }

    // Lazy loading for images
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    const src = img.getAttribute('data-src');
                    if (src) {
                        img.src = src;
                        img.removeAttribute('data-src');
                    }
                    observer.unobserve(img);
                }
            });
        });

        document.querySelectorAll('.movie-poster img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }

    // Smooth scroll to top
    const scrollToTop = document.createElement('button');
    scrollToTop.innerHTML = '<i class="fas fa-arrow-up"></i>';
    scrollToTop.className = 'scroll-to-top';
    document.body.appendChild(scrollToTop);

    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            scrollToTop.classList.add('show');
        } else {
            scrollToTop.classList.remove('show');
        }
    });

    scrollToTop.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    // Add hover effect for movie cards
    const movieCards = document.querySelectorAll('.movie-card');
    movieCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 6px 12px rgba(0,0,0,0.15)';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 4px 6px rgba(0,0,0,0.1)';
        });
    });

    // Add animation for genre tags
    const genreTags = document.querySelectorAll('.genre-tag');
    genreTags.forEach(tag => {
        tag.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
        });

        tag.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });

    // Handle pagination clicks
    const paginationLinks = document.querySelectorAll('.page-link');
    paginationLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (!this.classList.contains('active')) {
                showLoading();
            }
        });
    });
}); 