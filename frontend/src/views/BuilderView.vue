<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import api from '../services/api'
import { useRouter } from 'vue-router'

const router = useRouter()

function logout() {
  localStorage.removeItem('usuario')
  router.push('/')
}

const cpus = ref([])
const gpus = ref([])
const motherboards = ref([])
const cpuSelecionada = ref(null)
const gpuSelecionada = ref(null)
const placasCompativeis = ref([])
const placaSelecionada = ref(null)
const nomeBuild = ref('')
const usuario = JSON.parse(localStorage.getItem('usuario'))
const consumoTotal = computed(() => {
  if (!cpuSelecionada.value || !gpuSelecionada.value) {
    return 0
  }

  return cpuSelecionada.value.consumo + gpuSelecionada.value.consumo
})

const precoTotal = computed(() => {
  if (!cpuSelecionada.value || !gpuSelecionada.value || !placaSelecionada.value) {
    return 0
  }

  return (
    cpuSelecionada.value.preco +
    gpuSelecionada.value.preco +
    placaSelecionada.value.preco
  )
})

const fonteRecomendada = computed(() => {
  if (consumoTotal.value <= 250) {
    return 450
  }

  if (consumoTotal.value <= 350) {
    return 550
  }

  if (consumoTotal.value <= 500) {
    return 650
  }

  return 750
})

const compatibilidade = computed(() => {
  if (
    cpuSelecionada.value &&
    placaSelecionada.value &&
    cpuSelecionada.value.socket === placaSelecionada.value.socket
  ) {
    return 'Todas as peças são compatíveis ✅'
  }

  return 'Peças incompatíveis ❌'
})

const gargalo = computed(() => {
  if (!cpuSelecionada.value || !gpuSelecionada.value) {
    return ''
  }

  const precoCPU = cpuSelecionada.value.preco
  const precoGPU = gpuSelecionada.value.preco

  if (precoGPU > precoCPU * 3) {
    return 'Possível gargalo de CPU: a placa de vídeo é muito forte para esse processador.'
  }

  if (precoCPU > precoGPU * 2) {
    return 'Possível gargalo de GPU: o processador é forte, mas a placa de vídeo pode limitar o desempenho.'
  }

  return 'Setup equilibrado: CPU e GPU combinam bem.'
})

// limpar pesquisa de produto
 
function limparSelecao() {
  cpuSelecionada.value = null
  gpuSelecionada.value = null
  placaSelecionada.value = null
  placasCompativeis.value = []
}

const fonteIdeal = computed(() => {
  if (consumoTotal.value <= 250) {
    return '450W 80 Plus Bronze'
  }

  if (consumoTotal.value <= 350) {
    return '550W 80 Plus Bronze'
  }

  if (consumoTotal.value <= 500) {
    return '650W 80 Plus Gold'
  }

  return '750W 80 Plus Gold'
})

 // sair do perfil
 
function sair() {
  localStorage.removeItem('usuario')
  router.push('/')
}

async function salvarBuild() {
  if (
    
    !cpuSelecionada.value ||
    !gpuSelecionada.value ||
    !placaSelecionada.value
  ) {
    return
  }

  const novaBuild = {
    nome: nomeBuild.value,
    cpu: cpuSelecionada.value.nome,
    gpu: gpuSelecionada.value.nome,
    motherboard: placaSelecionada.value.nome,
    preco_total: precoTotal.value,
    consumo_total: consumoTotal.value
  }

  await api.post('/builds', novaBuild)

  await carregarBuilds()

  alert('Build salva com sucesso!')
}

async function deletarBuild(id) {
  await api.delete(`/builds/${id}`)

  buildsSalvas.value = buildsSalvas.value.filter(
    build => build.id !== id
  )
}

const buildsSalvas = ref([])
async function carregarBuilds() {
  const response = await api.get('/builds')

  buildsSalvas.value = response.data
}
onMounted(async () => {
  const cpuResponse = await api.get('/cpus')
  cpus.value = cpuResponse.data

  const gpuResponse = await api.get('/gpus')
  gpus.value = gpuResponse.data

  const motherboardResponse = await api.get('/motherboards')
  motherboards.value = motherboardResponse.data

  await carregarBuilds()
})

watch(cpuSelecionada, () => {
  if (!cpuSelecionada.value) {
    placasCompativeis.value = []
    placaSelecionada.value = null
    return
  }

  placasCompativeis.value = motherboards.value.filter(
    placa => placa.socket === cpuSelecionada.value.socket
  )

  placaSelecionada.value = null

})

