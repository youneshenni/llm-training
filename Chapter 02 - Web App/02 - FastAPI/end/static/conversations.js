fetch('/api/conversation').then((response) => response.json()).then((data) => {
    const conversationList = document.getElementById('conversation-list');
    data.forEach((conversation) => {
        const listItem = document.createElement('li');
        listItem.textContent = `${conversation.name}`;
        listItem.addEventListener('click', () => {
            fetch(`/api/conversation/${conversation.id}`)
                .then((response) => response.json())
                .then((messages) => {
                    const messageList = document.getElementById('message-list');
                    messageList.innerHTML = '';
                    messages.forEach((message) => {
                        const messageItem = document.createElement('li');
                        messageItem.textContent = `${message.role}: ${message.content}`;
                        messageList.appendChild(messageItem);
                    });
                });
        });
        conversationList.appendChild(listItem);
    });
});