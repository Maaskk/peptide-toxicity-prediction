<template>
  <header class="w-full border-b border-border/50 bg-card/80 backdrop-blur-md sticky top-0 z-50 shadow-sm">
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 max-w-7xl">
      <div class="flex items-center justify-between h-16 sm:h-20">
        <router-link 
          to="/" 
          class="flex items-center gap-2 sm:gap-3 font-bold text-lg sm:text-xl hover:opacity-80 transition-opacity">
          <div class="w-9 h-9 sm:w-10 sm:h-10 rounded-xl bg-gradient-to-br from-primary to-blue-600 flex items-center justify-center shadow-lg">
            <Dna class="w-5 h-5 sm:w-6 sm:h-6 text-primary-foreground" />
          </div>
          <span class="hidden sm:inline">PeptideTox<span class="text-primary">AI</span></span>
          <span class="sm:hidden">PT<span class="text-primary">AI</span></span>
        </router-link>

        <nav class="hidden md:flex items-center gap-4">
          <router-link 
            v-for="link in navigation" 
            :key="link.path"
            :to="link.path"
            class="px-5 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 hover:bg-accent/50 mx-1"
            :class="route.path === link.path ? 'bg-accent text-foreground font-semibold' : 'text-muted-foreground hover:text-foreground'">
            {{ link.name }}
          </router-link>
        </nav>

        <div class="flex items-center gap-2 sm:gap-3">
          <button 
            @click="toggleTheme" 
            class="p-2 sm:p-2.5 rounded-xl hover:bg-accent/50 transition-all duration-200 hover:scale-110 active:scale-95">
            <Sun v-if="theme === 'dark'" class="w-5 h-5 sm:w-6 sm:h-6" />
            <Moon v-else class="w-5 h-5 sm:w-6 sm:h-6" />
          </button>
          
          <button 
            @click="mobileMenuOpen = !mobileMenuOpen"
            class="md:hidden p-2 rounded-xl hover:bg-accent/50 transition-all duration-200">
            <Menu class="w-5 h-5" />
          </button>
        </div>
      </div>

      <!-- Mobile Menu -->
      <div 
        v-if="mobileMenuOpen" 
        class="md:hidden pb-4 pt-2 border-t border-border/50 animate-in slide-in-from-top">
        <nav class="flex flex-col gap-2">
          <router-link 
            v-for="link in navigation" 
            :key="link.path"
            :to="link.path"
            @click="mobileMenuOpen = false"
            class="px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200"
            :class="route.path === link.path 
              ? 'bg-accent text-foreground font-semibold' 
              : 'text-muted-foreground hover:bg-accent/50 hover:text-foreground'">
            {{ link.name }}
          </router-link>
        </nav>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { Dna, Sun, Moon, Menu } from 'lucide-vue-next'

const route = useRoute()
const theme = ref<'light' | 'dark'>('dark')
const mobileMenuOpen = ref(false)

const navigation = [
  { name: 'Dashboard', path: '/' },
  { name: 'Predict', path: '/predict' },
  { name: 'Analysis', path: '/analysis' },
  { name: 'History', path: '/history' }
]

const toggleTheme = () => {
  theme.value = theme.value === 'light' ? 'dark' : 'light'
  document.documentElement.classList.toggle('dark')
}

document.documentElement.classList.add('dark')
</script>

<style scoped>
@keyframes slide-in-from-top {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-in {
  animation: slide-in-from-top 0.2s ease-out;
}
</style>
