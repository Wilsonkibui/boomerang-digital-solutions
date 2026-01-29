/**
 * Main JavaScript for Boomerang Digital Solutions
 * Enhanced with modern animations and interactions
 */

// ===================================
// INITIALIZATION
// ===================================

document.addEventListener('DOMContentLoaded', function () {
    initMobileMenu();
    initScrollEffects();
    initScrollAnimations();
    initParallax();
    initAnimatedCounters();
    initFlashMessages();
    initSmoothScroll();
    initLoadingBar();
    initSearchAutocomplete();
});

// ===================================
// MOBILE MENU
// ===================================

function initMobileMenu() {
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const navMenu = document.getElementById('navMenu');

    if (mobileMenuToggle && navMenu) {
        mobileMenuToggle.addEventListener('click', function () {
            navMenu.classList.toggle('open');
        });

        // Close menu when clicking outside
        document.addEventListener('click', function (e) {
            if (!mobileMenuToggle.contains(e.target) && !navMenu.contains(e.target)) {
                navMenu.classList.remove('open');
            }
        });
    }
}

// ===================================
// SCROLL EFFECTS
// ===================================

function initScrollEffects() {
    const mainNav = document.getElementById('mainNav');
    if (!mainNav) return;

    let lastScroll = 0;

    window.addEventListener('scroll', function () {
        const currentScroll = window.scrollY;

        // Add scrolled class for styling
        if (currentScroll > 50) {
            mainNav.classList.add('scrolled');
        } else {
            mainNav.classList.remove('scrolled');
        }

        lastScroll = currentScroll;
    }, { passive: true });
}

// ===================================
// SCROLL ANIMATIONS (Intersection Observer)
// ===================================

function initScrollAnimations() {
    const animatedElements = document.querySelectorAll('.animate-on-scroll');

    if (animatedElements.length === 0) return;

    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
                // Optionally unobserve after animation
                // observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    animatedElements.forEach(el => observer.observe(el));
}

// ===================================
// PARALLAX EFFECT
// ===================================

function initParallax() {
    const parallaxElements = document.querySelectorAll('.parallax');

    if (parallaxElements.length === 0) return;

    window.addEventListener('scroll', function () {
        const scrolled = window.scrollY;

        parallaxElements.forEach(el => {
            const speed = el.dataset.speed || 0.5;
            const yPos = -(scrolled * speed);
            el.style.transform = `translateY(${yPos}px)`;
        });
    }, { passive: true });
}

// ===================================
// ANIMATED COUNTERS
// ===================================

function initAnimatedCounters() {
    const counters = document.querySelectorAll('[data-count]');

    if (counters.length === 0) return;

    const observerOptions = {
        threshold: 0.5
    };

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting && !entry.target.classList.contains('counted')) {
                animateCounter(entry.target);
                entry.target.classList.add('counted');
            }
        });
    }, observerOptions);

    counters.forEach(counter => observer.observe(counter));
}

function animateCounter(element) {
    const target = parseInt(element.dataset.count);
    const duration = 2000; // 2 seconds
    const increment = target / (duration / 16); // 60fps
    let current = 0;

    const updateCounter = () => {
        current += increment;
        if (current < target) {
            element.textContent = Math.floor(current);
            requestAnimationFrame(updateCounter);
        } else {
            element.textContent = target;
        }
    };

    updateCounter();
}

// ===================================
// SMOOTH SCROLL
// ===================================

function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href === '#') return;

            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// ===================================
// FLASH MESSAGES
// ===================================

function initFlashMessages() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s, transform 0.5s';
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-20px)';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });
}

// ===================================
// LOADING BAR
// ===================================

function initLoadingBar() {
    // Create loading bar element
    const loadingBar = document.createElement('div');
    loadingBar.className = 'loading-bar';
    loadingBar.id = 'loadingBar';
    document.body.appendChild(loadingBar);
}

function showLoadingBar() {
    const loadingBar = document.getElementById('loadingBar');
    if (loadingBar) {
        loadingBar.classList.add('loading');
    }
}

function hideLoadingBar() {
    const loadingBar = document.getElementById('loadingBar');
    if (loadingBar) {
        loadingBar.classList.remove('loading');
    }
}

// ===================================
// ADD TO CART
// ===================================

function addToCart(productId, redirect = '/cart') {
    showLoadingBar();

    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/cart/add';

    const productInput = document.createElement('input');
    productInput.type = 'hidden';
    productInput.name = 'product_id';
    productInput.value = productId;

    const redirectInput = document.createElement('input');
    redirectInput.type = 'hidden';
    redirectInput.name = 'redirect';
    redirectInput.value = redirect;

    const quantityInput = document.createElement('input');
    quantityInput.type = 'hidden';
    quantityInput.name = 'quantity';
    quantityInput.value = document.getElementById('quantity')?.value || 1;

    form.appendChild(productInput);
    form.appendChild(redirectInput);
    form.appendChild(quantityInput);

    document.body.appendChild(form);
    form.submit();
}

// ===================================
// UTILITY FUNCTIONS
// ===================================

function confirmDelete(message = 'Are you sure you want to delete this item?') {
    return confirm(message);
}

