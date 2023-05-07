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
import passwordHelper from "./helpers/password";

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

const beUrn: string = import.meta.env.VITE_BACKEND_URN;
const wsBeUrl: string = (import.meta.env.VITE_IS_SECURE ? "wss://" : "ws://") + `${beUrn}/state/ws`;
const httpBeUrl: string = (import.meta.env.VITE_IS_SECURE ? "https://" : "http://") + beUrn;
const wsConnection = new WebSocket(wsBeUrl);

wsConnection.onmessage = (event) => {
  let data: AppState = JSON.parse(event.data);
  appState.value = data;
};

const currentView: Ref<"home" | "stats" | "alert"> = ref("home");

const loginDialogRef: Ref<HTMLDialogElement | undefined | null> = ref(null);
const savePasswordForm: Ref<HTMLFormElement | undefined | null> = ref(null);
const password: Ref<string | null> = ref(passwordHelper.getPassword());

function savePassword(e: Event) {
  if (savePasswordForm.value == null || password.value == null) {
    e.preventDefault();
    return;
  }

  passwordHelper.savePassword(password.value);
}
</script>

<template>
  <dialog ref="loginDialogRef" class="bg-black" @submit="savePassword">
    <button @click="loginDialogRef?.close">X</button>
    <h2 class="font-bold">Insert password</h2>
    <form method="dialog" ref="savePasswordForm">
      <input type="password" placeholder="Insert password here" v-model="password" />
      <button type="submit" class="font-normal">Save password</button>
    </form>
  </dialog>
  <header>
    <nav class="flex flex-row">
      <ul class="selection gray-1 flex flex-row items-center gap-6 p-1 rounded-full">
        <li class="rounded-full"><button class="p-1" @click="() => currentView = 'home'">HOME</button></li>
        <li class="rounded-full"><button class="p-1" @click="() => currentView = 'stats'">STATS</button></li>
        <li class="rounded-full"><button class="p-1" @click="() => currentView = 'alert'">ALERTS</button></li>
        <li><button @click="loginDialogRef?.showModal">Update password</button></li>
      </ul>
    </nav>
  </header>

  <HomeView v-show="currentView === 'home'" :url="httpBeUrl" :ws-connection="wsConnection" :app-state="appState" />

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
