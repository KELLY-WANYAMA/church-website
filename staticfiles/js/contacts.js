    document.addEventListener('DOMContentLoaded', function() {
            const contactForm = document.getElementById('contactForm');
            const whatsappNote = document.getElementById('whatsappNote');
            
            // Show the WhatsApp note
            whatsappNote.style.display = 'block';
            
            contactForm.addEventListener('submit', function(e) {
                e.preventDefault();
                
                // Get form values
                const name = document.getElementById('name').value;
                const email = document.getElementById('email').value;
                const subject = document.getElementById('subject').value;
                const message = document.getElementById('message').value;
                
                // Format the message for WhatsApp
                const whatsappMessage = `New Message from ACK St. Judes Website:%0A%0A*Name:* ${data.name}%0A*Email:* ${data.email}%0A*Subject:* ${data.subject}%0A%0A*Message:*%0A${data.message}`;

                
                //INSERT HERE REAL WHATSAPP NUMBER
                // Create WhatsApp URL
                const whatsappURL = `https://wa.me/254791675625?text=${whatsappMessage}`;
                
                // Open WhatsApp in a new tab
                window.open(whatsappURL, '_blank');
                
                // Optional: Reset the form
                contactForm.reset();
                
                // Optional: Show a confirmation message
                alert('Thank you for your message! You will now be redirected to WhatsApp to send your message.');
            });
        });

     // Simple form validation
        document.getElementById('contactForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const subject = document.getElementById('subject').value;
            const message = document.getElementById('message').value;
            
            if (name && email && subject && message) {
                alert('Thank you for your message! We will get back to you soon.');
                document.getElementById('contactForm').reset();
            } else {
                alert('Please fill in all fields.');
            }
        });

document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    const dropdowns = document.querySelectorAll('.dropdown');

    // Toggle mobile menu
    hamburger.addEventListener('click', function() {
        this.classList.toggle('active');
        navLinks.classList.toggle('show');
    });

    // Toggle dropdowns on mobile
    dropdowns.forEach(dropdown => {
        const link = dropdown.querySelector('a');
        link.addEventListener('click', function(e) {
            if (window.innerWidth <= 768) {
                e.preventDefault();
                const menu = this.nextElementSibling;
                menu.classList.toggle('show');
            }
        });
    });
});
