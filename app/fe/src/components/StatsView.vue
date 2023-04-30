<script setup lang="ts">
import { defineProps, ref, Ref } from "vue";
import dayjs from "dayjs";
import utc from "dayjs/plugin/utc";
import Chart from "./Chart.vue";
import type RealtimeData from "../types/RealtimeData";
import AppState from "../types/AppState";
import { getRealtimeData } from "../helpers/StatsView";

dayjs.extend(utc);

const props = defineProps<{
  appState: AppState;
  beUrl: string;
}>();

const realtimeData: Ref<{
  humidity?: RealtimeData[];
  temperature?: RealtimeData[];
  co2?: RealtimeData[];
}> = ref({});

const tmp = await getRealtimeData(props.beUrl, "all");
realtimeData.value = { ...tmp };

async function updateTemperature(e: Event) {
  e.preventDefault();
  const tmp = await getRealtimeData(props.beUrl, "temp");
  // bad performance but i am too tired :D
  if (realtimeData.value.co2) {
    tmp.co2 = [...realtimeData.value.co2];
  }
  realtimeData.value = { ...tmp };
}

async function updateCo2(e: Event) {
  e.preventDefault();
  const tmp = await getRealtimeData(props.beUrl, "co2");
  // bad performance but i am too tired :D
  if (realtimeData.value.temperature) {
    tmp.temperature = [...realtimeData.value.temperature];
  }
  realtimeData.value = { ...tmp };
}
</script>

<template>
  <div class="flex flex-col lg:flex-row h-screen lg:h-[30rem] items-center justify-center px-4 lg:px-10 w-full">
    <div class="flex flex-col items-center justify-center h-full w-full">
      <p>Temperature</p>
      <Chart
        v-if="realtimeData.temperature != null"
        :data="realtimeData.temperature"
        :mean="appState.dht22_statistics.temperature_avg"
        :min="appState.dht22_statistics.temperature_min"
        :max="appState.dht22_statistics.temperature_max"
        data-label="Temperature (in °C)"
      />
      <button @click="updateTemperature">Update data</button>
    </div>

    <div class="flex flex-col items-center justify-center h-full w-full">
      <p>CO<sub>2</sub></p>
      <Chart
        v-if="realtimeData.co2 != null"
        :data="realtimeData.co2"
        :mean="appState.mq135_statistics.co2_avg"
        :min="appState.mq135_statistics.co2_min"
        :max="appState.mq135_statistics.co2_max"
        data-label="CO2 PPM"
      />
      <button @click="updateCo2">Update data</button>
    </div>
  </div>
</template>