</script>
  


<template>
  <div class="container">
    <header class="hero">

  <div>
    <h1>BuildMaster</h1>

    <p class="subtitle">
      Monte seu computador ideal com análise de compatibilidade,
      consumo, desempenho e custo.
    </p>

    <p class="usuario-logado">
      Bem-vindo, <strong>{{ usuario.nome }}</strong>
    </p>
  </div>

   <button class="btn-logout" @click="logout">
  Sair
</button>

</header>

<div class="builder-grid">

    <div class="card">
      <h2>Processador</h2>

      <select v-model="cpuSelecionada">
        <option :value="null" disabled>
          Escolha um processador
        </option>

        <option
          v-for="cpu in cpus"
          :key="cpu.id"
          :value="cpu"
        >
          {{ cpu.nome }} - R$ {{ cpu.preco }} - {{ cpu.consumo }}W
        </option>
      </select>
    </div>

    <div class="card">
      <h2>Placa de Vídeo</h2>

      <select v-model="gpuSelecionada">
        <option :value="null" disabled>
          Escolha uma GPU
        </option>

        <option
          v-for="gpu in gpus"
          :key="gpu.id"
          :value="gpu"
        >
          {{ gpu.nome }} - R$ {{ gpu.preco }} - {{ gpu.consumo }}W
        </option>
      </select>
    </div>

    <div class="card">
      <h2>Placa-Mãe Compatível</h2>

      <select v-model="placaSelecionada">
        <option :value="null" disabled>
          Escolha uma placa-mãe
        </option>

        <option
          v-for="placa in placasCompativeis"
          :key="placa.id"
          :value="placa"
        >
          {{ placa.nome }} - R$ {{ placa.preco }}
        </option>
      </select>
    </div>
 </div>
    <div
      v-if="
        cpuSelecionada &&
        gpuSelecionada &&
        placaSelecionada
      "
      class="resultado"
    >
      <h2> Resumo da configuração </h2>

      <div class="setup-grid">
        <div class="setup-card">
    <span class="titulo-info">CPU:</span>
    <span>{{ cpuSelecionada.nome }}</span>
</div>

        <div class="setup-card">
    <span class="titulo-info">GPU:</span>
    <span>{{ gpuSelecionada.nome }}</span>
</div>

<div class="setup-card">
    <span class="titulo-info">Placa-Mãe:</span>
    <span>{{ placaSelecionada.nome }}</span>
</div>
      </div>

      <hr>

<div class="compatibilidade-box">
  {{ compatibilidade }}
</div>

<h3>🧩 Análise de Gargalo</h3>

<p>
  {{ gargalo }}
</p>

<hr>

<div class="stats-grid">

  <div class="stat-card">
    <span>💰 Preço Total</span>
    <strong>R$ {{ precoTotal.toLocaleString('pt-BR', {
  minimumFractionDigits: 2,
  maximumFractionDigits: 2
}) }}</strong>
  </div>

  <div class="stat-card">
    <span>⚡ Consumo</span>
    <strong>{{ consumoTotal }}W</strong>
  </div>

  <div class="stat-card">
    <span>🔋 Fonte Recomendada</span>
    <strong>{{ fonteRecomendada }}W</strong>
  </div>

</div>

<hr>

<h3>🎮 FPS Estimado</h3>

<div class="fps-grid">

  <div class="fps-card">
    <span>Valorant</span>
    <strong>{{ gpuSelecionada.fps_valorant }} FPS</strong>
  </div>

  <div class="fps-card">
    <span>GTA V</span>
    <strong>{{ gpuSelecionada.fps_gta }} FPS</strong>
  </div>

  <div class="fps-card">
    <span>Cyberpunk 2077</span>
    <strong>{{ gpuSelecionada.fps_cyberpunk }} FPS</strong>
  </div>

</div>

<hr>

<div class="salvar-build">

  <h3>Nome da Build</h3>

  <input
    class="input-build"
    v-model="nomeBuild"
    type="text"
    placeholder="Ex.: PC Gamer RTX 4060"
  />

  <button
    class="btn-salvar"
    @click="salvarBuild"
  >
    💾 Salvar Build
  </button>

  <button
    class="btn-limpar"
    @click="limparSelecao"
  >
    🗑 Limpar Configuração
  </button>

</div>
    </div>

 <div class="builds-salvas">
<h2>
  Builds Salvas ({{ buildsSalvas.length }})
