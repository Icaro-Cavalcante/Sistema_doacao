import { state } from '../state.js';

export function renderSidebar() {
    const menuItems = [
        { id: 'dashboard', label: 'Dashboard', icon: 'layout-dashboard' },
        { id: 'doacoes', label: 'Doações', icon: 'package' },
        { id: 'estoque', label: 'Estoque de Itens', icon: 'boxes' },
        { id: 'pedidos', label: 'Pedidos de Auxílio', icon: 'clipboard-list' },
        { id: 'beneficiarios', label: 'Beneficiários', icon: 'users' },
        { id: 'voluntarios', label: 'Voluntários', icon: 'heart-handshake' }
    ];

    const sidebarMenu = document.getElementById('sidebarMenu');
    
    sidebarMenu.innerHTML = menuItems.map(item => {
        const isActive = state.currentView === item.id;
        
        const activeClasses = isActive 
            ? 'bg-blue-50 text-blue-700 font-semibold border-r-4 border-blue-600' 
            : 'text-gray-600 hover:bg-gray-50 hover:text-blue-600 font-medium border-r-4 border-transparent';
            
        return `
            <button class="w-full flex items-center gap-3 px-4 py-3 rounded-lg mb-1 transition-all duration-200 ${activeClasses} center-on-collapse" 
                    onclick="window.mudarView('${item.id}')">
                <i data-lucide="${item.icon}" class="w-5 h-5 flex-shrink-0 ${isActive ? 'text-blue-600' : 'text-gray-400'}"></i>
                <span class="text-sm font-medium whitespace-nowrap hide-on-collapse">${item.label}</span>
            </button>
        `;
    }).join('');
    
    if (window.lucide) window.lucide.createIcons();
}