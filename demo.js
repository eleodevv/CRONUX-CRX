// Estado de la aplicación
let projects = [];
let currentProject = null;
let currentTheme = 'light';

// Proyectos de ejemplo
const sampleProjects = [
    {
        id: 1,
        name: 'Tesis Universidad',
        path: '/home/usuario/documentos/tesis',
        type: 'documentos',
        versions: [
            { version: '1.3', date: '2024-02-20 14:30', description: 'Correcciones finales del capítulo 3', files: 12, size: '2.4 MB', added: 2, modified: 8, deleted: 1 },
            { version: '1.2', date: '2024-02-18 10:15', description: 'Agregado capítulo de metodología', files: 11, size: '2.1 MB', added: 15, modified: 3, deleted: 0 },
            { version: '1.1', date: '2024-02-15 16:45', description: 'Revisión de introducción y marco teórico', files: 10, size: '1.9 MB', added: 5, modified: 12, deleted: 2 },
            { version: '1.0', date: '2024-02-10 09:00', description: 'Versión inicial del proyecto', files: 8, size: '1.5 MB', added: 25, modified: 0, deleted: 0 }
        ]
    }
];

// Inicialización
document.addEventListener('DOMContentLoaded', () => {
    lucide.createIcons();
    loadTheme();
    loadProjects();
    setupEventListeners();
});

// Cargar tema
function loadTheme() {
    const savedTheme = localStorage.getItem('cronux-demo-theme') || 'light';
    currentTheme = savedTheme;
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon();
}

// Actualizar icono del tema
function updateThemeIcon() {
    const icon = document.getElementById('themeIcon');
    icon.setAttribute('data-lucide', currentTheme === 'light' ? 'sun' : 'moon');
    lucide.createIcons();
}

// Toggle tema
function toggleTheme() {
    currentTheme = currentTheme === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', currentTheme);
    localStorage.setItem('cronux-demo-theme', currentTheme);
    updateThemeIcon();
}

// Cargar proyectos
function loadProjects() {
    projects = [...sampleProjects];
    
    if (projects.length === 0) {
        document.getElementById('emptyState').style.display = 'flex';
        document.getElementById('projectsList').style.display = 'none';
    } else {
        document.getElementById('emptyState').style.display = 'none';
        document.getElementById('projectsList').style.display = 'flex';
        renderProjects();
    }
}

// Renderizar proyectos
function renderProjects() {
    const grid = document.getElementById('projectsGrid');
    grid.innerHTML = '';
    
    projects.forEach(project => {
        const card = createProjectCard(project);
        grid.appendChild(card);
    });
    
    // Asegurar que los iconos se rendericen
    setTimeout(() => lucide.createIcons(), 0);
}

// Crear tarjeta de proyecto
function createProjectCard(project) {
    const card = document.createElement('div');
    card.className = 'project-card';
    card.onclick = () => openProject(project);
    
    const iconMap = {
        'software': 'code',
        'documentos': 'file-text',
        'imagenes': 'image',
        'diseno': 'palette'
    };
    
    card.innerHTML = `
        <div class="project-icon">
            <i data-lucide="${iconMap[project.type] || 'folder'}"></i>
        </div>
        <div class="project-info">
            <div class="project-name">${project.name}</div>
            <div class="project-path">${project.path}</div>
            <div class="project-status">
                <span class="status-dot"></span>
                <span>Activo • ${project.versions.length} versiones</span>
            </div>
        </div>
    `;
    
    return card;
}

// Abrir proyecto
function openProject(project) {
    currentProject = project;
    
    // Ocultar pantalla de inicio
    document.getElementById('homeScreen').style.display = 'none';
    document.getElementById('projectScreen').style.display = 'flex';
    
    // Actualizar título
    document.getElementById('projectTitle').textContent = project.name;
    
    // Renderizar timeline y detalles
    renderTimeline();
    renderDetails();
    
    lucide.createIcons();
}

