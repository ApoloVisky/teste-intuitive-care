<template>
  <div class="container">
    <header class="header">
      <h1 class="title">🔍 Busca de Operadoras de Saúde</h1>
      <p class="subtitle">Encontre operadoras por nome, CNPJ ou registro ANS</p>
    </header>

    <div class="search-box">
      <div class="search-input-container">
        <input
          v-model="searchTerm"
          @keyup.enter="search"
          placeholder="Digite sua busca..."
          class="search-input"
          :disabled="loading"
        />
        <button @click="search" class="search-button" :disabled="!searchTerm || loading">
          <span v-if="loading">
            <i class="spinner"></i> Buscando...
          </span>
          <span v-else>Buscar</span>
        </button>
      </div>
    </div>

    <div v-if="errorMessage" class="error-message">
      <i class="icon">⚠️</i> {{ errorMessage }}
      <button v-if="errorMessage.includes('servidor')" @click="search" class="retry-button">
        Tentar novamente
      </button>
    </div>

    <div v-if="searchTerm && !loading && results.length === 0 && !errorMessage" class="empty-results">
      <i class="icon">😕</i> Nenhum resultado encontrado para "{{ searchTerm }}"
    </div>

    <div v-if="results.length > 0" class="results-container">
      <div class="results-header">
        <h2>📋 Resultados ({{ results.length }})</h2>
        <button @click="exportToCSV" class="export-button">
          <i class="icon">📤</i> Exportar CSV
        </button>
      </div>

      <div class="results-list">
        <div v-for="(item, index) in results" :key="index" class="result-card">
          <div class="card-header">
            <h3>{{ item.Nome || 'Nome não disponível' }}</h3>
            <span class="badge">{{ index + 1 }}</span>
          </div>
          
          <div class="card-body">
            <div class="info-row">
              <span class="label">CNPJ:</span>
              <span class="value">{{ item.CNPJ || 'Não informado' }}</span>
            </div>
            <div class="info-row">
              <span class="label">Registro ANS:</span>
              <span class="value">{{ item['Registro ANS'] || 'Não informado' }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="tips" v-if="results.length === 0 && !searchTerm">
      <h3>💡 Dicas para busca:</h3>
      <ul>
        <li>Tente buscar por partes do nome</li>
        <li>CNPJs devem ser digitados sem pontuação</li>
        <li>Você pode buscar por números do registro ANS</li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchTerm: '',
      results: [],
      loading: false,
      errorMessage: '',
    };
  },
  methods: {
  async search() {
    if (!this.searchTerm.trim()) {
      this.errorMessage = 'Por favor, digite um termo para buscar';
      return;
    }

    this.loading = true;
    this.errorMessage = '';
    this.results = [];

    try {
      // Teste se o servidor está respondendo
      const ping = await fetch('http://localhost:5000/api/health').catch(() => null);
      if (!ping || !ping.ok) {
        throw new Error('O servidor não está respondendo. Verifique se o backend está rodando.');
      }

      const response = await fetch(`http://localhost:5000/api/buscar?termo=${encodeURIComponent(this.searchTerm)}`);
      
      if (!response.ok) {
        throw new Error(`Erro na requisição (status ${response.status})`);
      }

      const data = await response.json();
      
      
      let rawResults = [];
      
      if (data?.data?.resultados) {
        rawResults = data.data.resultados.map(item => {
          
          const key = Object.keys(item)[0];
          const values = item[key].split(';').map(v => v.replace(/"/g, '').trim());
          
          
          return {
            'Registro ANS': values[0] || 'Não informado',
            'CNPJ': values[1] || 'Não informado',
            'Nome': values[3] || values[2] || 'Nome não disponível', 
            'Razao_Social': values[2],
            'Nome_Fantasia': values[3]
          };
        });
      }

      this.results = rawResults;

      if (this.results.length === 0) {
        this.errorMessage = 'Nenhum resultado encontrado';
      }
    } catch (error) {
      console.error('Erro na busca:', error);
      this.errorMessage = error.message || 'Erro ao conectar com o servidor. Verifique:'
        + '\n1. Se o servidor backend está rodando'
        + '\n2. Se a URL está correta (http://localhost:5000)'
        + '\n3. O console do navegador para detalhes (F12)';
    } finally {
      this.loading = false;
    }
  },
    exportToCSV() {
      if (this.results.length === 0) return;

      const headers = ['Nome', 'CNPJ', 'Registro ANS'];
      const csvRows = [
        headers.join(','),
        ...this.results.map(item => 
          headers.map(header => 
            `"${(item[header] || '').toString().replace(/"/g, '""')}"`
          ).join(',')
        )
      ];

      const csvContent = csvRows.join('\n');
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `operadoras_${new Date().toISOString().slice(0,10)}.csv`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  }
};
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.header {
  text-align: center;
  margin-bottom: 30px;
}

.title {
  color: #2c3e50;
  font-size: 2rem;
  margin-bottom: 5px;
}

.subtitle {
  color: #7f8c8d;
  font-size: 1rem;
}

.search-box {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.search-input-container {
  display: flex;
  gap: 10px;
}

.search-input {
  flex: 1;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  transition: all 0.3s;
}

.search-input:focus {
  border-color: #3498db;
  outline: none;
  box-shadow: 0 0 0 3px rgba(52,152,219,0.1);
}

.search-button {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 0 20px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.search-button:hover:not(:disabled) {
  background-color: #2980b9;
  transform: translateY(-1px);
}

.search-button:disabled {
  background-color: #95a5a6;
  cursor: not-allowed;
}

.spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255,255,255,0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-message {
  background-color: #fdecea;
  color: #e74c3c;
  padding: 15px;
  border-radius: 6px;
  margin-bottom: 20px;
  white-space: pre-line;
  line-height: 1.6;
}

.error-message .icon {
  margin-right: 8px;
}

.retry-button {
  margin-top: 10px;
  background: #e53935;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 4px;
  cursor: pointer;
  display: block;
}

.empty-results {
  background-color: #f8f9fa;
  color: #7f8c8d;
  padding: 15px;
  border-radius: 6px;
  text-align: center;
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
}

.results-container {
  margin-top: 30px;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.export-button {
  background: none;
  border: 1px solid #3498db;
  color: #3498db;
  padding: 8px 15px;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
}

.export-button:hover {
  background-color: #ebf5fb;
}

.results-list {
  display: grid;
  grid-template-columns: 1fr;
  gap: 15px;
}

.result-card {
  background: white;
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 15px;
  transition: all 0.3s;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.result-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  border-color: #3498db;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.card-header h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.2rem;
}

.badge {
  background-color: #3498db;
  color: white;
  padding: 3px 8px;
  border-radius: 10px;
  font-size: 0.8rem;
}

.info-row {
  display: flex;
  margin-bottom: 5px;
}

.label {
  font-weight: bold;
  color: #7f8c8d;
  min-width: 100px;
}

.value {
  color: #34495e;
}

.tips {
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  margin-top: 30px;
}

.tips h3 {
  margin-top: 0;
  color: #2c3e50;
}

.tips ul {
  padding-left: 20px;
  color: #7f8c8d;
}

@media (max-width: 768px) {
  .container {
    padding: 15px;
  }
  
  .title {
    font-size: 1.5rem;
  }
  
  .search-input-container {
    flex-direction: column;
  }
  
  .search-button {
    width: 100%;
    justify-content: center;
    padding: 12px;
  }
  
  .results-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .export-button {
    width: 100%;
    justify-content: center;
  }
  
  .info-row {
    flex-direction: column;
    gap: 2px;
  }
  
  .label {
    min-width: auto;
  }
}
</style>