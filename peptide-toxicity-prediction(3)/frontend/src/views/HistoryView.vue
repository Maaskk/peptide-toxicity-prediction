<template>
  <div class="flex flex-col min-h-screen">
    <AppHeader />
    
    <main class="flex-1 w-full flex justify-center">
      <div class="mx-auto max-w-7xl px-6 flex flex-col">
        
        <section class="flex flex-col items-center text-center pt-32 pb-24 gap-8">
          <h1 class="text-3xl sm:text-4xl lg:text-5xl font-bold bg-gradient-to-r from-primary via-blue-500 to-purple-500 bg-clip-text text-transparent">
            Prediction History
          </h1>
          <p class="text-muted-foreground text-base sm:text-lg max-w-2xl">
            View and manage your past predictions with advanced search and filtering.
          </p>
        </section>

        <section class="grid grid-cols-1 lg:grid-cols-3 gap-8 mt-32">
          <div class="lg:col-span-2 bg-card/50 backdrop-blur-sm border border-border/50 rounded-2xl p-6 sm:p-8 shadow-lg">
            <div class="flex gap-4">
            <div class="relative flex-1">
              <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
              <input 
                v-model="searchQuery"
                @keyup.enter="search"
                type="text"
                placeholder="Search by sequence..."
                  class="w-full pl-10 pr-4 py-3 bg-background/50 border border-border/50 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary transition-all"
              />
            </div>
            <button 
              @click="search"
                class="px-6 py-3 bg-gradient-to-r from-primary to-blue-600 text-primary-foreground rounded-xl font-semibold hover:from-primary/90 hover:to-blue-600/90 transition-all duration-200 shadow-lg hover:shadow-xl cursor-pointer">
              Search
            </button>
          </div>
        </div>

          <div class="bg-card/50 backdrop-blur-sm border border-border/50 rounded-2xl p-6 sm:p-8 shadow-lg">
          <div class="text-center">
              <div class="text-3xl sm:text-4xl font-bold mb-2">{{ stats.totalPredictions }}</div>
              <div class="text-sm sm:text-base text-muted-foreground font-medium mb-4">Total Predictions</div>
              <div class="flex gap-4 justify-center text-xs sm:text-sm">
                <span class="px-3 py-1.5 bg-red-500/10 text-red-500 rounded-full font-medium">{{ stats.toxicPredictions }} toxic</span>
                <span class="px-3 py-1.5 bg-green-500/10 text-green-500 rounded-full font-medium">{{ stats.nonToxicPredictions }} safe</span>
              </div>
            </div>
          </div>
        </section>

        <section class="py-20">
          <div class="bg-card/50 backdrop-blur-sm border border-border/50 rounded-2xl shadow-xl overflow-hidden">
            <div class="p-6 border-b border-border/50 flex items-center justify-between bg-background/30">
              <h2 class="text-xl sm:text-2xl font-bold text-foreground">Recent Predictions</h2>
          <button 
            @click="loadHistory"
                class="p-2 hover:bg-accent/50 rounded-xl transition-all duration-200 hover:scale-110 active:scale-95">
            <RefreshCw :class="['w-5 h-5', loading && 'animate-spin']" />
          </button>
        </div>

            <div v-if="loading && !history.length" class="flex items-center justify-center py-16">
              <div class="text-center">
                <div class="w-16 h-16 border-4 border-primary/20 border-t-primary rounded-full animate-spin mx-auto mb-4"></div>
                <p class="text-muted-foreground">Loading history...</p>
              </div>
        </div>

            <div v-else-if="!history.length" class="flex flex-col items-center justify-center py-16 text-muted-foreground">
              <div class="w-20 h-20 mb-6 rounded-full bg-gradient-to-br from-primary/10 to-blue-500/10 flex items-center justify-center">
                <Clock class="w-10 h-10 opacity-30" />
              </div>
              <p class="text-base sm:text-lg font-medium mb-2">No prediction history yet</p>
              <p class="text-sm text-center">Start making predictions to see them here</p>
        </div>

            <div v-else class="divide-y divide-border/50">
              <div v-for="item in history" :key="item.id" 
                   class="p-6 sm:p-8 hover:bg-accent/30 transition-all duration-200">
            <div class="flex items-start justify-between gap-4">
              <div class="flex-1 min-w-0">
                    <div class="flex items-center gap-3 mb-3 flex-wrap">
                      <span class="font-mono text-xs sm:text-sm bg-muted/50 px-3 py-1.5 rounded-lg">
                        {{ item.sequence.substring(0, 30) }}{{ item.sequence.length > 30 ? '...' : '' }}
                  </span>
                      <span :class="['px-3 py-1.5 rounded-full text-xs sm:text-sm font-semibold', 
                                     item.result.prediction === 'Toxic' ? 'bg-red-500/10 text-red-500 border border-red-500/20' : 'bg-green-500/10 text-green-500 border border-green-500/20']">
                    {{ item.result.prediction }}
                  </span>
                </div>
                
                    <div class="flex items-center gap-4 sm:gap-6 text-xs sm:text-sm text-muted-foreground flex-wrap">
                      <div class="flex items-center gap-1.5">
                        <Brain class="w-4 h-4" />
                    <span>{{ getModelName(item.model) }}</span>
                  </div>
                      <div class="flex items-center gap-1.5">
                        <TrendingUp class="w-4 h-4" />
                    <span>{{ (item.result.confidence * 100).toFixed(1) }}% confidence</span>
                  </div>
                      <div class="flex items-center gap-1.5">
                        <Clock class="w-4 h-4" />
                    <span>{{ formatDate(item.timestamp) }}</span>
                  </div>
                </div>
              </div>

              <div class="flex gap-2">
                <button 
                  @click="viewDetails(item)"
                      class="p-2 hover:bg-accent/50 rounded-lg transition-all duration-200 hover:scale-110 active:scale-95"
                  title="View details">
                      <Eye class="w-4 h-4 sm:w-5 sm:h-5" />
                </button>
                <button 
                  @click="copySequence(item.sequence)"
                      class="p-2 hover:bg-accent/50 rounded-lg transition-all duration-200 hover:scale-110 active:scale-95"
                  title="Copy sequence">
                      <Copy class="w-4 h-4 sm:w-5 sm:h-5" />
                </button>
              </div>
            </div>
          </div>
        </div>

            <div v-if="history.length > 0" class="p-4 sm:p-6 border-t border-border/50 text-center bg-background/30">
          <button 
            @click="loadMore"
            :disabled="loadingMore"
                class="px-6 py-2.5 text-sm sm:text-base font-medium text-primary hover:bg-primary/10 rounded-xl transition-all duration-200 disabled:opacity-50 cursor-pointer">
            {{ loadingMore ? 'Loading...' : 'Load More' }}
          </button>
        </div>
          </div>
        </section>
      </div>
    </main>

    <div v-if="selectedItem" 
         class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 z-50 animate-in fade-in"
         @click.self="selectedItem = null">
      <div class="bg-card/95 backdrop-blur-md border border-border/50 rounded-2xl max-w-2xl w-full max-h-[85vh] overflow-y-auto shadow-2xl">
        <div class="p-6 border-b border-border/50 flex items-start justify-between bg-background/30 sticky top-0">
          <h3 class="text-xl sm:text-2xl font-bold text-foreground">Prediction Details</h3>
          <button 
            @click="selectedItem = null" 
            class="p-2 hover:bg-accent/50 rounded-xl transition-all duration-200 hover:scale-110 active:scale-95">
            <X class="w-5 h-5" />
          </button>
        </div>

        <div class="p-6 space-y-6">
          <div>
            <label class="text-xs sm:text-sm font-semibold text-muted-foreground uppercase tracking-wide mb-2 block">Sequence</label>
            <p class="font-mono text-xs sm:text-sm bg-muted/30 p-3 sm:p-4 rounded-xl break-all">{{ selectedItem.sequence }}</p>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div class="p-4 bg-background/50 rounded-xl border border-border/50">
              <label class="text-xs sm:text-sm font-semibold text-muted-foreground uppercase tracking-wide mb-2 block">Prediction</label>
              <p :class="['text-lg sm:text-xl font-bold mt-1', 
                         selectedItem.result.prediction === 'Toxic' ? 'text-red-500' : 'text-green-500']">
                {{ selectedItem.result.prediction }}
              </p>
            </div>
            <div class="p-4 bg-background/50 rounded-xl border border-border/50">
              <label class="text-xs sm:text-sm font-semibold text-muted-foreground uppercase tracking-wide mb-2 block">Confidence</label>
              <p class="text-lg sm:text-xl font-bold mt-1">{{ (selectedItem.result.confidence * 100).toFixed(1) }}%</p>
            </div>
          </div>

          <div class="p-4 sm:p-5 bg-background/50 rounded-xl border border-border/50">
            <label class="text-xs sm:text-sm font-semibold text-muted-foreground uppercase tracking-wide mb-4 block">Probability Distribution</label>
            <div class="space-y-4">
              <div>
                <div class="flex justify-between text-sm sm:text-base mb-2 font-medium">
                  <span class="text-red-500">Toxic</span>
                  <span class="text-red-500">{{ (selectedItem.result.probability.toxic * 100).toFixed(1) }}%</span>
                </div>
                <div class="h-3 bg-muted/50 rounded-full overflow-hidden shadow-inner">
                  <div class="h-full bg-gradient-to-r from-red-500 to-rose-500 rounded-full transition-all duration-500" 
                       :style="{ width: `${selectedItem.result.probability.toxic * 100}%` }"></div>
                </div>
              </div>
              <div>
                <div class="flex justify-between text-sm sm:text-base mb-2 font-medium">
                  <span class="text-green-500">Non-Toxic</span>
                  <span class="text-green-500">{{ (selectedItem.result.probability.non_toxic * 100).toFixed(1) }}%</span>
                </div>
                <div class="h-3 bg-muted/50 rounded-full overflow-hidden shadow-inner">
                  <div class="h-full bg-gradient-to-r from-green-500 to-emerald-500 rounded-full transition-all duration-500" 
                       :style="{ width: `${selectedItem.result.probability.non_toxic * 100}%` }"></div>
                </div>
              </div>
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div class="p-4 bg-background/50 rounded-xl border border-border/50">
              <label class="text-xs sm:text-sm font-semibold text-muted-foreground uppercase tracking-wide mb-2 block">Model</label>
              <p class="text-sm sm:text-base font-medium mt-1">{{ getModelName(selectedItem.model) }}</p>
            </div>
            <div class="p-4 bg-background/50 rounded-xl border border-border/50">
              <label class="text-xs sm:text-sm font-semibold text-muted-foreground uppercase tracking-wide mb-2 block">Timestamp</label>
              <p class="text-sm sm:text-base font-medium mt-1">{{ formatDate(selectedItem.timestamp, true) }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Clock, Loader2, Search, Brain, TrendingUp, Eye, Copy, X, RefreshCw } from 'lucide-vue-next'
