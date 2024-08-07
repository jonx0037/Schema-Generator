document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('schemaForm');
    const schemaOutput = document.getElementById('schemaOutput');

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
        .then(response => response.json())
        .then(schema => {
            schemaOutput.textContent = JSON.stringify(schema, null, 2);
        })
        .catch(error => {
            console.error('Error:', error);
            schemaOutput.textContent = 'An error occurred while generating the schema.';
        });
    });
});