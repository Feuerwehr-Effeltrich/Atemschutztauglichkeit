async function loadData() {
    const res = await fetch('/api.json');
    const data = await res.json();
    const div = document.getElementById('data');
    div.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
}

loadData();
