function toggleDetails(element) {
    const details = element.nextElementSibling;
    const icon = element.querySelector('.arrow i');
    details.style.display = details.style.display === 'block' ? 'none' : 'block';
    icon.classList.toggle('fa-caret-right');
    icon.classList.toggle('fa-caret-down');
}

async function updateData() {
    const button = document.getElementById('update-button');
    button.disabled = true;
    button.textContent = 'Aktualisiere...';

    try {
        await fetch('/update', { method: 'POST' });
        window.location.reload();
    } catch (error) {
        console.error('Fehler beim Aktualisieren der Daten:', error);
        button.disabled = false;
        button.textContent = 'Daten aktualisieren';
    }
}
