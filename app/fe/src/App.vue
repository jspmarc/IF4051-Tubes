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
import Recommendation from "./components/Recommendation.vue";

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
  // is_recommending: false,
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
const isRecommending: Ref<boolean> = ref(true);
</script>

<template>
  <header>
    <nav class="flex flex-row mb-6">
      <ul class="selection gray-1 flex flex-row gap-6 p-1 rounded-full menu">
        <li class="rounded-full">
          <button
            class="p-1"
            @click="() => (currentView = 'home')"
            :class="currentView == 'home' ? 'gray-2' : 'gray-1'"
          >
            <template v-if="currentView === 'home'"
              ><div class="w-[13px] h-[13px] blue rounded-[14px]"></div
            ></template>
            <template v-else
              ><div
                class="w-[13px] h-[13px] border-[1px] border-black rounded-[14px]"
              ></div
            ></template>
            HOME
          </button>
        </li>
        <li class="rounded-full">
          <button
            class="p-1"
            @click="() => (currentView = 'stats')"
            :class="currentView == 'stats' ? 'gray-2' : 'gray-1'"
          >
            <template v-if="currentView === 'stats'"
              ><div class="w-[13px] h-[13px] blue rounded-[14px]"></div
            ></template>
            <template v-else
              ><div
                class="w-[13px] h-[13px] border-[1px] border-black rounded-[14px]"
              ></div
            ></template>
            STATS
          </button>
        </li>
        <li class="rounded-full">
          <button
            class="p-1"
            @click="() => (currentView = 'alert')"
            :class="currentView == 'alert' ? 'gray-2' : 'gray-1'"
          >
            <template v-if="currentView === 'alert'"
              ><div class="w-[13px] h-[13px] blue rounded-[14px]"></div
            ></template>
            <template v-else
              ><div
                class="w-[13px] h-[13px] border-[1px] border-black rounded-[14px]"
              ></div
            ></template>
            ALERTS
          </button>
        </li>
      </ul>
    </nav>
  </header>
  <Recommendation :is-recommending="isRecommending" title="Title" body="Body" />
  <HomeView
    v-show="currentView === 'home'"
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

.menu {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  /* padding: 0px 8px 0px 0px; */
  padding: 8px;
  gap: 12px;

  height: 56px;

  /* gray 1 */
  background: #e0e0de;
  border-radius: 32px;
}

.menu li button {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  padding: 10px 24px;
  gap: 8px;

  height: 44px;

  border-radius: 30px;

  font-weight: 500;
  font-size: 20px;
  line-height: 24px;

  /* black */
  color: #000000;
}
</style>
