document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('schemaForm');
    const schemaOutput = document.getElementById('schemaOutput');

    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();

            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());

            fetch('/generate_schema', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(schema => {
                schemaOutput.textContent = JSON.stringify(schema, null, 2);
            })
            .catch(error => {
                console.error('Error:', error);
                schemaOutput.textContent = `An error occurred while generating the schema: ${error.message}`;
            });
        });
    }

    // Load existing schema data if available
    const projectId = document.getElementById('project_id');
    if (projectId) {
        fetch(`/project/${projectId.value}`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.schema) {
                    Object.keys(data.schema).forEach(key => {
                        const input = document.getElementById(key);
                        if (input) {
                            input.value = data.schema[key];
                        }
                    });
                }
            })
            .catch(error => {
                console.error('Error loading project data:', error);
                alert(`Error loading project data: ${error.message}`);
            });
    }
});