</h2>

  <div class="builds-grid">
    <div
      v-for="build in buildsSalvas"
      :key="build.id"
      class="build-card"
    >
      <div class="build-header">

  <h3>{{ build.nome }}</h3>

  <span>#{{ build.id }}</span>

</div>

<div class="build-componentes">

  <p><strong>🖥 Processador</strong><br>{{ build.cpu }}</p>

  <p><strong>🎮 Placa de Vídeo</strong><br>{{ build.gpu }}</p>

  <p><strong>🧩 Placa-Mãe</strong><br>{{ build.motherboard }}</p>

</div>

<div class="build-info">

  <div>
    <small>Preço</small>
    <strong>
  R$ {{
    build.preco_total.toLocaleString('pt-BR', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    })
  }}
</strong>
  </div>

  <div>
    <small>Consumo</small>
    <strong>{{ build.consumo_total }}W</strong>
  </div>

</div>

<button
class="btn-deletar"
@click="deletarBuild(build.id)"
>
🗑 Excluir Build
</button>
      </div>
     </div>
    </div>
  </div>
</template>

<style>
body {
  margin: 0;
  background: #f3f4f6;
  font-family: 'Poppins', sans-serif;
  color: #111827;
}

.container {
  max-width: 1200px;
  margin: auto;
  padding: 40px;
  color: #111827;
}

h1 {
  font-size: 48px;
  margin-bottom: 15px;
  color: #111827;
  text-shadow: none;
}

.card {
  background: white;
  padding: 24px;
  border-radius: 16px;
  border: 1px solid #e5e7eb;
  box-shadow: 0 8px 25px rgba(0,0,0,.08);
  transition: .25s;
}

.card:hover{
  transform: translateY(-4px);
  box-shadow:0 15px 30px rgba(0,0,0,.12);
}

.card h2{
    color:#111827;
    margin-bottom:18px;
}

select{
    width:100%;
    padding:14px;
    border-radius:10px;
    border:1px solid #d1d5db;
    background:white;
    color:#111827;
    font-size:15px;
    transition:.2s;
}

select:focus{
    outline:none;
    border-color:#2563eb;
    box-shadow:0 0 0 4px rgba(37,99,235,.15);
}

.resultado{
    background:#fff;
    padding:35px;
    border-radius:18px;
    margin-top:35px;
    border:1px solid #E5E7EB;
    box-shadow:0 10px 30px rgba(0,0,0,.08);
}

.resultado h2 {
    color: #111827;
}

.resultado h3 {
  color: #facc15;
}

hr {
  border: none;
  height: 1px;
  background: #334155;
  margin: 20px 0;
}

p {
  font-size: 17px;
}

.btn-limpar{
    width:100%;
    margin-top:15px;
    padding:15px;
    background:#EF4444;
    color:white;
    border:none;
    border-radius:10px;
    cursor:pointer;
    transition:.2s;
}

.btn-limpar:hover{
    background:#DC2626;
}

.setup-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
  margin-bottom: 25px;
}

.setup-card{
    background:#F9FAFB;
    border:1px solid #E5E7EB;
    padding:20px;
    border-radius:14px;
    box-shadow:none;
}

.setup-card strong{
    color:#2563EB;
}

.setup-card span{
    color:#111827;
}

.btn-salvar{
    width:100%;
    margin-top:20px;
    padding:15px;
    background:#2563EB;
    color:white;
    border:none;
    border-radius:10px;
    font-size:16px;
    font-weight:600;
    cursor:pointer;
    transition:.2s;
}

.btn-salvar:hover{
    background:#1D4ED8;
}

.build-card {
  background: rgba(15, 23, 42, 0.9);
  border: 1px solid #38bdf8;
  padding: 20px;
  border-radius: 14px;
  margin-bottom: 20px;
  box-shadow: 0 0 20px rgba(56, 189, 248, 0.2);
}
.btn-deletar {
  margin-top: 12px;
  padding: 10px 18px;
  border: none;
  border-radius: 10px;
  background: #ef4444;
  color: white;
  cursor: pointer;
}

.btn-deletar:hover {
  transform: scale(1.05);
}

.hero {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 30px;
  margin-bottom: 40px;
}

.badge {
  display: inline-block;
  padding: 8px 14px;
  background: rgba(124, 58, 237, 0.2);
  border: 1px solid #a855f7;
  border-radius: 999px;
  color: #c084fc;
  font-size: 14px;
  margin-bottom: 12px;
}

.subtitle {
  max-width: 700px;
  color: #6b7280;
  font-size: 18px;
  line-height: 1.6;
}

