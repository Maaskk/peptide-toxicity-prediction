<template>
  <div class="flex flex-col min-h-screen">
    <AppHeader />
    
    <main class="flex-1 w-full flex justify-center">
      <div class="mx-auto max-w-7xl px-6 flex flex-col">
        
        <section class="flex flex-col items-center text-center pt-32 pb-24 gap-8">
          <h1 class="text-3xl sm:text-4xl lg:text-5xl font-bold bg-gradient-to-r from-primary via-blue-500 to-purple-500 bg-clip-text text-transparent">
            Feature Analysis
          </h1>
          <p class="text-muted-foreground text-base sm:text-lg max-w-2xl">
            Analyze physicochemical properties and amino acid composition of peptide sequences.
          </p>
        </section>

        <section class="max-w-2xl mx-auto mt-32">
          <div class="bg-card/50 backdrop-blur-sm border border-border/50 rounded-2xl p-8 sm:p-10 shadow-xl">
      <div class="mb-8">
              <label class="block text-sm font-semibold mb-4 text-foreground text-center">Peptide Sequence</label>
            <textarea 
              v-model="sequence"
              placeholder="ACDEFGHIKLMNPQRSTVWY"
                rows="6"
                class="w-full px-4 py-3 bg-background/50 border border-border/50 rounded-xl font-mono text-sm sm:text-base resize-none focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary transition-all"
            ></textarea>
          </div>

            <div class="flex justify-center items-center w-full mt-6">
          <button 
            @click="analyze" 
            :disabled="loading || !sequence.trim()"
                class="px-12 py-4 bg-gradient-to-r from-primary to-blue-600 text-primary-foreground rounded-xl font-semibold hover:from-primary/90 hover:to-blue-600/90 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 flex items-center justify-center gap-2 shadow-lg hover:shadow-xl hover:scale-[1.02] active:scale-[0.98] text-base cursor-pointer">
            <Loader2 v-if="loading" class="w-5 h-5 animate-spin" />
            <span>{{ loading ? 'Analyzing...' : 'Analyze Features' }}</span>
          </button>
        </div>
          </div>
        </section>

        <section v-if="analysis || loading" class="max-w-2xl mx-auto mt-32">
          <div class="bg-card/50 backdrop-blur-sm border border-border/50 rounded-2xl p-8 sm:p-10 shadow-xl">
            <h2 class="text-xl sm:text-2xl font-bold mb-8 text-foreground text-center">Analysis Results</h2>
            
            <div v-if="loading" class="flex flex-col items-center justify-center h-64 sm:h-80">
              <div class="w-16 h-16 sm:w-20 sm:h-20 border-4 border-primary/20 border-t-primary rounded-full animate-spin mb-6"></div>
              <p class="text-muted-foreground text-base sm:text-lg font-medium">Extracting features...</p>
          </div>

            <div v-if="analysis && !loading" class="space-y-8 animate-in fade-in">
              <div class="grid grid-cols-2 gap-6 max-w-md mx-auto">
                <div class="p-4 sm:p-5 bg-gradient-to-br from-muted/50 to-muted/30 rounded-xl border border-border/50 text-center">
                  <div class="text-2xl sm:text-3xl font-bold mb-1">{{ analysis.length }}</div>
                  <div class="text-xs sm:text-sm text-muted-foreground font-medium">Length (aa)</div>
                </div>
                <div class="p-4 sm:p-5 bg-gradient-to-br from-muted/50 to-muted/30 rounded-xl border border-border/50 text-center">
                  <div class="text-2xl sm:text-3xl font-bold mb-1">{{ analysis.physicochemicalProperties.netCharge.toFixed(1) }}</div>
                  <div class="text-xs sm:text-sm text-muted-foreground font-medium">Net Charge</div>
              </div>
            </div>

              <div class="p-5 sm:p-6 bg-background/50 rounded-xl border border-border/50">
                <h3 class="font-semibold text-base sm:text-lg mb-6 text-center">Physicochemical Properties</h3>
                <div class="space-y-5">
            <div>
                    <div class="flex justify-between text-sm sm:text-base mb-2 font-medium">
                    <span>Hydrophobicity</span>
                    <span>{{ analysis.physicochemicalProperties.hydrophobicity.toFixed(2) }}</span>
                  </div>
                    <div class="h-3 bg-muted/50 rounded-full overflow-hidden shadow-inner">
                      <div class="h-full bg-gradient-to-r from-blue-500 to-cyan-500 rounded-full transition-all duration-500" 
                           :style="{ width: `${Math.min(Math.abs(analysis.physicochemicalProperties.hydrophobicity) * 20, 100)}%` }"></div>
                    </div>
                </div>

                <div>
                    <div class="flex justify-between text-sm sm:text-base mb-2 font-medium">
                    <span>Aromatic Content</span>
                    <span>{{ analysis.physicochemicalProperties.aromaticContent.toFixed(1) }}%</span>
                  </div>
                    <div class="h-3 bg-muted/50 rounded-full overflow-hidden shadow-inner">
                      <div class="h-full bg-gradient-to-r from-purple-500 to-pink-500 rounded-full transition-all duration-500" 
                           :style="{ width: `${analysis.physicochemicalProperties.aromaticContent}%` }"></div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="p-5 sm:p-6 bg-background/50 rounded-xl border border-border/50">
                <h3 class="font-semibold text-base sm:text-lg mb-6 text-center">Amino Acid Composition</h3>
                <div class="space-y-3 max-h-64 overflow-y-auto custom-scrollbar pr-2">
                  <div v-for="(value, aa) in topAminoAcids" :key="aa" class="flex items-center gap-3">
                    <span class="font-mono text-sm sm:text-base w-8 font-semibold">{{ aa }}</span>
                    <div class="flex-1 h-6 bg-muted/50 rounded-lg overflow-hidden shadow-inner">
                      <div class="h-full bg-gradient-to-r from-green-500 to-emerald-500 flex items-center px-2 transition-all duration-500" 
                           :style="{ width: `${value}%` }">
                        <span class="text-xs text-white font-medium whitespace-nowrap">{{ value.toFixed(1) }}%</span>
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
import { ref, computed } from 'vue'
import { BarChart3, Loader2 } from 'lucide-vue-next'
import AppHeader from '../components/AppHeader.vue'
import { analyzeFeatures } from '../services/api'

const sequence = ref('')
const loading = ref(false)
const analysis = ref<any>(null)

const analyze = async () => {
  loading.value = true
  analysis.value = null

  try {
    const response = await analyzeFeatures(sequence.value.trim())
    if (response.success) {
    analysis.value = response.data
    } else {
      throw new Error(response.message || 'Analysis failed')
    }
  } catch (error: any) {
    console.error('Analysis failed:', error)
    alert(error.message || 'Analysis failed. Please check your input and try again.')
  } finally {
    loading.value = false
  }
}

const topAminoAcids = computed(() => {
  if (!analysis.value) return {}
  
  const aac = analysis.value.aminoAcidComposition
  const sorted = Object.entries(aac)
    .filter(([, value]: [string, any]) => value > 0)
    .sort(([, a]: [string, any], [, b]: [string, any]) => b - a)
    .slice(0, 10)
  
  return Object.fromEntries(sorted)
})
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

.animate-in {
  animation: fade-in 0.3s ease-out;
}

.fade-in {
  animation: fade-in 0.3s ease-out;
}
</style>