// Renderizar timeline
function renderTimeline() {
    const container = document.getElementById('timelineContainer');
    container.innerHTML = '';
    
    if (!currentProject || !currentProject.versions.length) {
        container.innerHTML = `
            <div style="text-align: center; padding: 40px 0; color: var(--text-muted);">
                <i data-lucide="history" style="width: 48px; height: 48px; margin-bottom: 12px;"></i>
                <div style="font-size: 14px; font-weight: 300;">Sin versiones</div>
            </div>
        `;
        lucide.createIcons();
        return;
    }
    
    currentProject.versions.forEach((version, index) => {
        const isActive = index === 0;
        const isLast = index === currentProject.versions.length - 1;
        
        const item = document.createElement('div');
        item.className = 'timeline-item';
        item.innerHTML = `
            <div class="timeline-line-container">
                <div class="timeline-dot ${isActive ? 'active' : ''}"></div>
                ${!isLast ? '<div class="timeline-line"></div>' : ''}
            </div>
            <div class="timeline-info">
                <div class="timeline-version ${isActive ? 'active' : ''}">v${version.version}</div>
                <div class="timeline-date">${version.date.split(' ')[0]}</div>
            </div>
        `;
        container.appendChild(item);
    });
    
    lucide.createIcons();
}

// Renderizar detalles
function renderDetails() {
    const container = document.getElementById('detailsContainer');
    container.innerHTML = '';
    
    if (!currentProject || !currentProject.versions.length) {
        container.innerHTML = `
            <div style="text-align: center; padding: 60px; color: var(--text-muted);">
                <div style="font-size: 64px; margin-bottom: 15px;">◯</div>
                <div style="font-size: 16px; font-weight: 300; color: var(--text-primary); margin-bottom: 5px;">Sin versiones guardadas</div>
                <div style="font-size: 13px; font-weight: 300;">Guarda tu primera versión para comenzar</div>
            </div>
        `;
        return;
    }
    
    currentProject.versions.forEach((version, index) => {
        const isActive = index === 0;
        const card = createVersionCard(version, isActive);
        container.appendChild(card);
    });
    
    lucide.createIcons();
}

// Crear tarjeta de versión
function createVersionCard(version, isActive) {
    const card = document.createElement('div');
    card.className = 'version-card';
    
    card.innerHTML = `
        <div class="version-header">
            <div class="version-title-section">
                <div class="version-number">v${version.version}</div>
                <div class="version-date">${version.date}</div>
            </div>
            ${isActive ? '<div class="version-badge">ACTUAL</div>' : ''}
        </div>
        <div class="version-description">${version.description}</div>
        
        <div class="version-file-info">
            <div class="file-info-item">
                <i data-lucide="folder"></i>
                <span>${version.files} archivos</span>
            </div>
            <div class="file-info-item">
                <i data-lucide="hard-drive"></i>
                <span>${version.size}</span>
            </div>
        </div>
        
        <div class="version-stats">
            <div class="version-stat added">
                <i data-lucide="plus-circle"></i>
                <span>${version.added} agregados</span>
            </div>
            <div class="version-stat modified">
                <i data-lucide="edit"></i>
                <span>${version.modified} modificados</span>
            </div>
            <div class="version-stat deleted">
                <i data-lucide="minus-circle"></i>
                <span>${version.deleted} eliminados</span>
            </div>
        </div>
        <div class="version-actions">
            <button class="version-action-btn">
                <i data-lucide="eye"></i>
                Ver cambios
            </button>
            <button class="version-action-btn">
                <i data-lucide="rotate-ccw"></i>
                Restaurar
            </button>
            <button class="version-action-btn">
                <i data-lucide="git-compare"></i>
                Comparar
            </button>
        </div>
    `;
    
    return card;
}

// Volver a inicio
function backToHome() {
    currentProject = null;
    document.getElementById('homeScreen').style.display = 'flex';
    document.getElementById('projectScreen').style.display = 'none';
}

