<script setup lang="ts">
import { ref, Ref } from "vue";
import dayjs from "dayjs";
import utc from "dayjs/plugin/utc";
import Chart from "./Chart.vue";
import type RawRealtimeData from "../types/RawRealtimeData";
import type RealtimeData from "../types/RealtimeData";
import AppState from "../types/AppState";

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

const rawRealtimeData: {
  humidity?: RawRealtimeData[];
  temperature?: RawRealtimeData[];
  co2?: RawRealtimeData[];
} = await (
  await fetch(
    "http://localhost:8080/realtime-data?time_range=-30m&data=temperature&data=co2"
  )
).json();

for (const key in rawRealtimeData) {
  if (key !== "humidity" && key !== "temperature" && key !== "co2") {
    continue;
  }

  const data = rawRealtimeData[key];
  if (!data) {
    continue;
  }

  realtimeData.value[key] = data.map((datum) => {
    const time = dayjs.utc(datum[0]).local();

    return {
      time,
      value: datum[1],
    };
  });
}
</script>

<template>
  <p>Temperature</p>
  <Chart
    v-if="realtimeData.temperature != null"
    :data="realtimeData.temperature"
    :mean="appState.dht22_statistics.temperature_avg"
    :min="appState.dht22_statistics.temperature_min"
    :max="appState.dht22_statistics.temperature_max"
    data-label="Temperature (in °C)"
  />

  <p>CO<sub>2</sub></p>
  <Chart
    v-if="realtimeData.co2 != null"
    :data="realtimeData.co2"
    :mean="appState.mq135_statistics.co2_avg"
    :min="appState.mq135_statistics.co2_min"
    :max="appState.mq135_statistics.co2_max"
    data-label="CO2 PPM"
  />
</template>
