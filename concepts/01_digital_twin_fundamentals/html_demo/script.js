// Digital Twin Fundamentals - Interactive Demo

document.addEventListener('DOMContentLoaded', function() {
    // View Toggle
    const viewToggle = document.getElementById('viewToggle');
    const nonTechnical = document.querySelector('.non-technical');
    const technical = document.querySelector('.technical');
    let isTechnicalView = false;

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

    // Temperature Animation
    const physicalValue = document.getElementById('physicalValue');
    const twinValue = document.getElementById('twinValue');
    let temperature = 25;

    function updateTemperature() {
        temperature += (Math.random() - 0.5) * 2;
        temperature = Math.max(20, Math.min(35, temperature));
        
        physicalValue.textContent = temperature.toFixed(1) + '°C';
        
        setTimeout(() => {
            twinValue.textContent = temperature.toFixed(1) + '°C';
        }, 500);
    }

    setInterval(updateTemperature, 2000);

    // Architecture Steps
    const steps = [
        {
            layers: [1],
            arrows: [],
            description: '<strong>Step 1:</strong> Sensors on physical assets collect real-time data about temperature, pressure, vibration, and other parameters.'
        },
        {
            layers: [1, 2],
            arrows: [1],
            description: '<strong>Step 2:</strong> Data flows through IoT gateways that handle protocol translation, filtering, and initial processing.'
        },
        {
            layers: [1, 2, 3],
            arrows: [1, 2],
            description: '<strong>Step 3:</strong> The digital twin platform receives data, updates the virtual model, and runs analytics and simulations.'
        },
        {
            layers: [1, 2, 3, 4],
            arrows: [1, 2, 3],
            description: '<strong>Step 4:</strong> Insights are visualized through dashboards, 3D views, and alerts are generated based on rules and ML models.'
        },
        {
            layers: [1, 2, 3, 4, 5],
            arrows: [1, 2, 3, 4],
            description: '<strong>Step 5:</strong> Users make decisions based on insights, and control commands can be sent back to physical assets.'
        }
    ];

    let currentStep = 0;
    const prevBtn = document.getElementById('prevStep');
    const nextBtn = document.getElementById('nextStep');
    const stepIndicator = document.getElementById('stepIndicator');
    const stepDescription = document.getElementById('stepDescription');

    function updateArchitecture() {
        const step = steps[currentStep];
        
        for (let i = 1; i <= 5; i++) {
            const layer = document.getElementById('layer' + i);
            const arrow = document.getElementById('arrow' + i);
            
            if (step.layers.includes(i)) {
                layer.classList.add('active');
            } else {
                layer.classList.remove('active');
            }
            
            if (arrow) {
                if (step.arrows.includes(i)) {
                    arrow.classList.add('active');
                } else {
                    arrow.classList.remove('active');
                }
            }
        }
        
        stepIndicator.textContent = 'Step ' + (currentStep + 1) + ' of ' + steps.length;
        stepDescription.innerHTML = '<p>' + step.description + '</p>';
        
        prevBtn.disabled = currentStep === 0;
        nextBtn.disabled = currentStep === steps.length - 1;
    }

    prevBtn.addEventListener('click', function() {
        if (currentStep > 0) {
            currentStep--;
            updateArchitecture();
        }
    });

    nextBtn.addEventListener('click', function() {
        if (currentStep < steps.length - 1) {
            currentStep++;
            updateArchitecture();
        }
    });

    updateArchitecture();

    // Smooth scrolling for nav links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
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
});