<template>
    <div class="busca-container">
      <div class="busca-wrapper">
        <input v-model="termoBusca" placeholder="Digite o termo de busca" class="busca-input" />
        <button @click="buscarOperadoras" class="busca-botao" :disabled="carregando">Buscar</button>
        <p v-if="carregando">Carregando...</p>
        <p v-if="resultados.length === 0 && !carregando && termoBusca !== ''">Nenhum resultado encontrado.</p>
        <ul class="resultados-lista">
          <li v-for="operadora in resultados" :key="operadora.CNPJ" class="resultados-item">
            {{ operadora.Nome }} (CNPJ: {{ operadora.CNPJ }}, Registro ANS: {{ operadora['Registro ANS'] }})
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import './BuscaOperadoras.css';
  
  export default {
    data() {
      return {
        termoBusca: '',
        resultados: [],
        carregando: false,
      };
    },
    methods: {
      buscarOperadoras() {
        this.carregando = true;
        axios
          .get(`/buscar?termo=${this.termoBusca}`)
          .then((response) => {
            this.resultados = response.data;
            this.carregando = false;
          })
          .catch((error) => {
            console.error('Erro na busca:', error);
            this.carregando = false;
          });
      },
    },
  };
  </script>
  
  <style scoped>
  .busca-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background-color: #f4f4f4;
  }
  
  .busca-wrapper {
    width: 600px;
    padding: 20px;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  .busca-input {
    width: 100%;
    padding: 10px;
    margin-bottom: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  .busca-botao {
    padding: 10px 15px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .busca-botao:hover {
    background-color: #0056b3;
  }
  
  .resultados-lista {
    list-style: none;
    padding: 0;
  }
  
  .resultados-item {
    padding: 10px;
    border-bottom: 1px solid #eee;
  }
  
  .resultados-item:last-child {
    border-bottom: none;
  }
  </style>