// Setup event listeners
function setupEventListeners() {
    // Theme toggle
    document.getElementById('themeToggle').onclick = toggleTheme;
    
    // Crear proyecto
    document.getElementById('createProjectBtn').onclick = () => openModal('newProjectModal');
    document.getElementById('newProjectBtn').onclick = () => openModal('newProjectModal');
    
    // Abrir proyecto
    document.getElementById('openProjectBtn').onclick = () => showToast('Selecciona una carpeta en tu sistema');
    document.getElementById('openProjectBtn2').onclick = () => showToast('Selecciona una carpeta en tu sistema');
    
    // Importar
    document.getElementById('importBtn').onclick = () => showToast('Función de importar proyecto');
    
    // Limpiar
    document.getElementById('cleanBtn').onclick = () => showToast('Lista limpiada');
    
    // Volver
    document.getElementById('backBtn').onclick = backToHome;
    
    // Guardar versión
    document.getElementById('saveVersionBtn').onclick = () => openModal('saveVersionModal');
    
    // Confirmar crear proyecto
    document.getElementById('confirmCreateBtn').onclick = createProject;
    
    // Confirmar guardar versión
    document.getElementById('confirmSaveBtn').onclick = saveVersion;
    
    // Búsqueda
    document.getElementById('searchInput').oninput = (e) => {
        const query = e.target.value.toLowerCase();
        const cards = document.querySelectorAll('.project-card');
        cards.forEach((card, index) => {
            const project = projects[index];
            const matches = project.name.toLowerCase().includes(query) || 
                          project.path.toLowerCase().includes(query);
            card.style.display = matches ? 'flex' : 'none';
        });
    };
}

// Abrir modal
function openModal(modalId) {
    document.getElementById(modalId).classList.add('active');
}

// Cerrar modal
function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
}

// Crear proyecto
function createProject() {
    const name = document.getElementById('projectNameInput').value.trim();
    const type = document.getElementById('projectTypeInput').value;
    
    if (!name) {
        showToast('Por favor ingresa un nombre', 'error');
        return;
    }
    
    const newProject = {
        id: projects.length + 1,
        name: name,
        path: `/home/usuario/proyectos/${name.toLowerCase().replace(/\s+/g, '-')}`,
        type: type,
        versions: [
            { version: '1.0', date: new Date().toISOString().slice(0, 16).replace('T', ' '), description: 'Versión inicial del proyecto', files: 5, size: '1.2 MB', added: 0, modified: 0, deleted: 0 }
        ]
    };
    
    projects.push(newProject);
    
    // Actualizar UI
    document.getElementById('emptyState').style.display = 'none';
    document.getElementById('projectsList').style.display = 'flex';
    renderProjects();
    
    closeModal('newProjectModal');
    showToast(`Proyecto "${name}" creado exitosamente`);
    
    // Limpiar formulario
    document.getElementById('projectNameInput').value = '';
    
    // Abrir el nuevo proyecto
    setTimeout(() => openProject(newProject), 500);
}

// Guardar versión
function saveVersion() {
    const description = document.getElementById('versionDescInput').value.trim();
    
    if (!description) {
        showToast('Por favor describe los cambios', 'error');
        return;
    }
    
    if (!currentProject) {
        showToast('No hay proyecto abierto', 'error');
        return;
    }
    
    // Calcular nueva versión
    const lastVersion = parseFloat(currentProject.versions[0].version);
    const newVersion = (lastVersion + 0.1).toFixed(1);
    
    // Crear nueva versión
    const newVersionData = {
        version: newVersion,
        date: new Date().toISOString().slice(0, 16).replace('T', ' '),
        description: description,
        files: currentProject.versions[0].files + Math.floor(Math.random() * 3) - 1,
        size: (parseFloat(currentProject.versions[0].size) + (Math.random() * 0.5 - 0.2)).toFixed(1) + ' MB',
        added: Math.floor(Math.random() * 10),
        modified: Math.floor(Math.random() * 15),
        deleted: Math.floor(Math.random() * 5)
    };
    
    currentProject.versions.unshift(newVersionData);
    
    // Actualizar UI
    renderTimeline();
    renderDetails();
    
    closeModal('saveVersionModal');
    showToast('Versión guardada exitosamente');
    
    // Limpiar formulario
    document.getElementById('versionDescInput').value = '';
}

// Mostrar toast
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    const icon = document.getElementById('toastIcon');
    const messageEl = document.getElementById('toastMessage');
    
    if (type === 'error') {
        icon.setAttribute('data-lucide', 'x-circle');
        toast.style.background = 'var(--accent-danger)';
    } else {
        icon.setAttribute('data-lucide', 'check-circle');
        toast.style.background = 'var(--accent-success)';
    }
    
    lucide.createIcons();
    messageEl.textContent = message;
    
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}
