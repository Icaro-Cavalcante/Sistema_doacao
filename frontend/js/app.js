import { state } from './state.js';
import { renderSidebar } from './components/sidebar.js';
import { renderDashboard } from './components/dashboard.js';
import { renderDoacoes } from './components/doacoes.js';
import { renderEstoque } from './components/estoque.js';
import { renderPedidos } from './components/pedidos.js';
import { renderBeneficiarios } from './components/beneficiarios.js';
import { renderVoluntarios } from './components/voluntarios.js';
import {
    openNovaDoacaoModal, salvarNovaDoacao,
    openNovoBeneficiarioModal, salvarNovoBeneficiario,
    openNovaVagaModal, salvarNovaVaga,
    openNovoItemModal, salvarNovoItem,
    openNovoPedidoModal, salvarNovoPedido,
    openDistribuirModal, aprovarPedido, distribuirPedido,
    abrirMovimentacaoModal, salvarMovimentacao, verInscritosModal
} from './components/modals.js';
import { showToast } from './utils/helpers.js';

window.mudarView = mudarView;
window.showToast = showToast;
window.carregarConteudoGlobal = carregarConteudo; 

window.openNovaDoacaoModal = openNovaDoacaoModal;
window.salvarNovaDoacao = salvarNovaDoacao;
window.openNovoBeneficiarioModal = openNovoBeneficiarioModal;
window.salvarNovoBeneficiario = salvarNovoBeneficiario;
window.openNovaVagaModal = openNovaVagaModal;
window.salvarNovaVaga = salvarNovaVaga;
window.openNovoItemModal = openNovoItemModal;
window.salvarNovoItem = salvarNovoItem;
window.openNovoPedidoModal = openNovoPedidoModal;
window.salvarNovoPedido = salvarNovoPedido;
window.openDistribuirModal = openDistribuirModal;
window.aprovarPedido = aprovarPedido;
window.distribuirPedido = distribuirPedido;
window.abrirMovimentacaoModal = abrirMovimentacaoModal;
window.salvarMovimentacao = salvarMovimentacao;
window.verInscritosModal = verInscritosModal;

window.marcarNotificacaoLida = (id) => {
    const notif = state.notifications.find(n => n.id === id);
    if(notif) notif.read = true;
    renderNotificacoes();
};

function toggleMobileMenu(forceClose = false) {
    const sidebar = document.getElementById('sidebar');
    const backdrop = document.getElementById('sidebarBackdrop');
    
    const isOpen = forceClose ? false : sidebar.classList.contains('-translate-x-full');

    if (isOpen) {
        sidebar.classList.remove('-translate-x-full');
        backdrop.classList.remove('hidden');
    } else {
        sidebar.classList.add('-translate-x-full');
        backdrop.classList.add('hidden');
    }
}

function iniciarApp() {
    if (!document.getElementById('toast')) {
        const toastTemplate = document.getElementById('toast-template');
        if (toastTemplate) {
            document.body.appendChild(toastTemplate.content.cloneNode(true));
        }
    }

    if (typeof renderSidebar === 'function') renderSidebar();
    carregarConteudo();
    renderNotificacoes();
    
    // Lógica Retrair Menu Refatorada (SÓ 3 LINHAS DE CÓDIGO!)
    const toggleBtn = document.getElementById('toggleSidebar');
    if (toggleBtn) {
        toggleBtn.addEventListener('click', () => {
            document.body.classList.toggle('sidebar-collapsed');
        });
    }

    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const closeSidebarMobile = document.getElementById('closeSidebarMobile');
    const sidebarBackdrop = document.getElementById('sidebarBackdrop');

    if (mobileMenuBtn) mobileMenuBtn.addEventListener('click', () => toggleMobileMenu());
    if (closeSidebarMobile) closeSidebarMobile.addEventListener('click', () => toggleMobileMenu(true));
    if (sidebarBackdrop) sidebarBackdrop.addEventListener('click', () => toggleMobileMenu(true));

    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            state.searchTerm = e.target.value;
            carregarConteudo(); 
        });
    }

    const notifBtn = document.getElementById('notificationBtn');
    const notifDropdown = document.getElementById('notificationDropdown');
    if (notifBtn && notifDropdown) {
        notifBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            state.showNotifications = !state.showNotifications;
            notifDropdown.classList.toggle('hidden', !state.showNotifications);
        });

        document.addEventListener('click', (e) => {
            if (!notifDropdown.contains(e.target) && !notifBtn.contains(e.target)) {
                state.showNotifications = false;
                notifDropdown.classList.add('hidden');
            }
        });
    }

    const logoutBtnClick = document.getElementById('logoutBtn');
    if (logoutBtnClick) {
        logoutBtnClick.addEventListener('click', () => {
            showToast('Logout realizado com sucesso!', 'success');
        });
    }
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', iniciarApp);
} else {
    iniciarApp();
}

function mudarView(view) {
    state.currentView = view;
    renderSidebar();
    carregarConteudo();
    
    if (window.innerWidth < 1024) {
        toggleMobileMenu(true);
    }
}

function carregarConteudo() {
    const mainArea = document.getElementById('mainArea');
    
    if (state.currentView === 'dashboard') {
        mainArea.innerHTML = renderDashboard();
    } else if (state.currentView === 'doacoes') {
        mainArea.innerHTML = renderDoacoes();
    } else if (state.currentView === 'estoque') {
        mainArea.innerHTML = renderEstoque();
    } else if (state.currentView === 'pedidos') {
        mainArea.innerHTML = renderPedidos();
    } else if (state.currentView === 'beneficiarios') {
        mainArea.innerHTML = renderBeneficiarios();
    } else if (state.currentView === 'voluntarios') {
        mainArea.innerHTML = renderVoluntarios();
    }
    
    if (window.lucide) window.lucide.createIcons();
}

function renderNotificacoes() {
    const notificacoesNaoLidas = state.notifications.filter(n => !n.read).length;
    const badge = document.getElementById('notificationBadge');
    
    if (badge) {
        badge.style.display = notificacoesNaoLidas > 0 ? 'block' : 'none';
    }

    const list = document.getElementById('notificationList');
    if (!list) return;

    if(state.notifications.length === 0) {
        list.innerHTML = '<div class="px-4 py-4 text-sm text-gray-500 text-center">Nenhuma notificação</div>';
        return;
    }
    
    list.innerHTML = state.notifications.map(n => `
        <div class="px-4 py-3 border-b border-gray-50 hover:bg-gray-50 cursor-pointer flex flex-col gap-1 transition-opacity ${n.read ? 'opacity-50' : 'opacity-100'}" onclick="window.marcarNotificacaoLida(${n.id})">
            <span class="text-sm font-medium text-gray-800">${n.message}</span>
            <span class="text-xs text-gray-400 flex items-center gap-1">
                <i data-lucide="clock" class="w-3 h-3"></i> ${n.time}
            </span>
        </div>
    `).join('');

    if (window.lucide) window.lucide.createIcons();
}