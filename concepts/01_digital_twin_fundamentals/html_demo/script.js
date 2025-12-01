// Digital Twin Fundamentals - Interactive Demo

document.addEventListener('DOMContentLoaded', function() {
    // ===== VIEW TOGGLE =====
    const viewToggle = document.getElementById('viewToggle');
    const nonTechnical = document.querySelector('.non-technical');
    const technical = document.querySelector('.technical');
    let isTechnicalView = false;

    if (viewToggle) {
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

    // ===== FACTORY MACHINE SYNCHRONIZATION =====
    const physicalTemp = document.getElementById('physicalTemp');
    const digitalTemp = document.getElementById('digitalTemp');
    const physicalMotor = document.getElementById('physicalMotor');
    const digitalMotor = document.getElementById('digitalMotor');
    const physicalNeedle = document.getElementById('physicalNeedle');
    const digitalNeedle = document.getElementById('digitalNeedle');
    const tempSlider = document.getElementById('tempSlider');
    const speedSlider = document.getElementById('speedSlider');
    const tempValue = document.getElementById('tempValue');
    const speedValue = document.getElementById('speedValue');
    const alertBtn = document.getElementById('alertBtn');
    const steamContainer = document.getElementById('steamContainer');

    let currentTemp = 25;
    let currentSpeed = 50;
    let isAlert = false;

    function updateMachineState() {
        // Update temperature displays
        const tempClass = currentTemp > 80 ? 'danger' : currentTemp > 60 ? 'warning' : '';
        
        if (physicalTemp) {
            physicalTemp.textContent = currentTemp + '°C';
            physicalTemp.className = 'temp-display ' + tempClass;
        }
        
        // Sync digital twin with slight delay for realism
        setTimeout(() => {
            if (digitalTemp) {
                digitalTemp.textContent = currentTemp + '°C';
                digitalTemp.className = 'temp-display ' + tempClass;
            }
        }, 200);

        // Update motor speed
        const spinDuration = Math.max(0.2, 4 - (currentSpeed / 25));
        if (physicalMotor) {
            physicalMotor.style.animationDuration = spinDuration + 's';
        }
        setTimeout(() => {
            if (digitalMotor) {
                digitalMotor.style.animationDuration = spinDuration + 's';
            }
        }, 200);

        // Update gauge needles
        const needleRotation = -45 + (currentSpeed * 0.9);
        if (physicalNeedle) {
            physicalNeedle.style.transform = `translateX(-50%) rotate(${needleRotation}deg)`;
        }
        setTimeout(() => {
            if (digitalNeedle) {
                digitalNeedle.style.transform = `translateX(-50%) rotate(${needleRotation}deg)`;
            }
        }, 200);

        // Show steam when hot
        if (steamContainer) {
            steamContainer.style.opacity = currentTemp > 60 ? '1' : '0';
        }
    }

    // Temperature slider
    if (tempSlider) {
        tempSlider.addEventListener('input', function() {
            currentTemp = parseInt(this.value);
            if (tempValue) tempValue.textContent = currentTemp + '°C';
            updateMachineState();
        });
    }

    // Speed slider
    if (speedSlider) {
        speedSlider.addEventListener('input', function() {
            currentSpeed = parseInt(this.value);
            if (speedValue) speedValue.textContent = currentSpeed + '%';
            updateMachineState();
        });
    }

    // Alert simulation
    if (alertBtn) {
        alertBtn.addEventListener('click', function() {
            isAlert = !isAlert;
            const machines = document.querySelectorAll('.factory-machine');
            
            if (isAlert) {
                // Trigger alert state
                currentTemp = 95;
                if (tempSlider) tempSlider.value = 95;
                if (tempValue) tempValue.textContent = '95°C';
                
                machines.forEach(m => {
                    m.style.animation = 'alertShake 0.5s ease-in-out infinite';
                });
                
                alertBtn.textContent = 'Clear Alert';
                alertBtn.style.background = 'linear-gradient(135deg, #10b981, #059669)';
            } else {
                // Clear alert
                currentTemp = 25;
                if (tempSlider) tempSlider.value = 25;
                if (tempValue) tempValue.textContent = '25°C';
                
                machines.forEach(m => {
                    m.style.animation = '';
                });
                
                alertBtn.textContent = 'Simulate Alert';
                alertBtn.style.background = 'linear-gradient(135deg, #ef4444, #dc2626)';
            }
            
            updateMachineState();
        });
    }

    // Add alert shake animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes alertShake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-5px); }
            75% { transform: translateX(5px); }
        }
    `;
    document.head.appendChild(style);

    // Initialize machine state
    updateMachineState();

    // ===== SMART BUILDING WINDOW ANIMATION =====
    function animateWindows() {
        const windows = document.querySelectorAll('.smart-building .window');
        windows.forEach(w => {
            if (Math.random() > 0.7) {
                w.classList.toggle('on');
            }
        });
    }
    setInterval(animateWindows, 2000);

    // ===== ROLE CARDS INTERACTION =====
    const roleCards = document.querySelectorAll('.role-card');
    roleCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            roleCards.forEach(c => c.classList.remove('active'));
            this.classList.add('active');
        });
    });

    // ===== PROCESS FLOW ANIMATION =====
    const flowSteps = document.querySelectorAll('.flow-step');
    const runDemoBtn = document.getElementById('runDemo');
    const resetDemoBtn = document.getElementById('resetDemo');
    let demoInterval = null;
    let currentFlowStep = 0;

    function activateStep(index) {
        flowSteps.forEach((step, i) => {
            if (i <= index) {
                step.classList.add('active');
            } else {
                step.classList.remove('active');
            }
        });
    }

    function runProcessDemo() {
        if (demoInterval) clearInterval(demoInterval);
        currentFlowStep = 0;
        
        // Reset all steps
        flowSteps.forEach(step => step.classList.remove('active'));
        
        // Animate through steps
        demoInterval = setInterval(() => {
            if (currentFlowStep < flowSteps.length) {
                activateStep(currentFlowStep);
                currentFlowStep++;
            } else {
                clearInterval(demoInterval);
                // Flash all steps
                setTimeout(() => {
                    flowSteps.forEach(step => {
                        step.style.transition = 'all 0.3s';
                        step.style.transform = 'scale(1.05)';
                    });
                    setTimeout(() => {
                        flowSteps.forEach(step => {
                            step.style.transform = 'scale(1)';
                        });
                    }, 300);
                }, 500);
            }
        }, 1000);
    }

    function resetDemo() {
        if (demoInterval) clearInterval(demoInterval);
        currentFlowStep = 0;
        flowSteps.forEach(step => step.classList.remove('active'));
    }

    if (runDemoBtn) {
        runDemoBtn.addEventListener('click', runProcessDemo);
    }

    if (resetDemoBtn) {
        resetDemoBtn.addEventListener('click', resetDemo);
    }

    // Auto-run demo on scroll into view
    const howSection = document.getElementById('how');
    let hasRunDemo = false;
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !hasRunDemo) {
                hasRunDemo = true;
                setTimeout(runProcessDemo, 500);
            }
        });
    }, { threshold: 0.3 });

    if (howSection) {
        observer.observe(howSection);
    }

    // ===== BENEFIT CARDS HOVER EFFECTS =====
    const benefitDemos = document.querySelectorAll('.benefit-demo');
    benefitDemos.forEach(demo => {
        demo.addEventListener('mouseenter', function() {
            const animation = this.querySelector('.benefit-animation');
            if (animation) {
                animation.style.transform = 'scale(1.1)';
            }
        });
        demo.addEventListener('mouseleave', function() {
            const animation = this.querySelector('.benefit-animation');
            if (animation) {
                animation.style.transform = 'scale(1)';
            }
        });
    });

    // ===== INDUSTRY CARDS INTERACTION =====
    const industryCards = document.querySelectorAll('.industry-card');
    industryCards.forEach(card => {
        card.addEventListener('click', function() {
            const industry = this.dataset.industry;
            
            // Add click feedback
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'translateY(-5px)';
            }, 150);
            
            // Could expand to show more details
            console.log('Selected industry:', industry);
        });
    });

    // ===== SMOOTH SCROLLING =====
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

    // ===== PARALLAX EFFECT ON SCROLL =====
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const header = document.querySelector('header');
        if (header) {
            header.style.backgroundPositionY = scrolled * 0.5 + 'px';
        }
    });

    // ===== RANDOM DATA PACKET ANIMATION =====
    function randomizePackets() {
        const packets = document.querySelectorAll('.data-packet');
        packets.forEach((packet, i) => {
            const delay = Math.random() * 2;
            packet.style.animationDelay = delay + 's';
        });
    }
    setInterval(randomizePackets, 6000);

    // ===== SENSOR DOT PULSE SYNC =====
    function syncSensorPulse() {
        const sensors = document.querySelectorAll('.sensor-dot');
        sensors.forEach((sensor, i) => {
            sensor.style.animationDelay = (i * 0.2) + 's';
        });
    }
    syncSensorPulse();

    console.log('Digital Twin Fundamentals Demo Loaded Successfully!');
});