import AppHeader from '../components/AppHeader.vue'
import { getHistory, getStats } from '../services/api'

const loading = ref(true)
const loadingMore = ref(false)
const history = ref<any[]>([])
const stats = ref({
  totalPredictions: 0,
  toxicPredictions: 0,
  nonToxicPredictions: 0
})
const searchQuery = ref('')
const selectedItem = ref<any>(null)
const currentLimit = ref(20)

const loadHistory = async () => {
  loading.value = true
  try {
    const [historyResponse, statsResponse] = await Promise.all([
      getHistory(currentLimit.value),
      getStats()
    ])
    if (historyResponse.success) {
    history.value = historyResponse.data.predictions
    }
    if (statsResponse.success) {
    stats.value = statsResponse.data
    }
  } catch (error) {
    console.error('Failed to load history:', error)
  } finally {
    loading.value = false
  }
}

const loadMore = async () => {
  loadingMore.value = true
  currentLimit.value += 20
  try {
    const response = await getHistory(currentLimit.value)
    if (response.success) {
    history.value = response.data.predictions
    }
  } catch (error) {
    console.error('Failed to load more:', error)
  } finally {
    loadingMore.value = false
  }
}

const search = async () => {
  if (!searchQuery.value.trim()) {
    loadHistory()
    return
  }
  
  loading.value = true
  try {
    console.log('Searching for:', searchQuery.value)
  } catch (error) {
    console.error('Search failed:', error)
  } finally {
    loading.value = false
  }
}

const viewDetails = (item: any) => {
  selectedItem.value = item
}

const copySequence = (sequence: string) => {
  navigator.clipboard.writeText(sequence)
}

const getModelName = (modelId: string) => {
  const models: Record<string, string> = {
    ensemble: 'Ensemble',
    logistic_regression: 'Logistic Regression',
    random_forest: 'Random Forest',
    svm: 'SVM'
  }
  return models[modelId] || modelId
}

const formatDate = (timestamp: string, detailed = false) => {
  const date = new Date(timestamp)
  if (detailed) {
    return date.toLocaleString()
  }
  
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)
  
  if (minutes < 1) return 'Just now'
  if (minutes < 60) return `${minutes}m ago`
  if (hours < 24) return `${hours}h ago`
  if (days < 7) return `${days}d ago`
  return date.toLocaleDateString()
}

onMounted(() => {
  loadHistory()
})
</script>

<style scoped>
@keyframes fade-in {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.animate-in {
  animation: fade-in 0.2s ease-out;
}

.fade-in {
  animation: fade-in 0.2s ease-out;
}
</style>
