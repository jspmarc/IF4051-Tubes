<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";
import type { Ref } from "vue";
import HomeView from "./components/HomeView.vue";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
} from "chart.js";
import "chart.js/auto";
import annotationPlugin from "chartjs-plugin-annotation";
import AppMode from "./types/AppMode";
import type AppState from "./types/AppState";

const StatsView = defineAsyncComponent(
  () => import("./components/StatsView.vue")
);

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  annotationPlugin
);

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

const currentView: Ref<"home" | "stats" | "alert"> = ref("home");
</script>

<template>
  <header>
    <nav class="flex flex-row">
      <ul class="selection bg-gray-1 flex flex-row gap-6 p-1 my-2.5 rounded-full text-primary-text">
        <li class=""><button class="rounded-full py-1 px-5" :class="{ 'bg-gray-2': currentView === 'home'}" @click="() => currentView = 'home'">HOME</button></li>
        <li class=""><button class="rounded-full py-1 px-5" :class="{ 'bg-gray-2': currentView === 'stats'}" @click="() => currentView = 'stats'">STATS</button></li>
        <li class=""><button class="rounded-full py-1 px-5" :class="{ 'bg-gray-2': currentView === 'alert'}" @click="() => currentView = 'alert'">ALERTS</button></li>
      </ul>
    </nav>
  </header>

  <HomeView
    v-show="currentView === 'home'"
    class="my-2.5"
    :url="httpBeUrl"
    :ws-connection="wsConnection"
    :app-state="appState"
  />

  <div class="h-full w-full" v-show="currentView === 'stats'">
    <Suspense>
      <StatsView :app-state="appState" :be-url="httpBeUrl" />

      <template #fallback> Loading... </template>
    </Suspense>
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