// Image Preview (for admin product forms)
function previewImages(input) {
    const preview = document.getElementById('imagePreview');
    if (!preview) return;

    preview.innerHTML = '';

    if (input.files) {
        Array.from(input.files).forEach((file, index) => {
            const reader = new FileReader();

            reader.onload = function (e) {
                const img = document.createElement('img');
                img.src = e.target.result;
                img.className = 'scale-in';
                img.style.width = '100px';
                img.style.height = '100px';
                img.style.objectFit = 'cover';
                img.style.borderRadius = 'var(--radius-md)';
                img.style.marginRight = 'var(--space-2)';
                img.style.marginBottom = 'var(--space-2)';
                preview.appendChild(img);
            };

            reader.readAsDataURL(file);
        });
    }
}

// Dynamic Spec Fields (for product form)
function addSpecField() {
    const container = document.getElementById('specsContainer');
    if (!container) return;

    const index = container.children.length;
    const div = document.createElement('div');
    div.className = 'flex gap-4 fade-in';
    div.style.marginBottom = 'var(--space-3)';
    div.innerHTML = `
        <input type="text" name="spec_keys[]" class="form-input" placeholder="Property (e.g. RAM)" style="flex: 1;">
        <input type="text" name="spec_values[]" class="form-input" placeholder="Value (e.g. 8GB)" style="flex: 1;">
        <button type="button" onclick="this.parentElement.remove()" class="btn btn-outline btn-sm">Remove</button>
    `;
    container.appendChild(div);
}

// ===================================
// SEARCH AUTOCOMPLETE
// ===================================

function initSearchAutocomplete() {
    const searchInput = document.querySelector('.search-input');
    if (!searchInput) return;

    let debounceTimer;
    let currentFocus = -1;
    let suggestionsContainer;

    // Create suggestions container
    const searchBar = searchInput.closest('.search-bar');
    if (!searchBar) return;

    suggestionsContainer = document.createElement('div');
    suggestionsContainer.className = 'search-suggestions';
    suggestionsContainer.style.display = 'none';
    searchBar.appendChild(suggestionsContainer);

    // Input event handler with debouncing
    searchInput.addEventListener('input', function () {
        const query = this.value.trim();

        clearTimeout(debounceTimer);

        if (query.length < 2) {
            hideSuggestions();
            return;
        }

        debounceTimer = setTimeout(() => {
            fetchSuggestions(query);
        }, 300);
    });

    // Keyboard navigation
    searchInput.addEventListener('keydown', function (e) {
        const suggestions = suggestionsContainer.querySelectorAll('.suggestion-item');

        if (e.key === 'ArrowDown') {
            e.preventDefault();
            currentFocus++;
            if (currentFocus >= suggestions.length) currentFocus = 0;
            setActive(suggestions);
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            currentFocus--;
            if (currentFocus < 0) currentFocus = suggestions.length - 1;
            setActive(suggestions);
        } else if (e.key === 'Enter') {
            if (currentFocus > -1 && suggestions[currentFocus]) {
                e.preventDefault();
                suggestions[currentFocus].click();
            }
        } else if (e.key === 'Escape') {
            hideSuggestions();
        }
    });

    // Close suggestions when clicking outside
    document.addEventListener('click', function (e) {
        if (!searchBar.contains(e.target)) {
            hideSuggestions();
        }
    });

    function fetchSuggestions(query) {
        fetch(`/api/search-suggestions?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                displaySuggestions(data);
            })
            .catch(error => {
                console.error('Error fetching suggestions:', error);
            });
    }

    function displaySuggestions(suggestions) {
        if (suggestions.length === 0) {
            hideSuggestions();
            return;
        }

        suggestionsContainer.innerHTML = '';
        currentFocus = -1;

        suggestions.forEach(product => {
            const item = document.createElement('a');
            item.href = `/product/${product.slug}`;
            item.className = 'suggestion-item';

            const imageUrl = product.image ? `/uploads/${product.image}` : '/assets/images/placeholder.png';

            item.innerHTML = `
                <img src="${imageUrl}" alt="${product.name}" class="suggestion-image" onerror="this.src='data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2248%22 height=%2248%22%3E%3Crect fill=%22%23f0f0f0%22 width=%2248%22 height=%2248%22/%3E%3C/svg%3E'">
                <div class="suggestion-info">
                    <div class="suggestion-name">${product.name}</div>
                    <div class="suggestion-meta">
                        <span class="suggestion-category">${product.category}</span>
                        <span class="suggestion-price">KES ${product.price.toLocaleString()}</span>
                    </div>
                </div>
            `;

            suggestionsContainer.appendChild(item);
        });

        suggestionsContainer.style.display = 'block';
    }

    function hideSuggestions() {
        suggestionsContainer.style.display = 'none';
        currentFocus = -1;
    }

    function setActive(suggestions) {
        removeActive(suggestions);
        if (currentFocus >= 0 && currentFocus < suggestions.length) {
            suggestions[currentFocus].classList.add('active');
        }
    }

    function removeActive(suggestions) {
        suggestions.forEach(item => item.classList.remove('active'));
    }
}

// ===================================
// BUTTON RIPPLE EFFECT
// ===================================

document.addEventListener('click', function (e) {
    if (e.target.classList.contains('btn-ripple') || e.target.closest('.btn-ripple')) {
        const button = e.target.classList.contains('btn-ripple') ? e.target : e.target.closest('.btn-ripple');
        const ripple = document.createElement('span');
        const rect = button.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;

        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.classList.add('ripple');

        button.appendChild(ripple);

        setTimeout(() => ripple.remove(), 600);
    }
});

