<template>
  <div class="flex flex-col min-h-screen">
    <AppHeader />
    
    <main class="flex-1 w-full flex justify-center">
      <div class="mx-auto max-w-7xl px-6 flex flex-col">
        
        <section class="flex flex-col items-center text-center pt-32 pb-24 gap-8">
          <h1 class="text-3xl sm:text-4xl lg:text-5xl font-bold bg-gradient-to-r from-primary via-blue-500 to-purple-500 bg-clip-text text-transparent">
            Predict Peptide Toxicity
          </h1>
          <p class="text-muted-foreground text-base sm:text-lg max-w-2xl">
            Enter peptide sequences to predict their toxicity using advanced machine learning models trained on validated datasets.
          </p>
          <div class="flex flex-wrap justify-center gap-2 sm:gap-3">
            <span class="px-3 py-1.5 bg-primary/10 text-primary rounded-full text-xs sm:text-sm font-medium border border-primary/20">
              ML-Powered
            </span>
            <span class="px-3 py-1.5 bg-green-500/10 text-green-500 rounded-full text-xs sm:text-sm font-medium border border-green-500/20">
              Validated Models
            </span>
            <span class="px-3 py-1.5 bg-blue-500/10 text-blue-500 rounded-full text-xs sm:text-sm font-medium border border-blue-500/20">
              Real-time Analysis
            </span>
      </div>
        </section>

        <section class="grid grid-cols-1 xl:grid-cols-2 gap-8 lg:gap-12 mt-32">
          <div class="bg-card/50 backdrop-blur-sm border border-border/50 rounded-2xl p-8 sm:p-10 shadow-xl hover:shadow-2xl transition-all duration-300">
            <div class="mb-8">
              <label class="block text-sm font-semibold mb-3 text-foreground text-center">Prediction Mode</label>
              <div class="flex gap-2 sm:gap-3 justify-center">
              <button 
                @click="mode = 'single'" 
                  :class="mode === 'single' 
                    ? 'bg-primary text-primary-foreground shadow-lg scale-105' 
                    : 'bg-secondary/50 text-secondary-foreground hover:bg-secondary/70'"
                  class="flex-1 py-2.5 sm:py-3 rounded-xl font-medium transition-all duration-200 text-sm sm:text-base">
                Single Sequence
              </button>
              <button 
                @click="mode = 'batch'" 
                  :class="mode === 'batch' 
                    ? 'bg-primary text-primary-foreground shadow-lg scale-105' 
                    : 'bg-secondary/50 text-secondary-foreground hover:bg-secondary/70'"
                  class="flex-1 py-2.5 sm:py-3 rounded-xl font-medium transition-all duration-200 text-sm sm:text-base">
                Batch
              </button>
            </div>
          </div>

            <div class="mb-8">
              <label class="block text-sm font-semibold mb-4 text-foreground text-center">ML Model</label>
              <select 
                v-model="selectedModel" 
                class="w-full px-4 py-3 bg-background/50 border border-border/50 rounded-xl text-sm sm:text-base focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary transition-all">
              <option value="ensemble">Ensemble (Recommended)</option>
              <option value="logistic_regression">Logistic Regression</option>
              <option value="random_forest">Random Forest</option>
              <option value="svm">Support Vector Machine</option>
            </select>
          </div>

            <div class="mb-8">
              <label class="block text-sm font-semibold mb-4 text-foreground text-center">
              {{ mode === 'single' ? 'Peptide Sequence' : 'Peptide Sequences (one per line)' }}
            </label>
            <textarea 
              v-model="inputSequence"
              :placeholder="mode === 'single' ? 'ACDEFGHIKLMNPQRSTVWY' : 'ACDEFGHIK\nMKLPQRSTVWY\nFGHIKLMNP'"
                :rows="mode === 'single' ? 5 : 8"
                class="w-full px-4 py-3 bg-background/50 border border-border/50 rounded-xl font-mono text-sm sm:text-base resize-none focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary transition-all"
            ></textarea>
              <p class="text-xs text-muted-foreground mt-2 leading-relaxed text-center">
                Use standard amino acid letters (A, C, D, E, F, G, H, I, K, L, M, N, P, Q, R, S, T, V, W, Y)
              </p>
              <div class="mt-4 flex flex-wrap gap-2 justify-center">
                <button 
                  @click="inputSequence = 'GIGAVLKVLTTGLPALISWIKRKRQQ'" 
                  class="text-xs sm:text-sm px-3 py-1.5 bg-muted/50 hover:bg-muted border border-border/50 rounded-lg text-muted-foreground hover:text-foreground transition-all duration-200">
                  Example: Toxic
                </button>
                <button 
                  @click="inputSequence = 'GIVEQCCTSICSLYQLENYCN'" 
                  class="text-xs sm:text-sm px-3 py-1.5 bg-muted/50 hover:bg-muted border border-border/50 rounded-lg text-muted-foreground hover:text-foreground transition-all duration-200">
                  Example: Non-Toxic
                </button>
              </div>
          </div>

            <div class="flex justify-center items-center w-full">
          <button 
            @click="predict" 
            :disabled="loading || !inputSequence.trim()"
                class="px-12 py-4 bg-gradient-to-r from-primary to-blue-600 text-primary-foreground rounded-xl font-semibold hover:from-primary/90 hover:to-blue-600/90 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 flex items-center justify-center gap-2 shadow-lg hover:shadow-xl hover:scale-[1.02] active:scale-[0.98] text-base cursor-pointer">
            <Loader2 v-if="loading" class="w-5 h-5 animate-spin" />
                <span>{{ loading ? 'Analyzing...' : 'Predict Toxicity' }}</span>
          </button>
        </div>

            <div v-if="!loading && result" class="mt-6 p-3 sm:p-4 bg-gradient-to-r from-green-500/10 to-emerald-500/10 border border-green-500/20 rounded-xl text-center">
              <p class="text-sm sm:text-base text-green-500 font-medium flex items-center justify-center gap-2">
                <CheckCircle2 class="w-5 h-5" />
                Prediction successful!
              </p>
            </div>
          </div>

          <div class="bg-card/50 backdrop-blur-sm border border-border/50 rounded-2xl p-8 sm:p-10 shadow-xl hover:shadow-2xl transition-all duration-300">
            <div class="mb-8 text-center">
              <h2 class="text-xl sm:text-2xl font-bold text-foreground mb-2">Prediction Results</h2>
              <button 
                v-if="result" 
                @click="result = null; errorMessage = ''" 
                class="text-sm text-muted-foreground hover:text-foreground transition-colors px-4 py-2 rounded-lg hover:bg-muted/50 mx-auto">
                Clear Results
              </button>
          </div>

            <div v-if="!result && !loading && !errorMessage" class="flex flex-col items-center justify-center h-64 sm:h-80 text-muted-foreground">
              <div class="w-20 h-20 sm:w-24 sm:h-24 mb-6 rounded-full bg-gradient-to-br from-primary/10 to-blue-500/10 flex items-center justify-center">
                <Activity class="w-10 h-10 sm:w-12 sm:h-12 opacity-30" />
              </div>
              <p class="text-base sm:text-lg font-medium mb-2">No predictions yet</p>
              <p class="text-sm text-muted-foreground text-center">Enter a sequence and click predict</p>
            </div>

            <div v-if="errorMessage" class="p-4 sm:p-5 bg-gradient-to-r from-red-500/10 to-rose-500/10 border border-red-500/20 rounded-xl mb-4 animate-in fade-in">
              <div class="flex items-start gap-3">
                <AlertCircle class="w-5 h-5 sm:w-6 sm:h-6 text-red-500 flex-shrink-0 mt-0.5" />
                <div class="flex-1">
                  <p class="font-semibold text-red-500 text-sm sm:text-base mb-1">Error</p>
                  <p class="text-sm sm:text-base text-red-400 leading-relaxed">{{ errorMessage }}</p>
                </div>
              </div>
                </div>

            <div v-if="loading" class="flex flex-col items-center justify-center h-64 sm:h-80">
              <div class="relative">
                <div class="w-16 h-16 sm:w-20 sm:h-20 border-4 border-primary/20 border-t-primary rounded-full animate-spin mb-6"></div>
                      </div>
              <p class="text-muted-foreground text-base sm:text-lg font-medium mb-2">Analyzing sequence...</p>
              <p class="text-xs sm:text-sm text-muted-foreground">This may take a few seconds</p>
                      </div>

            <div v-if="result && !loading" class="space-y-8 animate-in fade-in slide-in-from-bottom-4">
              <div v-if="mode === 'single'" class="space-y-6">
                <div class="p-5 sm:p-6 rounded-2xl border-2 shadow-lg transition-all duration-300" 
                     :class="result.result.prediction === 'Toxic' 
                       ? 'bg-gradient-to-br from-red-500/10 to-rose-500/10 border-red-500/30' 
                       : 'bg-gradient-to-br from-green-500/10 to-emerald-500/10 border-green-500/30'">
                  <div class="flex items-center gap-4 mb-3 justify-center">
                    <div class="w-12 h-12 sm:w-14 sm:h-14 rounded-full flex items-center justify-center"
                         :class="result.result.prediction === 'Toxic' ? 'bg-red-500/20' : 'bg-green-500/20'">
                      <AlertCircle v-if="result.result.prediction === 'Toxic'" class="w-7 h-7 sm:w-8 sm:h-8 text-red-500" />
                      <CheckCircle2 v-else class="w-7 h-7 sm:w-8 sm:h-8 text-green-500" />
                    </div>
                    <div>
                      <span class="text-2xl sm:text-3xl font-bold block" 
                            :class="result.result.prediction === 'Toxic' ? 'text-red-500' : 'text-green-500'">
                        {{ result.result.prediction }}
                      </span>
                      <p class="text-sm text-muted-foreground mt-1">
                        Confidence: <span class="font-semibold">{{ (result.result.confidence * 100).toFixed(1) }}%</span>
                      </p>
                    </div>
                  </div>
                </div>

                <div class="space-y-6">
                  <div class="p-5 bg-background/50 rounded-xl border border-border/50">
                    <label class="text-xs sm:text-sm font-semibold text-muted-foreground uppercase tracking-wide mb-2 block text-center">Sequence</label>
                    <p class="font-mono text-xs sm:text-sm bg-muted/30 p-3 rounded-lg break-all text-center">{{ result.sequence }}</p>
                  </div>

                  <div class="p-5 bg-background/50 rounded-xl border border-border/50">
                    <label class="text-xs sm:text-sm font-semibold text-muted-foreground uppercase tracking-wide mb-5 block text-center">Probability Distribution</label>
                    <div class="space-y-5">
                      <div>
                        <div class="flex justify-between text-sm sm:text-base mb-2 font-medium">
                          <span class="text-red-500">Toxic</span>
                          <span class="text-red-500">{{ (result.result.probability.toxic * 100).toFixed(1) }}%</span>
                        </div>
                        <div class="h-3 bg-muted/50 rounded-full overflow-hidden shadow-inner">
                          <div class="h-full bg-gradient-to-r from-red-500 to-rose-500 rounded-full transition-all duration-500" 
                               :style="{ width: `${result.result.probability.toxic * 100}%` }"></div>
                        </div>
                      </div>
                <div>
                        <div class="flex justify-between text-sm sm:text-base mb-2 font-medium">
                          <span class="text-green-500">Non-Toxic</span>
                          <span class="text-green-500">{{ (result.result.probability.non_toxic * 100).toFixed(1) }}%</span>
                        </div>
                        <div class="h-3 bg-muted/50 rounded-full overflow-hidden shadow-inner">
                          <div class="h-full bg-gradient-to-r from-green-500 to-emerald-500 rounded-full transition-all duration-500" 
                               :style="{ width: `${result.result.probability.non_toxic * 100}%` }"></div>
                        </div>
                </div>
              </div>
            </div>

                  <div class="p-4 bg-background/50 rounded-xl border border-border/50">
                    <label class="text-xs sm:text-sm font-semibold text-muted-foreground uppercase tracking-wide mb-2 block text-center">Model Used</label>
                    <p class="text-sm sm:text-base font-medium text-center">{{ getModelName(result.model) }}</p>
                </div>
                </div>
              </div>

              <div v-else class="space-y-5">
                <div class="grid grid-cols-3 gap-3 sm:gap-4 max-w-md mx-auto">
                  <div class="text-center p-4 sm:p-5 bg-gradient-to-br from-muted/50 to-muted/30 rounded-xl border border-border/50">
                    <div class="text-2xl sm:text-3xl font-bold mb-1">{{ result.total }}</div>
                    <div class="text-xs sm:text-sm text-muted-foreground font-medium">Total</div>
                  </div>
                  <div class="text-center p-4 sm:p-5 bg-gradient-to-br from-red-500/10 to-rose-500/10 rounded-xl border border-red-500/20">
                    <div class="text-2xl sm:text-3xl font-bold text-red-500 mb-1">{{ result.toxic }}</div>
                    <div class="text-xs sm:text-sm text-muted-foreground font-medium">Toxic</div>
                  </div>
                  <div class="text-center p-4 sm:p-5 bg-gradient-to-br from-green-500/10 to-emerald-500/10 rounded-xl border border-green-500/20">
                    <div class="text-2xl sm:text-3xl font-bold text-green-500 mb-1">{{ result.nonToxic }}</div>
                    <div class="text-xs sm:text-sm text-muted-foreground font-medium">Non-Toxic</div>
                  </div>
                </div>

                <div class="max-h-96 overflow-y-auto space-y-2 pr-2 custom-scrollbar">
                <div v-for="(pred, idx) in result.predictions" :key="idx" 
                       class="p-4 rounded-xl border-2 transition-all duration-200 hover:scale-[1.02]"
                       :class="pred.result.prediction === 'Toxic' 
                         ? 'border-red-500/30 bg-gradient-to-r from-red-500/5 to-rose-500/5' 
                         : 'border-green-500/30 bg-gradient-to-r from-green-500/5 to-emerald-500/5'">
                    <div class="flex items-start justify-between gap-3">
                    <div class="flex-1 min-w-0">
                        <p class="font-mono text-xs sm:text-sm truncate mb-2 font-medium">{{ pred.sequence }}</p>
                        <p class="text-xs sm:text-sm font-semibold"
                           :class="pred.result.prediction === 'Toxic' ? 'text-red-500' : 'text-green-500'">
                          {{ pred.result.prediction }} 
                          <span class="text-muted-foreground">({{ (pred.result.confidence * 100).toFixed(1) }}%)</span>
                        </p>
                      </div>
                      <div class="flex-shrink-0">
                        <AlertCircle v-if="pred.result.prediction === 'Toxic'" class="w-5 h-5 sm:w-6 sm:h-6 text-red-500" />
                        <CheckCircle2 v-else class="w-5 h-5 sm:w-6 sm:h-6 text-green-500" />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Activity, Loader2, AlertCircle, CheckCircle2 } from 'lucide-vue-next'
