<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";
import type { Ref } from "vue";
import HomeView from "./components/HomeView.vue";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from "chart.js"
import "chart.js/auto"
import AppMode from "./types/AppMode";
import type AppState from "./types/AppState";

const StatsView = defineAsyncComponent(() => import("./components/StatsView.vue"));

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

let appState: Ref<AppState> = ref({
  current_mode: AppMode.Ai,
  active_alarms: [],
  servo_multiple: 0,
  dht22_statistics: {
    humidity_avg: 0,
    humidity_max: 0,
    humidity_min: 0,
    temperature_avg: 0,
    temperature_max: 0,
    temperature_min: 0,
    created_timestamp: 0,
  },
  mq135_statistics: {
    co2_avg: 0,
    co2_max: 0,
    co2_min: 0,
    created_timestamp: 0,
  },
});

const beUrn = import.meta.env.VITE_BACKEND_URN;
const wsBeUrl = `ws://${beUrn}/state/ws`;
const httpBeUrl = `http://${beUrn}`;
const wsConnection = new WebSocket(wsBeUrl);

wsConnection.onmessage = (event) => {
  let data: AppState = JSON.parse(event.data);
  appState.value = data;
};
</script>

<template>
  <header>
    <nav>
      halo
    </nav>
  </header>
  <Suspense>
    <StatsView />

    <template #fallback>
        Loading...
    </template>
  </Suspense>
  <!-- <HomeView :url="httpBeUrl" :ws-connection="wsConnection" :app-state="appState" /> -->
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
