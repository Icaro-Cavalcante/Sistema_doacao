export function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    const toastContent = document.getElementById('toastContent');
    
    let iconName = 'check-circle';
    let bgColor = 'bg-green-500';
    
    if (type === 'error') {
        iconName = 'alert-circle';
        bgColor = 'bg-red-500';
    } else if (type === 'info') {
        iconName = 'info';
        bgColor = 'bg-blue-500';
    }

    toastContent.className = `${bgColor} text-white px-4 py-3 rounded-lg shadow-lg flex items-center gap-3 font-medium`;
    toastContent.innerHTML = `<i data-lucide="${iconName}" class="w-5 h-5"></i><span>${message}</span>`;
    
    if (window.lucide) window.lucide.createIcons();
    
    toast.classList.remove('hidden');
    toast.classList.add('opacity-100');
    
    setTimeout(() => {
        toast.classList.remove('opacity-100');
        setTimeout(() => toast.classList.add('hidden'), 300);
    }, 3000);
}

export function formatDate(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString + 'T12:00:00');
    return date.toLocaleDateString('pt-BR');
}

export function getStatusColor(status) {
    if (!status) return "bg-gray-100 text-gray-800";

    const cores = {
        // Status Doações e Distribuições
        "Recebida": "bg-blue-100 text-blue-800",
        "Recebido": "bg-blue-100 text-blue-800",
        "Triagem": "bg-yellow-100 text-yellow-800",
        "Distribuído": "bg-green-100 text-green-800",
        "Em separação": "bg-purple-100 text-purple-800",
        "Entregue": "bg-green-100 text-green-800",
        
        // Status Pedidos
        "Pendente": "bg-orange-100 text-orange-800",
        "Aprovado": "bg-green-100 text-green-800",
        "Atendido": "bg-emerald-100 text-emerald-800",
        
        // Status Vagas e Beneficiários
        "Ativa": "bg-emerald-100 text-emerald-800",
        "Ativo": "bg-emerald-100 text-emerald-800",
        "Encerrada": "bg-gray-100 text-gray-800",
        "Inativo": "bg-red-100 text-red-800",
        
        // Prioridades
        "Alta": "bg-red-100 text-red-800 font-bold",
        "Média": "bg-yellow-100 text-yellow-800",
        "Baixa": "bg-green-100 text-green-800",

        // Estoque
        "Em Estoque": "bg-green-100 text-green-800",
        "Baixo Estoque": "bg-yellow-100 text-yellow-800 font-medium",
        "Sem Estoque": "bg-red-100 text-red-800 font-bold",
        "Esgotado": "bg-red-100 text-red-800 font-bold",
    };
    
    // Procura a cor exata ou usa um fallback cinza
    return cores[status] || cores[status.trim()] || "bg-gray-100 text-gray-800";
}