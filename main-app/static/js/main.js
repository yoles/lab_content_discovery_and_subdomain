// TechCorp Main JavaScript
console.log('TechCorp WebApp v2.1.4');
console.log('Environment: production');
console.log('Debug mode: disabled');

// Internal development note: Check dev.techcorp.local for debug mode
// Staging server: staging.techcorp.local
// Admin panel: admin.techcorp.local

document.addEventListener('DOMContentLoaded', function() {
    // Add fade-in animation to sections
    const sections = document.querySelectorAll('section');
    sections.forEach(section => {
        section.classList.add('fade-in');
    });

    // Contact form handling
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const formMessage = document.getElementById('formMessage');
            formMessage.innerHTML = `
                <div class="alert alert-info">
                    <i class="fas fa-info-circle"></i>
                    This is a demo form. In production, this would send your message to our team.
                </div>
            `;

            // Reset form
            setTimeout(() => {
                contactForm.reset();
                formMessage.innerHTML = '';
            }, 3000);
        });
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add active class to current nav item
    const currentLocation = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentLocation) {
            link.classList.add('active');
        }
    });

    // Console easter egg for curious pentesters
    console.log('%c🔍 Looking for hidden endpoints?', 'color: #0d6efd; font-size: 16px; font-weight: bold;');
    console.log('%cTry checking:', 'color: #6c757d; font-size: 14px;');
    console.log('  - /robots.txt');
    console.log('  - /sitemap.xml');
    console.log('  - /api/v1/info');
    console.log('  - Hidden subdomains?');
    console.log('%cHint: Subdomain enumeration might reveal interesting environments', 'color: #198754; font-size: 12px;');
});

// API endpoint discovery helper (for demonstration)
function checkAPIEndpoints() {
    const endpoints = [
        '/api/v1/info',
        '/api/v1/status',
        '/api/v2/admin/users', // Undocumented!
    ];

    console.log('Known API endpoints:');
    endpoints.forEach(endpoint => {
        console.log(`  - ${endpoint}`);
    });
}

// Developer tools detection
(function() {
    const devtools = {
        isOpen: false,
        orientation: null
    };

    const threshold = 160;
    const emitEvent = (isOpen, orientation) => {
        if (isOpen) {
            console.log('%c⚠️ Developer tools detected', 'color: #dc3545; font-weight: bold;');
            console.log('%cAre you a pentester? Check out our bug bounty program!', 'color: #0d6efd;');
        }
    };

    setInterval(() => {
        const widthThreshold = window.outerWidth - window.innerWidth > threshold;
        const heightThreshold = window.outerHeight - window.innerHeight > threshold;
        const orientation = widthThreshold ? 'vertical' : 'horizontal';

        if (!(heightThreshold && widthThreshold) &&
            ((window.Firebug && window.Firebug.chrome && window.Firebug.chrome.isInitialized) || widthThreshold || heightThreshold)) {
            if (!devtools.isOpen || devtools.orientation !== orientation) {
                emitEvent(true, orientation);
                devtools.isOpen = true;
                devtools.orientation = orientation;
            }
        } else {
            if (devtools.isOpen) {
                devtools.isOpen = false;
                devtools.orientation = null;
            }
        }
    }, 500);
})();

// Expose API helper in console
window.TechCorp = {
    version: '2.1.4',
    environment: 'production',
    checkAPI: checkAPIEndpoints,
    endpoints: {
        main: 'techcorp.local',
        dev: 'dev.techcorp.local',
        staging: 'staging.techcorp.local',
        admin: 'admin.techcorp.local'
    }
};
