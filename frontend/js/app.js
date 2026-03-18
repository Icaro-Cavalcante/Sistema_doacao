import { state } from './state.js';
import { renderSidebar } from './components/sidebar.js';
import { renderDashboard } from './components/dashboard.js';
import { renderDoacoes } from './components/doacoes.js';
import { renderEstoque } from './components/estoque.js';
import { renderPedidos } from './components/pedidos.js';
import { renderBeneficiarios } from './components/beneficiarios.js';
import { renderVoluntarios } from './components/voluntarios.js';
import { renderUsuarios } from './components/usuarios.js';
import {
    openNovaDoacaoModal, salvarNovaDoacao, deletarDoacao,
    openNovoBeneficiarioModal, salvarNovoBeneficiario, deletarBeneficiario,
    openNovaVagaModal, salvarNovaVaga, deletarVaga,
    openNovoItemModal, salvarNovoItem, deletarItem,
    openNovoPedidoModal, salvarNovoPedido, atualizarStatusPedido, deletarPedido,
    distribuirPedido, salvarDistribuicao,
    abrirMovimentacaoModal, salvarMovimentacao, verInscritosModal,
    openNovoUsuarioModal, salvarNovoUsuario, deletarUsuario
} from './components/modals.js';
import { showToast } from './utils/helpers.js';

window.mudarView = mudarView;
window.showToast = showToast;
window.carregarConteudoGlobal = carregarConteudo; 

// Bind modals e crud actions para o escopo global
window.openNovaDoacaoModal = openNovaDoacaoModal;
window.salvarNovaDoacao = salvarNovaDoacao;
window.deletarDoacao = deletarDoacao;

window.openNovoBeneficiarioModal = openNovoBeneficiarioModal;
window.salvarNovoBeneficiario = salvarNovoBeneficiario;
window.deletarBeneficiario = deletarBeneficiario;

window.openNovaVagaModal = openNovaVagaModal;
window.salvarNovaVaga = salvarNovaVaga;
window.deletarVaga = deletarVaga;

window.openNovoItemModal = openNovoItemModal;
window.salvarNovoItem = salvarNovoItem;
window.deletarItem = deletarItem;

window.openNovoPedidoModal = openNovoPedidoModal;
window.salvarNovoPedido = salvarNovoPedido;
window.atualizarStatusPedido = atualizarStatusPedido;
window.deletarPedido = deletarPedido;

window.distribuirPedido = distribuirPedido;
window.salvarDistribuicao = salvarDistribuicao;

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

    // Exibir o nome do usuário logado
    const nomeUsuario = localStorage.getItem('usuario_nome');
    if (nomeUsuario) {
        const profileDiv = document.getElementById('profileBtn');
        if (profileDiv) {
            const inicial = nomeUsuario.charAt(0).toUpperCase();
            profileDiv.innerHTML = `
                <div class="w-8 h-8 lg:w-9 lg:h-9 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold shadow-sm text-sm lg:text-base flex-shrink-0">${inicial}</div>
                <div class="hidden md:block">
                    <p class="text-sm font-bold text-gray-800 leading-tight truncate w-24" title="${nomeUsuario}">${nomeUsuario}</p>
                    <p class="text-xs text-gray-500">Gestor</p>
                </div>
            `;
        }
    }

    if (typeof renderSidebar === 'function') renderSidebar();
    carregarConteudo();
    renderNotificacoes();
    
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
        logoutBtnClick.addEventListener('click', (e) => {
            e.preventDefault();
            localStorage.removeItem('access_token');
            localStorage.removeItem('usuario_nome');
            localStorage.removeItem('usuario_login');
            window.location.href = 'login.html';
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

// Como as renderizações agora fazem fetch (async), carregarConteudo vira async
async function carregarConteudo() {
    const mainArea = document.getElementById('mainArea');
    
    // Mostra spinner enquanto carrega
    mainArea.innerHTML = `
        <div class="flex flex-col items-center justify-center h-64 text-blue-500">
            <i data-lucide="loader-2" class="w-10 h-10 animate-spin mb-4"></i>
            <p class="text-gray-500 font-medium">A carregar dados...</p>
        </div>
    `;
    if (window.lucide) window.lucide.createIcons();

    try {
        let htmlContent = '';
        
        if (state.currentView === 'dashboard') {
            htmlContent = await renderDashboard();
        } else if (state.currentView === 'doacoes') {
            htmlContent = await renderDoacoes();
        } else if (state.currentView === 'estoque') {
            htmlContent = await renderEstoque();
        } else if (state.currentView === 'pedidos') {
            htmlContent = await renderPedidos();
        } else if (state.currentView === 'beneficiarios') {
            htmlContent = await renderBeneficiarios();
        } else if (state.currentView === 'voluntarios') {
            htmlContent = await renderVoluntarios();
        } else if (state.currentView === 'usuarios') {
            htmlContent = await renderUsuarios();
        }
        
        mainArea.innerHTML = htmlContent;
    } catch (error) {
        console.error("Erro ao renderizar view:", error);
        mainArea.innerHTML = `<div class="p-8 text-center text-red-500 font-bold">Erro ao carregar a página. Verifique se o servidor está online.</div>`;
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