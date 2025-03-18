// Main JavaScript file for the Email/SMS Spam Classifier

document.addEventListener('DOMContentLoaded', () => {
    console.log('Spam Classifier application loaded successfully!');
    
    // Get the message input element
    const messageInput = document.getElementById('message');
    
    // Auto-resize textarea based on content
    if (messageInput) {
        messageInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
        
        // Focus the input field when the page loads
        messageInput.focus();
    }
    
    // Add animation to result display
    const resultElement = document.querySelector('.result');
    if (resultElement) {
        // Add a slight delay before showing the result for a better user experience
        setTimeout(() => {
            resultElement.style.opacity = '0';
            resultElement.style.display = 'block';
            
            // Trigger reflow
            resultElement.offsetHeight;
            
            // Fade in the result
            resultElement.style.transition = 'opacity 0.5s ease-in-out';
            resultElement.style.opacity = '1';
        }, 300);
    }
}); 