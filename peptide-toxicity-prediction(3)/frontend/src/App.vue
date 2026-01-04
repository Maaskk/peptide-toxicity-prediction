<template>
  <div id="app" class="min-h-screen flex flex-col bg-background text-foreground">
    <router-view />
  </div>
</template>

<script setup lang="ts">
// Main app component
</script>

<style>
#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
</style>
