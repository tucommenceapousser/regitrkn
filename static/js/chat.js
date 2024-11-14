document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');
    const chatHistory = document.getElementById('chat-history');

    chatForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        const message = messageInput.value.trim();
        if (!message) return;

        // Add user message to chat
        appendMessage('Vous', message, 'user-message');
        messageInput.value = '';

        try {
            const response = await fetch('/get_advice', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': document.querySelector('input[name="csrf_token"]').value
                },
                body: `message=${encodeURIComponent(message)}`
            });

            const data = await response.json();
            appendMessage('Coach', data.response, 'coach-message');
        } catch (error) {
            console.error('Chat error:', error);
            appendMessage('Système', 'Une erreur de communication s\'est produite. Veuillez réessayer.', 'system-message');
        }

        chatHistory.scrollTop = chatHistory.scrollHeight;
    });

    function appendMessage(sender, message, className) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `mb-3`;
        messageDiv.innerHTML = `
            <div class="message ${className}">
                <strong>${sender}:</strong> ${message}
            </div>
        `;
        chatHistory.appendChild(messageDiv);
    }
});