@media (max-width: 768px) {
  .hero {
    flex-direction: column;
    align-items: flex-start;
  }

  h1 {
    text-align: left;
    font-size: 38px;
  }
}

.builder-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 22px;
  margin-bottom: 30px;
}

@media (max-width: 900px) {
  .builder-grid {
    grid-template-columns: 1fr;
  }
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 18px;
  margin: 30px 0;
}

.stat-card {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 22px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  transition: .2s;
}

.stat-card:hover {
  transform: translateY(-4px);
}

.stat-card span {
  color: #64748b;
  font-size: 14px;
}

.stat-card strong {
  color: #111827;
  font-size: 24px;
  font-weight: bold;
}

.purple {
  background: linear-gradient(135deg, #7c3aed, #a855f7);
}

.blue {
  background: linear-gradient(135deg, #2563eb, #38bdf8);
}

.green {
  background: linear-gradient(135deg, #16a34a, #22c55e);
}

.yellow {
  background: linear-gradient(135deg, #ca8a04, #facc15);
  color: #111827;
}

.compatibilidade-box{
    background: #dcfce7;
    border: 2px solid #22c55e;
    color: #166534;
    padding: 18px;
    border-radius: 14px;
    font-weight: 600;
}

@media (max-width: 700px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
.builds-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.build-header {
  display: flex;
  justify-content: space-between;
  gap: 15px;
  align-items: center;
}

.build-header span {
  color: #c084fc;
  font-size: 14px;
}

.build-info {
  display: flex;
  justify-content: space-between;
  margin: 18px 0;
  color: #38bdf8;
}

@media (max-width: 700px) {
  .builds-grid {
    grid-template-columns: 1fr;
  }
}

.build-card h3 {
  color: #38bdf8;
  font-size: 30px;
  margin-bottom: 25px;
}
.btn-logout{
    background:#ef4444;
    color:white;
    border:none;
    padding:12px 22px;
    border-radius:10px;
    cursor:pointer;
    font-weight:bold;
    transition:.2s;
}

.btn-logout:hover{
    background:#dc2626;
}

.usuario-logado{
    margin-top:15px;
    color:#6b7280;
    font-size:15px;
}

.usuario-logado strong{
    color:#2563EB;
}

.fps-grid{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:18px;
    margin:25px 0;
}

.fps-card{
    background:#ffffff;
    border:1px solid #e5e7eb;
    border-radius:14px;
    padding:20px;
    text-align:center;
    box-shadow:0 8px 18px rgba(0,0,0,.08);
    transition:.2s;
}

.fps-card:hover{
    transform:translateY(-4px);
}

.fps-card span{
    display:block;
    color:#6b7280;
    margin-bottom:10px;
    font-size:14px;
}

.fps-card strong{
    font-size:24px;
    color:#2563EB;
}

@media(max-width:768px){
    .fps-grid{
        grid-template-columns:1fr;
    }
}

.build-card{

    background:#fff;
    border:1px solid #E5E7EB;
    border-radius:18px;
    padding:22px;

    box-shadow:0 10px 25px rgba(0,0,0,.08);

    transition:.25s;
}

.build-card:hover{

    transform:translateY(-5px);

}

.build-componentes{

    margin:20px 0;

}

.build-componentes p{

    margin:15px 0;

    color:#374151;

}

.build-componentes strong{

    color:#2563EB;

}

.build-info{

    display:flex;

    justify-content:space-between;

    margin:25px 0;

}

.build-info div{

    display:flex;

    flex-direction:column;

}

.build-info small{

    color:#9CA3AF;

}

.build-info strong{

    font-size:20px;

}
.btn-deletar{

    width:100%;

    padding:14px;

    background:#DC2626;

    color:white;

    border:none;

    border-radius:10px;

    cursor:pointer;

    transition:.2s;

}

.btn-deletar:hover{

    background:#B91C1C;

}
.setup-card {
    display: flex;
    align-items: center;
    gap: 8px;
}

.titulo-info {
    color: #2563eb;
    font-weight: 700;
}

.salvar-build {
  margin-top: 35px;
  padding: 30px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 18px;
}

.salvar-build h3 {
  margin-bottom: 18px;
  color: #111827;
}

.input-build {
  width: 100%;
  box-sizing: border-box;
  padding: 16px;
  margin-bottom: 20px;

  border: 1px solid #cbd5e1;
  border-radius: 12px;

  font-size: 16px;

  transition: .2s;
}

.input-build:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 4px rgba(37, 99, 235, .15);
}
</style>