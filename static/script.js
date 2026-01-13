async function sendQuery() {
    const queryInput = document.getElementById('queryInput');
    const searchBtn = document.getElementById('searchBtn');
    const btnText = document.getElementById('btnText');
    const loader = document.getElementById('loader');
    const resultContainer = document.getElementById('resultContainer');
    const responseContent = document.getElementById('responseContent');

    const query = queryInput.value.trim();
    if (!query) return;

    // UI Loading State
    searchBtn.disabled = true;
    btnText.textContent = "Planning Trip...";
    loader.classList.remove('hidden');
    resultContainer.classList.add('hidden');

    try {
        const response = await fetch('/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query: query })
        });

        if (!response.ok) {
            throw new Error(`Server Error: ${response.status}`);
        }

        const data = await response.json();
        
        // Render Markdown
        const rawMarkdown = data.answer;
        const cleanHtml = DOMPurify.sanitize(marked.parse(rawMarkdown));
        
        responseContent.innerHTML = cleanHtml;
        resultContainer.classList.remove('hidden');
        
        // Smooth scroll to result
        resultContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });

    } catch (error) {
        console.error('Error:', error);
        responseContent.innerHTML = `<p style="color: #ff6b6b; text-align: center;">⚠️ Something went wrong: ${error.message}. Please try again.</p>`;
        resultContainer.classList.remove('hidden');
    } finally {
        // Reset Button
        searchBtn.disabled = false;
        btnText.textContent = "Start Journey";
        loader.classList.add('hidden');
    }
}
