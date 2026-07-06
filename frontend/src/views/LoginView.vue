<template>
  <div class="login-container">
    <div class="login-card">
      <div class="logo-buildmaster">
    🖥️
</div>
      <h1>BuildMaster</h1>
      <p>Faça login para acessar o configurador de PCs.</p>

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

      <button @click="login">
        Entrar
      </button>

      <p class="cadastro">
        Não possui conta?

        <router-link to="/cadastro">
          Cadastre-se
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

const email = ref('')
const senha = ref('')

async function login() {
  try {
    const response = await api.post('/users/login', {
     email: email.value,
     senha: senha.value
})

localStorage.setItem(
  'usuario',
  JSON.stringify(response.data)
)

router.push('/builder')
  } catch (error) {
    alert('E-mail ou senha inválidos.')
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
  width: 420px;
  background: white;
  padding: 40px;
  border-radius: 18px;
  box-shadow: 0 10px 35px rgba(0,0,0,.08);
}

h1{
  font-size:40px;
  font-weight:700;
  color:#111827;
  text-align:center;
  margin-bottom:8px;
}

p{
  color:#64748b;
  text-align:center;
}

input{
  width:100%;
  box-sizing:border-box;
  padding:15px;
  margin-top:16px;

  border:1px solid #d1d5db;
  border-radius:12px;

  font-size:15px;
  transition: .25s;
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
  background:#1D4ED8;
  transform:translateY(-2px);
}

.cadastro {
  margin-top: 20px;
}

a{
  color:#2563eb;
  font-weight:600;
  text-decoration:none;
}

a:hover{
  text-decoration:underline;
}

.logo-buildmaster{
    font-size:55px;
    text-align:center;
    margin-bottom:20px;
}

.login-card {
  width: 460px;
  background: white;
  padding: 45px;
  border-radius: 18px;
  box-shadow: 0 10px 35px rgba(0,0,0,.08);
}
</style>