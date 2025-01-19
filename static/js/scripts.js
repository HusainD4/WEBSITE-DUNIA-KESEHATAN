document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('berlangganan-form');
    const notif = document.getElementById('notif');
    const notifNama = document.getElementById('notif-nama');
    const notifEmail = document.getElementById('notif-email');

    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();

            const nama = form.querySelector('input[name="nama"]').value;
            const email = form.querySelector('input[name="email"]').value;

            // Tampilkan notifikasi
            notifNama.textContent = nama;
            notifEmail.textContent = email;
            notif.classList.remove('d-none');
        });
    }
});




// Update chat order based on the selected option
function updateChatOrder(order) {
    const chatList = document.getElementById('chat-list');
    const chatItems = Array.from(chatList.querySelectorAll('.list-group-item'));

    // Sort items based on timestamp
    chatItems.sort((a, b) => {
        const timestampA = parseInt(a.getAttribute('data-timestamp'));
        const timestampB = parseInt(b.getAttribute('data-timestamp'));

        return order === 'newest' ? timestampB - timestampA : timestampA - timestampB;
    });

    // Re-append items to chat list
    chatList.innerHTML = '';
    chatItems.forEach(item => chatList.appendChild(item));
}
