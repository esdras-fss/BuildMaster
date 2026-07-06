<template>
  <div class="login-container">
    <div class="login-card">
      <div class="logo-buildmaster">
  🖥️
</div>

<h1>Criar Conta</h1>

<p class="descricao">
  Cadastre-se para utilizar o BuildMaster.
</p>
      <h1>Criar Conta</h1>

      <input
        v-model="nome"
        type="text"
        placeholder="Nome"
      />

      <input
        v-model="email"
        type="email"
        placeholder="E-mail"
      />

      <input
        v-model="senha"
        type="password"
        placeholder="Senha"
      />

      <button @click="cadastrar">
        Cadastrar
      </button>

      <p class="cadastro">
        Já possui conta?

        <router-link to="/">
          Entrar
        </router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()

const nome = ref('')
const email = ref('')
const senha = ref('')

async function cadastrar() {
  try {
    await api.post('/users', {
      nome: nome.value,
      email: email.value,
      senha: senha.value
    })

    alert('Usuário cadastrado com sucesso!')

    router.push('/')
  } catch (error) {
  alert(error.response?.data?.detail || 'Erro ao cadastrar usuário.')
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  background: #f5f7fb;
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-card {
  width: 460px;
  background: white;
  padding: 45px;
  border-radius: 18px;
  box-shadow: 0 10px 35px rgba(0,0,0,.08);
}

.logo-buildmaster{
  font-size:55px;
  text-align:center;
  margin-bottom:20px;
}

h1{
  font-size:40px;
  color:#111827;
  text-align:center;
  margin-bottom:10px;
}

.descricao{
  color:#64748b;
  text-align:center;
  margin-bottom:20px;
}

input{
  width:100%;
  box-sizing:border-box;
  padding:15px;
  margin-top:16px;

  border:1px solid #d1d5db;
  border-radius:12px;

  font-size:15px;
  transition:.25s;
}

input:focus{
  outline:none;
  border-color:#2563eb;
  box-shadow:0 0 0 4px rgba(37,99,235,.15);
}

button{
  width:100%;
  margin-top:24px;
  padding:16px;

  background:#2563eb;
  color:white;

  border:none;
  border-radius:12px;

  font-size:16px;
  font-weight:600;

  cursor:pointer;

  transition:.25s;
}

button:hover{
  background:#1d4ed8;
  transform:translateY(-2px);
}

.cadastro{
  margin-top:25px;
  text-align:center;
  color:#64748b;
}

a{
  color:#2563eb;
  text-decoration:none;
  font-weight:600;
}

a:hover{
  text-decoration:underline;
}
</style>