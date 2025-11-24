document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('mothersUnionForm');
    const messageDiv = document.getElementById('form-message');

    if (!form) {
        console.error('❌ Form element not found');
        return;
    }

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        console.log('📝 Form submission started');
        
        // Show loading state
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        submitBtn.disabled = true;
        submitBtn.textContent = 'Submitting...';
        submitBtn.style.opacity = '0.7';

        // Clear previous messages
        messageDiv.style.display = 'none';
        messageDiv.textContent = '';

        // Get form data
        const formData = new FormData(form);
        const data = {
            full_name: formData.get('full_name').trim(),
            email: formData.get('email').trim(),
            phone: formData.get('phone')?.trim() || '',
            message: formData.get('message').trim()
        };

        console.log('📝 Sending data:', data);

        // Get CSRF token
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        // Send to Django view
        fetch('/submit-membership-interest/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            console.log('📝 Response status:', response.status);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(result => {
            console.log('📝 Response data:', result);
            
            if (result.status === 'success') {
                showMessage(result.message, 'success');
                form.reset();
                
                // Redirect to WhatsApp after successful submission
                redirectToWhatsApp(data);
            } else {
                showMessage(result.message || 'An error occurred. Please try again.', 'error');
            }
        })
        .catch(error => {
            console.error('❌ Fetch error:', error);
            showMessage('Network error. Please check your connection and try again.', 'error');
        })
        .finally(() => {
            // Reset button state
            submitBtn.disabled = false;
            submitBtn.textContent = originalText;
            submitBtn.style.opacity = '1';
        });
    });

    function showMessage(message, type) {
        messageDiv.textContent = message;
        messageDiv.style.display = 'block';
        
        // Set appropriate styling
        if (type === 'success') {
            messageDiv.style.backgroundColor = '#d4edda';
            messageDiv.style.color = '#155724';
            messageDiv.style.border = '1px solid #c3e6cb';
        } else {
            messageDiv.style.backgroundColor = '#f8d7da';
            messageDiv.style.color = '#721c24';
            messageDiv.style.border = '1px solid #f5c6cb';
        }
        
        messageDiv.style.padding = '12px';
        messageDiv.style.borderRadius = '4px';
        messageDiv.style.marginTop = '15px';
        
        // Hide message after 8 seconds for success, 10 seconds for error
        const hideTime = type === 'success' ? 8000 : 10000;
        setTimeout(() => {
            messageDiv.style.display = 'none';
        }, hideTime);
    }

    function redirectToWhatsApp(formData) {
        const secretaryPhone = '254791675625'; // Remove + for WhatsApp URL
        const message = `🙏 New Mother's Union Membership Interest!

👤 Name: ${formData.full_name}
📧 Email: ${formData.email}
📞 Phone: ${formData.phone || 'Not provided'}

💬 Message:
${formData.message}

Please follow up within 48 hours. 🙏`;
        
        const encodedMessage = encodeURIComponent(message);
        const whatsappUrl = `https://wa.me/${secretaryPhone}?text=${encodedMessage}`;
        
        console.log('📱 WhatsApp URL:', whatsappUrl);
        
        // Open WhatsApp in new tab after a short delay
        setTimeout(() => {
            window.open(whatsappUrl, '_blank', 'noopener,noreferrer');
        }, 1500);
    }
});