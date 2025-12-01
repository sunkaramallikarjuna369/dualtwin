document.addEventListener('DOMContentLoaded', function() {
    const viewToggle = document.getElementById('viewToggle');
    const nonTechnical = document.querySelector('.non-technical');
    const technical = document.querySelector('.technical');
    let isTechnicalView = false;

    if (viewToggle && nonTechnical && technical) {
        viewToggle.addEventListener('click', function() {
            isTechnicalView = !isTechnicalView;
            if (isTechnicalView) {
                nonTechnical.classList.add('hidden');
                technical.classList.remove('hidden');
                viewToggle.textContent = 'Simple View';
            } else {
                nonTechnical.classList.remove('hidden');
                technical.classList.add('hidden');
                viewToggle.textContent = 'Technical View';
            }
        });
    }

    const steps = [
        '<strong>Step 1:</strong> Data is collected from physical systems through sensors and IoT devices.',
        '<strong>Step 2:</strong> Data is processed and synchronized with the digital twin model.',
        '<strong>Step 3:</strong> Analytics and insights are generated for decision-making.'
    ];

    let currentStep = 0;
    const prevBtn = document.getElementById('prevStep');
    const nextBtn = document.getElementById('nextStep');
    const stepIndicator = document.getElementById('stepIndicator');
    const stepDescription = document.getElementById('stepDescription');

    function updateStep() {
        if (stepIndicator) stepIndicator.textContent = 'Step ' + (currentStep + 1) + ' of ' + steps.length;
        if (stepDescription) stepDescription.innerHTML = '<p>' + steps[currentStep] + '</p>';
        if (prevBtn) prevBtn.disabled = currentStep === 0;
        if (nextBtn) nextBtn.disabled = currentStep === steps.length - 1;
    }

    if (prevBtn) prevBtn.addEventListener('click', function() {
        if (currentStep > 0) { currentStep--; updateStep(); }
    });

    if (nextBtn) nextBtn.addEventListener('click', function() {
        if (currentStep < steps.length - 1) { currentStep++; updateStep(); }
    });

    updateStep();
});