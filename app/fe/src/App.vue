<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";
import type { Ref } from "vue";
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
import HomeView from "./components/HomeView.vue";
import Recommendation from "./components/Recommendation.vue";
import AlertBox from "./components/AlertBox.vue";

const AlertView = defineAsyncComponent(
  () => import("./components/AlertView.vue")
);
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
const isAlerting: Ref<boolean> = ref(true);
</script>

<template>
  <header
    class="flex lg:w-2/6 md:w-3/6 sm:w-4/6 w-full mx-auto min-w-[450px] mb-6"
  >
    <nav class="w-full">
      <ul class="bg-gray-1 flex flex-row gap-3 rounded-full menu w-full">
        <li class="rounded-full">
          <button
            class=""
            @click="() => (currentView = 'home')"
            :class="{ 'bg-gray-2': currentView == 'home' }"
          >
            <template v-if="currentView === 'home'"
              ><div class="w-[13px] h-[13px] bg-blue rounded-[14px]"></div
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
            class=""
            @click="() => (currentView = 'stats')"
            :class="{ 'bg-gray-2': currentView == 'stats' }"
          >
            <template v-if="currentView === 'stats'"
              ><div class="w-[13px] h-[13px] bg-blue rounded-[14px]"></div
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
            class=""
            @click="
              () => {
                currentView = 'alert';
                isAlerting = false;
              }
            "
            :class="{
              'bg-gray-2': currentView == 'alert',
              'bg-yellow': isAlerting,
            }"
          >
            <template v-if="currentView === 'alert'"
              ><div class="w-[13px] h-[13px] bg-blue rounded-[14px]"></div
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

  <!-- RECOMMENDATION -->
  <Recommendation
    v-show="isRecommending"
    title="This is a Recommendation"
    body="Body"
    :cta-primary="
      () => {
        // TODO
        isRecommending = false;
      }
    "
    :cta-secondary="() => (isRecommending = false)"
  />

  <!-- ALERT -->
  <AlertBox
    v-show="isAlerting && currentView !== 'alert'"
    title="This is an Alert"
    body="Body"
    :temperature="40"
    :ppm="600"
    cta-primary-text="Acknowledge"
    :cta-primary="
      () => {
        // TODO adjust action(s) needed
        isAlerting = false;
      }
    "
    :cta-secondary="() => (isAlerting = false)"
    @click="
      currentView = 'alert';
      isAlerting = false;
    "
  />

  <!-- HOME VIEW -->
  <HomeView
    v-show="currentView === 'home'"
    class=""
    :url="httpBeUrl"
    :ws-connection="wsConnection"
    :app-state="appState"
  />

  <!-- STATS VIEW -->
  <div class="h-full w-full" v-show="currentView === 'stats'">
    <Suspense>
      <StatsView :app-state="appState" :be-url="httpBeUrl" />

      <template #fallback> Loading... </template>
    </Suspense>
  </div>

  <!-- ALERT VIEW -->
  <AlertView v-show="currentView === 'alert'" class=""> asdfsd</AlertView>
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
  justify-content: space-between;
  align-items: center;
  /* padding: 0px 8px 0px 0px; */
  padding: 8px;

  height: 56px;

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
