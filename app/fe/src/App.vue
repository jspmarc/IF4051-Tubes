<script setup lang="ts">
// import HelloWorld from './components/HelloWorld.vue'
import HomeView from './components/HomeView.vue';

const beUrn = import.meta.env.VITE_BACKEND_URN;
const wsBeUrl = `ws://${beUrn}/state/ws`;
const httpBeUrl = `http://${beUrn}`;
let wsConnection = new WebSocket(wsBeUrl);
</script>

<template>
  <div class="flex w-full place-self-center">
    <HomeView :url="httpBeUrl"
              :ws-connection="wsConnection" />
  </div>
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
