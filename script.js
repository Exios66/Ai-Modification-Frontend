document.addEventListener('DOMContentLoaded', () => {
    const themeToggleBtn = document.getElementById('theme-toggle');
    const body = document.body;
    const form = document.getElementById('assessment-form');
    const resultsSection = document.getElementById('results');
    const aiResponseDiv = document.getElementById('ai-response');
    const userGroupDiv = document.getElementById('user-group');

    // Theme Toggle Functionality
    themeToggleBtn.addEventListener('click', () => {
        body.classList.toggle('dark-theme');
        toggleThemeIcon();
    });

    function toggleThemeIcon() {
        const icon = themeToggleBtn.querySelector('i');
        if (body.classList.contains('dark-theme')) {
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
        } else {
            icon.classList.remove('fa-sun');
            icon.classList.add('fa-moon');
        }
    }

    // Form Submission Handling
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Collect form data
        const formData = new FormData(form);
        const data = {
            cognitive_bias_awareness: parseInt(formData.get('cognitive_bias_awareness')),
            persuasion_receptivity: parseInt(formData.get('persuasion_receptivity')),
            deception_susceptibility: parseInt(formData.get('deception_susceptibility')),
            emotional_response_bias: parseInt(formData.get('emotional_response_bias'))
        };

        try {
            // Send data to backend
            const response = await fetch('/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `Server Error: ${response.statusText}`);
            }

            const result = await response.json();

            // Display results
            displayResults(result);
        } catch (error) {
            alert('An error occurred: ' + error.message);
            console.error(error);
        }
    });

    function displayResults(result) {
        // Display AI Response
        let aiResponseHTML = '<ul>';
        for (const [key, value] of Object.entries(result.adjusted_response)) {
            aiResponseHTML += `<li><strong>${capitalizeFirstLetter(key)}:</strong> ${value}</li>`;
        }
        aiResponseHTML += '</ul>';
        aiResponseDiv.innerHTML = aiResponseHTML;

        // Display User Group
        userGroupDiv.innerHTML = `<p><strong>${result.user_group.name}:</strong> ${result.user_group.description}</p>`;

        // Show results section
        resultsSection.classList.remove('hidden');

        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    function capitalizeFirstLetter(string) {
        return string.charAt(0).toUpperCase() + string.slice(1).replace('_', ' ');
    }
});
