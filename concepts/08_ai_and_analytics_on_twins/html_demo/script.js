// DualTwin 360 - Interactive Demo
document.addEventListener('DOMContentLoaded', function() {
    // View Toggle
    const viewToggle = document.getElementById('viewToggle');
    const nonTechnical = document.querySelector('.non-technical');
    const technical = document.querySelector('.technical');
    let isTechnicalView = false;

    if (viewToggle) {
        viewToggle.addEventListener('click', function() {
            isTechnicalView = !isTechnicalView;
            if (isTechnicalView) {
                if (nonTechnical) nonTechnical.classList.add('hidden');
                if (technical) technical.classList.remove('hidden');
                viewToggle.textContent = 'Simple View';
            } else {
                if (nonTechnical) nonTechnical.classList.remove('hidden');
                if (technical) technical.classList.add('hidden');
                viewToggle.textContent = 'Technical View';
            }
        });
    }

    // Process Flow Animation
    const flowSteps = document.querySelectorAll('.flow-step');
    const runBtn = document.getElementById('runDemo') || document.getElementById('runCommDemo');
    const resetBtn = document.getElementById('resetDemo') || document.getElementById('resetCommDemo');
    let demoInterval = null;
    let currentStep = 0;

    function activateStep(index) {
        flowSteps.forEach((step, i) => {
            if (i <= index) {
                step.classList.add('active');
            } else {
                step.classList.remove('active');
            }
        });
    }

    function runDemo() {
        if (demoInterval) clearInterval(demoInterval);
        currentStep = 0;
        flowSteps.forEach(step => step.classList.remove('active'));
        
        demoInterval = setInterval(() => {
            if (currentStep < flowSteps.length) {
                activateStep(currentStep);
                currentStep++;
            } else {
                clearInterval(demoInterval);
            }
        }, 800);
    }

    function resetDemo() {
        if (demoInterval) clearInterval(demoInterval);
        currentStep = 0;
        flowSteps.forEach(step => step.classList.remove('active'));
    }

    if (runBtn) runBtn.addEventListener('click', runDemo);
    if (resetBtn) resetBtn.addEventListener('click', resetDemo);

    // Auto-run on scroll
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && flowSteps.length > 0) {
                setTimeout(runDemo, 500);
                observer.disconnect();
            }
        });
    }, { threshold: 0.3 });

    const howSection = document.getElementById('how');
    if (howSection) observer.observe(howSection);

    // Card hover effects
    document.querySelectorAll('.benefit-card, .card-item, .industry-slide').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) scale(1.02)';
        });
        card.addEventListener('mouseleave', function() {
            this.style.transform = '';
        });
    });

    // Smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    console.log('DualTwin 360 Demo Loaded!');
});
