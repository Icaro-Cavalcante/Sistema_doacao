export function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    const toastContent = document.getElementById('toastContent');
    
    // Define o ícone e a cor com base no tipo
    let iconName = 'check-circle';
    let bgColor = 'bg-green-500';
    
    if (type === 'error') {
        iconName = 'alert-circle';
        bgColor = 'bg-red-500';
    } else if (type === 'info') {
        iconName = 'info';
        bgColor = 'bg-blue-500';
    }

    // Recria todo o conteúdo do toast para garantir que o <i> existe sempre fresquinho para o Lucide
    toastContent.className = `${bgColor} text-white px-4 py-3 rounded-lg shadow-lg flex items-center gap-3 font-medium`;
    toastContent.innerHTML = `<i data-lucide="${iconName}" class="w-5 h-5"></i><span>${message}</span>`;
    
    // Renderiza os ícones novamente
    if (window.lucide) window.lucide.createIcons();
    
    // Mostra o Toast
    toast.classList.remove('hidden');
    toast.classList.add('opacity-100');
    
    // Esconde depois de 3 segundos
    setTimeout(() => {
        toast.classList.remove('opacity-100');
        setTimeout(() => toast.classList.add('hidden'), 300);
    }, 3000);
}

export function formatDate(dateString) {
    if (!dateString) return '-';
    // Corrige o timezone para evitar que o dia volte 1 dia atrás devido a fuso horário
    const date = new Date(dateString + 'T12:00:00');
    return date.toLocaleDateString('pt-BR');
}

export function getStatusColor(status) {
    const cores = {
        // Status Gerais
        "Recebido": "bg-blue-100 text-blue-800",
        "Triagem": "bg-yellow-100 text-yellow-800",
        "Distribuído": "bg-green-100 text-green-800",
        "Pendente": "bg-orange-100 text-orange-800",
        "Aprovado": "bg-green-100 text-green-800",
        "Ativa": "bg-emerald-100 text-emerald-800",
        
        // Prioridades
        "Alta": "bg-red-100 text-red-800 font-bold",
        "Média": "bg-yellow-100 text-yellow-800",
        "Baixa": "bg-green-100 text-green-800",

        // Estoque
        "Em Estoque": "bg-green-100 text-green-800",
        "Baixo Estoque": "bg-yellow-100 text-yellow-800 font-medium",
        "Esgotado": "bg-red-100 text-red-800 font-bold",
    };
    return cores[status] || "bg-gray-100 text-gray-800";
}