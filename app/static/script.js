async function buscar() {
    const chave = document.getElementById('chave').value;
    if (!chave) return;
    const resp = await fetch(`/api/busca?chave=${encodeURIComponent(chave)}`);
    const data = await resp.json();
    mostrarResultado(data);
    atualizarHistorico();
}

function mostrarResultado(data) {
    const resultado = document.getElementById('resultado');
    resultado.innerHTML = '';
    const ul = document.createElement('ul');
    Object.entries(data).forEach(([k, v]) => {
        const li = document.createElement('li');
        li.textContent = `${k}: ${Array.isArray(v) ? v.join(', ') : v}`;
        ul.appendChild(li);
    });
    resultado.appendChild(ul);
    desenharGrafico(data);
}

async function atualizarHistorico() {
    const resp = await fetch('/api/historico');
    const hist = await resp.json();
    const div = document.getElementById('historico');
    div.innerHTML = '';
    hist.slice().reverse().forEach(item => {
        const hdiv = document.createElement('div');
        const date = new Date(item.data_hora).toLocaleString('pt-BR');
        hdiv.textContent = `${item.chave} - ${date}`;
        hdiv.onclick = () => mostrarResultado(item.data);
        div.appendChild(hdiv);
    });
}

function desenharGrafico(data) {
    const ctx = document.getElementById('grafico');
    const chartData = {
        labels: ['Renda', 'Score', 'Processos'],
        datasets: [{
            label: 'Indicadores',
            data: [data.renda || 0, data.score || 0, data.processos || 0],
            backgroundColor: ['#0a84ff', '#5e5ce6', '#bf5af2']
        }]
    };
    if (window.grafico) window.grafico.destroy();
    window.grafico = new Chart(ctx, { type: 'bar', data: chartData });
}

function exportar(tipo) {
    const chave = document.getElementById('chave').value;
    if (!chave) return;
    window.open(`/api/export/${tipo}?chave=${encodeURIComponent(chave)}`, '_blank');
}

document.addEventListener('DOMContentLoaded', atualizarHistorico);
