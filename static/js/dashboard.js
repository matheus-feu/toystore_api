document.addEventListener('DOMContentLoaded', async function () {
    // Gráfico de vendas por dia
    try {
        const resp = await fetch('/api/v1/toy_store/sales-stats/stats-per-day/', {
            credentials: 'include'
        });
        if (resp.status === 401) {
            alert('Você não está autenticado. Faça login.');
            return;
        }
        const data = await resp.json();
        const items = Array.isArray(data) ? data : (data.results || data.data || []);
        const labels = items.map(item => item.sale_date);
        const valores = items.map(item => item.total);

        new Chart(document.getElementById('vendas-chart').getContext('2d'), {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Total de Vendas',
                    data: valores,
                    backgroundColor: 'rgba(54, 162, 235, 0.5)'
                }]
            }
        });
    } catch (err) {
        console.error('Erro ao carregar gráfico:', err);
    }

    // Destaques (highlights)
    try {
        const respHighlights = await fetch('/api/v1/toy_store/sales-stats/highlights/', {
            credentials: 'include'
        });
        if (respHighlights.status === 401) {
            alert('Você não está autenticado. Faça login.');
            return;
        }
        const highlights = await respHighlights.json();
        const highlightsDiv = document.getElementById('highlights');
        if (highlightsDiv) {
            highlightsDiv.innerHTML = `
                <div class="row">
                    <div class="col">
                        <div class="card text-bg-primary mb-3">
                            <div class="card-body">
                                <h5 class="card-title">Maior Volume de Vendas</h5>
                                <p class="card-text mb-1"><strong>${highlights.top_sales_volume.customer_name ?? '-'}</strong></p>
                                <p class="card-text fs-3">${highlights.top_sales_volume.value ?? '-'}</p>
                            </div>
                        </div>
                    </div>
                    <div class="col">
                        <div class="card text-bg-success mb-3">
                            <div class="card-body">
                                <h5 class="card-title">Maior Média por Venda</h5>
                                <p class="card-text mb-1"><strong>${highlights.top_average_sale.customer_name ?? '-'}</strong></p>
                                <p class="card-text fs-3">${highlights.top_average_sale.value ?? '-'}</p>
                            </div>
                        </div>
                    </div>
                    <div class="col">
                        <div class="card text-bg-warning mb-3">
                            <div class="card-body">
                                <h5 class="card-title">Maior Frequência de Compra</h5>
                                <p class="card-text mb-1"><strong>${highlights.top_unique_sale_days.customer_name ?? '-'}</strong></p>
                                <p class="card-text fs-3">${highlights.top_unique_sale_days.value ?? '-'}</p>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }
    } catch (err) {
        console.error('Erro ao carregar destaques:', err);
    }
});