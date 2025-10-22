function toggleDetails(element) {
    const details = element.nextElementSibling;
    if (details.style.display === "block") {
        details.style.display = "none";
        element.querySelector('.arrow').textContent = '▶';
    } else {
        details.style.display = "block";
        element.querySelector('.arrow').textContent = '▼';
    }
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
