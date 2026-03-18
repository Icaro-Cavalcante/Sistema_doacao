import { state } from '../state.js';

export function renderSidebar() {
    const menuItems = [
        { id: 'dashboard', label: 'Dashboard', icon: 'layout-dashboard' },
        { id: 'doacoes', label: 'Doações', icon: 'package' },
        { id: 'rastreios', label: 'Rastreios', icon: 'map-pin' },
        { id: 'estoque', label: 'Estoque de Itens', icon: 'boxes' },
        { id: 'pedidos', label: 'Pedidos de Auxílio', icon: 'clipboard-list' },
        { id: 'distribuicoes', label: 'Distribuições', icon: 'truck' },
        { id: 'beneficiarios', label: 'Beneficiários', icon: 'heart' },
        { id: 'voluntarios', label: 'Voluntariado', icon: 'users' },
        { id: 'usuarios', label: 'Usuários', icon: 'user-cog' },
        { id: 'perfis', label: 'Perfis (PF/PJ)', icon: 'id-card' }
    ];

    const sidebarMenu = document.getElementById('sidebarMenu');
    
    sidebarMenu.innerHTML = menuItems.map(item => {
        const isActive = state.currentView === item.id;
        
        const activeClasses = isActive 
            ? 'bg-blue-50 text-blue-700 font-bold shadow-sm' 
            : 'text-gray-600 hover:bg-gray-50 hover:text-blue-600 font-medium';
            
        return `
            <button class="w-full flex items-center gap-3 px-4 py-3 rounded-xl mb-1.5 transition-all duration-200 ${activeClasses} center-on-collapse" 
                    onclick="window.mudarView('${item.id}')">
                <i data-lucide="${item.icon}" class="w-5 h-5 flex-shrink-0 ${isActive ? 'text-blue-600' : 'text-gray-400'}"></i>
                <span class="text-sm whitespace-nowrap hide-on-collapse">${item.label}</span>
            </button>
        `;
    }).join('');
    
    if (window.lucide) window.lucide.createIcons();
}