document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('mothersUnionForm');
    const messageDiv = document.getElementById('form-message');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Show loading state
        const submitBtn = form.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        submitBtn.textContent = 'Submitting...';

        // Get form data
        const formData = new FormData(form);
        const data = {
            full_name: formData.get('full_name'),
            email: formData.get('email'),
            phone: formData.get('phone'),
            message: formData.get('message')
        };

        // Send to your Django view
        fetch('/submit-membership-interest/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            if (result.status === 'success') {
                showMessage(result.message, 'success');
                form.reset();
                
                // Redirect to WhatsApp
                redirectToWhatsApp(data);
            } else {
                showMessage(result.message, 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showMessage('An error occurred. Please try again.', 'error');
        })
        .finally(() => {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Submit Interest';
        });
    });

    function showMessage(message, type) {
        messageDiv.textContent = message;
        messageDiv.style.display = 'block';
        messageDiv.className = type === 'success' ? 'alert alert-success' : 'alert alert-danger';
        
        // Hide message after 5 seconds
        setTimeout(() => {
            messageDiv.style.display = 'none';
        }, 5000);
    }

    function redirectToWhatsApp(formData) {
        const secretaryPhone = '+254791675625'; // From your settings
        const message = `New Mother's Union Interest Form Submission:
        
Name: ${formData.full_name}
Email: ${formData.email}
Phone: ${formData.phone || 'Not provided'}
Message: ${formData.message}

Please follow up with this interested member.`;
        
        const encodedMessage = encodeURIComponent(message);
        const whatsappUrl = `https://wa.me/${secretaryPhone}?text=${encodedMessage}`;
        
        // Open WhatsApp in new tab after a short delay
        setTimeout(() => {
            window.open(whatsappUrl, '_blank');
        }, 1000);
    }
});
