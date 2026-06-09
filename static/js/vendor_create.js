const step1 = document.getElementById('step-1');
const step2 = document.getElementById('step-2');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const submitBtn = document.getElementById('submitBtn');
const progressLine = document.getElementById('progressLine');
const stepCircles = document.querySelectorAll('.step-circle');

// Dynamic file upload text and visual confirmation script logic
document.querySelectorAll('.custom-file-upload input[type="file"]').forEach(input => {
    input.addEventListener('change', function() {
        const wrapper = this.parentElement;
        const textLabel = wrapper.querySelector('.file-label-text');
        const icon = wrapper.querySelector('i');
        
        if (this.files && this.files.length > 0) {
            const fileName = this.files[0].name;
            textLabel.textContent = fileName;
            wrapper.classList.add('has-file');
            if(icon) icon.className = "fa-solid fa-circle-check";
        } else {
            textLabel.textContent = "Click to upload file";
            wrapper.classList.remove('has-file');
        }
    });
});

nextBtn.addEventListener('click', () => {
    const requiredFields = step1.querySelectorAll('input[required]');
    let isValid = true;
    requiredFields.forEach(field => {
        if(!field.value) {
            field.style.borderColor = '#ef4444';
            isValid = false;
        } else {
            field.style.borderColor = 'var(--border)';
        }
    });

    if (!isValid) return;

    step1.classList.remove('active');
    step2.classList.add('active');

    nextBtn.style.display = 'none';
    submitBtn.style.display = 'block';
    prevBtn.style.display = 'block';

    stepCircles[1].classList.add('active');
    stepCircles[0].classList.add('completed');
    progressLine.style.width = '100%';
});

prevBtn.addEventListener('click', () => {
    step2.classList.remove('active');
    step1.classList.add('active');

    nextBtn.style.display = 'block';
    submitBtn.style.display = 'none';
    prevBtn.style.display = 'none';

    stepCircles[1].classList.remove('active');
    stepCircles[0].classList.remove('completed');
    progressLine.style.width = '0%';
});