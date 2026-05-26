<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import api from '../services/api'

const cpus = ref([])
const gpus = ref([])
const motherboards = ref([])

const cpuSelecionada = ref(null)
const gpuSelecionada = ref(null)

const placasCompativeis = ref([])
const placaSelecionada = ref(null)

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

const categoriaSetup = computed(() => {
  if (precoTotal.value === 0) {
    return ''
  }

  if (precoTotal.value <= 3000) {
    return 'Setup de Entrada'
  }

  if (precoTotal.value <= 6000) {
    return 'Setup Intermediário'
  }

  return 'Setup High-end'
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

async function salvarBuild() {
  if (
    !cpuSelecionada.value ||
    !gpuSelecionada.value ||
    !placaSelecionada.value
  ) {
    return
  }

  const novaBuild = {
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
    <p class="badge">PC Builder Inteligente</p>
    <h1>BuildMaster</h1>
    <p class="subtitle">
      Monte seu PC gamer com compatibilidade automática, FPS estimado e análise de gargalo.
    </p>
  </div>

  <button class="btn-limpar" @click="limparSelecao">
    Limpar seleção
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
      <h2>Seu Setup</h2>

      <div class="setup-grid">
        <div class="setup-card">
          <strong>CPU</strong>
          <span>{{ cpuSelecionada.nome }}</span>
        </div>

        <div class="setup-card">
          <strong>GPU</strong>
          <span>{{ gpuSelecionada.nome }}</span>
        </div>

        <div class="setup-card">
          <strong>Placa-Mãe</strong>
          <span>{{ placaSelecionada.nome }}</span>
        </div>
      </div>

      <hr>

      <h3>FPS Estimado</h3>

      <p>
        Valorant:
        {{ gpuSelecionada.fps_valorant }} FPS
      </p>

      <p>
        GTA V:
        {{ gpuSelecionada.fps_gta }} FPS
      </p>

      <p>
        Cyberpunk:
        {{ gpuSelecionada.fps_cyberpunk }} FPS
      </p>

      <hr>

     <div class="stats-grid">

  <div class="stat-card purple">
    <span>💰 Preço Total</span>
    <strong>R$ {{ precoTotal.toFixed(2) }}</strong>
  </div>

  <div class="stat-card blue">
    <span>⚡ Consumo</span>
    <strong>{{ consumoTotal }}W</strong>
  </div>

  <div class="stat-card green">
    <span>🔋 Fonte Ideal</span>
    <strong>{{ fonteIdeal }}</strong>
  </div>

  <div class="stat-card yellow">
    <span>🏆 Categoria</span>
    <strong>{{ categoriaSetup }}</strong>
  </div>

</div>

<div class="compatibilidade-box">
  {{ compatibilidade }}
</div>

      <h3>Análise de Gargalo</h3>

      <p>
        {{ gargalo }}
      </p>

      <button class="btn-salvar" @click="salvarBuild">
        Salvar Build
      </button>
    </div>

   <div class="builds-salvas">
  <h2>Builds Salvas</h2>

  <div
    v-for="build in buildsSalvas"
    :key="build.id"
    class="build-card"
  >
     <h3>{{ build.cpu }}</h3>

     <p>{{ build.gpu }}</p>

     <p>{{ build.motherboard }}</p>

     <p>💰 R$ {{ build.preco_total.toFixed(2) }}</p>
 
     <p>⚡ {{ build.consumo_total }}W</p>

     <button
       class="btn-deletar"
       @click="deletarBuild(build.id)"
     >
       Excluir Build
       </button>
    </div>
    </div>
  </div>
</template>

<style>
body {
  margin: 0;
  background: radial-gradient(circle at top, #1e1b4b, #020617 60%);
  font-family: Arial, sans-serif;
}

.container {
  max-width: 1000px;
  margin: auto;
  padding: 40px;
  color: white;
}

h1 {
  font-size: 48px;
  margin-bottom: 40px;
  color: #a855f7;
  text-shadow: 0 0 20px #7c3aed;
}

.card {
  background: rgba(30, 41, 59, 0.75);
  padding: 24px;
  margin-bottom: 25px;
  border-radius: 22px;
  border: 1px solid rgba(124, 58, 237, 0.35);
  backdrop-filter: blur(12px);
  box-shadow:
    0 0 25px rgba(124, 58, 237, 0.18),
    inset 0 0 20px rgba(255, 255, 255, 0.02);

  transition:
    transform 0.25s ease,
    box-shadow 0.25s ease,
    border 0.25s ease;
}

.card:hover {
  transform: translateY(-6px);

  border: 1px solid #a855f7;

  box-shadow:
    0 0 35px rgba(168, 85, 247, 0.35),
    0 0 80px rgba(56, 189, 248, 0.12);
}

.card h2 {
  color: #38bdf8;
}

select {
  width: 100%;
  padding: 14px;
  border-radius: 14px;
  margin-top: 15px;

  background: rgba(2, 6, 23, 0.9);
  color: white;

  border: 1px solid rgba(124, 58, 237, 0.35);

  font-size: 16px;

  transition: 0.25s;
}

select:hover {
  border-color: #38bdf8;
}

select:focus {
  outline: none;

  border-color: #a855f7;

  box-shadow:
    0 0 20px rgba(168, 85, 247, 0.4);
}

.resultado {
  background: rgba(17, 24, 39, 0.95);
  padding: 30px;
  border-radius: 20px;
  margin-top: 30px;
  border: 2px solid #a855f7;
  box-shadow: 0 0 30px rgba(168, 85, 247, 0.45);
}

.resultado h2 {
  color: #22c55e;
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

.btn-limpar {
  display: block;
  margin: 0 auto 30px auto;
  padding: 12px 24px;
  background: linear-gradient(90deg, #7c3aed, #38bdf8);
  color: white;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  font-size: 16px;
  box-shadow: 0 0 20px rgba(124, 58, 237, 0.45);
}

.btn-limpar:hover {
  transform: scale(1.05);
} 

.setup-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
  margin-bottom: 25px;
}

.setup-card {
  background: #020617;
  border: 1px solid #38bdf8;
  padding: 18px;
  border-radius: 14px;
  box-shadow: 0 0 15px rgba(56, 189, 248, 0.25);
}

.setup-card strong {
  display: block;
  color: #38bdf8;
  margin-bottom: 8px;
}

.setup-card span {
  color: white;
}

.btn-salvar {
  margin-top: 25px;
  padding: 14px 28px;
  border: none;
  border-radius: 12px;
  background: linear-gradient(90deg, #22c55e, #38bdf8);
  color: white;
  font-size: 16px;
  cursor: pointer;
  box-shadow: 0 0 20px rgba(34, 197, 94, 0.4);
}

.builds-salvas {
  margin-top: 50px;
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
  max-width: 650px;
  color: #cbd5e1;
  font-size: 18px;
  line-height: 1.5;
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
  padding: 22px;
  border-radius: 18px;
  color: white;
  font-weight: bold;

  display: flex;
  flex-direction: column;
  gap: 10px;

  backdrop-filter: blur(10px);

  transition: 0.25s;
}

.stat-card:hover {
  transform: translateY(-4px) scale(1.02);
}

.stat-card span {
  font-size: 14px;
  opacity: 0.9;
}

.stat-card strong {
  font-size: 22px;
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

.compatibilidade-box {
  margin-top: 20px;
  padding: 18px;
  border-radius: 14px;
  background: rgba(15, 23, 42, 0.85);
  border: 1px solid #22c55e;
  font-size: 17px;
}

@media (max-width: 700px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>