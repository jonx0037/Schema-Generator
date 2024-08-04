document.addEventListener('DOMContentLoaded', () => {
	const projectForm = document.getElementById('project-form');
	const projectsList = document.getElementById('projects-list');

	projectForm.addEventListener('submit', (e) => {
		e.preventDefault();

		const project = {
			name: document.getElementById('project-name').value,
			description: document.getElementById('project-description').value,
			seoTitle: document.getElementById('seo-title').value,
			seoDescription: document.getElementById('seo-description').value,
			seoKeywords: document.getElementById('seo-keywords').value,
		};

		saveProject(project);
		displayProjects();
		projectForm.reset();
	});

	function saveProject(project) {
		let projects = JSON.parse(localStorage.getItem('projects')) || [];
		projects.push(project);
		localStorage.setItem('projects', JSON.stringify(projects));
	}

	function displayProjects() {
		projectsList.innerHTML = '';
		let projects = JSON.parse(localStorage.getItem('projects')) || [];
		projects.forEach((project, index) => {
			let li = document.createElement('li');
			li.textContent = `${project.name} - ${project.seoTitle}`;
			projectsList.appendChild(li);
		});
	}

	displayProjects();
});