import AppHeader from '../components/AppHeader.vue'
import { predictSingle, predictBatch } from '../services/api'

const mode = ref<'single' | 'batch'>('single')
const selectedModel = ref('ensemble')
const inputSequence = ref('')
const loading = ref(false)
const result = ref<any>(null)
const errorMessage = ref('')

const predict = async () => {
  loading.value = true
  result.value = null
  errorMessage.value = ''

  const sequence = inputSequence.value.trim()
  if (!sequence) {
    errorMessage.value = 'Please enter a peptide sequence'
    loading.value = false
    return
  }

  const validAAs = /^[ACDEFGHIKLMNPQRSTVWY]+$/i
  if (mode.value === 'single') {
    if (!validAAs.test(sequence)) {
      errorMessage.value = 'Invalid sequence. Only standard amino acids (A, C, D, E, F, G, H, I, K, L, M, N, P, Q, R, S, T, V, W, Y) are allowed.'
      loading.value = false
      return
    }
  } else {
    const sequences = sequence.split('\n').filter(s => s.trim())
    const invalid = sequences.filter(s => !validAAs.test(s.trim()))
    if (invalid.length > 0) {
      errorMessage.value = `Invalid sequences found. Only standard amino acids are allowed.`
      loading.value = false
      return
    }
  }

  try {
    if (mode.value === 'single') {
      const response = await predictSingle(sequence, selectedModel.value)
      if (response.success) {
      result.value = response.data
      } else {
        throw new Error(response.message || 'Prediction failed')
      }
    } else {
      const sequences = sequence.split('\n').filter(s => s.trim())
      const response = await predictBatch(sequences, selectedModel.value)
      if (response.success) {
      result.value = response.data
      } else {
        throw new Error(response.message || 'Batch prediction failed')
      }
    }
  } catch (error: any) {
    console.error('Prediction failed:', error)
    errorMessage.value = error.message || 'Failed to connect to prediction service. Please make sure the backend is running.'
  } finally {
    loading.value = false
  }
}

const getModelName = (modelId: string) => {
  const models: Record<string, string> = {
    ensemble: 'Ensemble (All Models)',
    logistic_regression: 'Logistic Regression',
    random_forest: 'Random Forest',
    svm: 'Support Vector Machine'
  }
  return models[modelId] || modelId
}
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: hsl(var(--muted));
  border-radius: 10px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: hsl(var(--primary));
  border-radius: 10px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: hsl(var(--primary) / 0.8);
}

@keyframes fade-in {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slide-in-from-bottom-4 {
  from {
    transform: translateY(1rem);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.animate-in {
  animation: fade-in 0.3s ease-out;
}

.fade-in {
  animation: fade-in 0.3s ease-out;
}

.slide-in-from-bottom-4 {
  animation: slide-in-from-bottom-4 0.4s ease-out;
}
</style>
