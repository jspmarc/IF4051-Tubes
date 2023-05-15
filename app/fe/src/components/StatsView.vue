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
const timeRange = ref("30s");

const tmp = await getRealtimeData(props.beUrl, "all", timeRange.value);
realtimeData.value = { ...tmp };

async function updateTemperature(e: Event) {
  e.preventDefault();
  const tmp = await getRealtimeData(props.beUrl, "temp", timeRange.value);
  // bad performance but i am too tired :D
  if (realtimeData.value.co2) {
    tmp.co2 = [...realtimeData.value.co2];
  }
  realtimeData.value = { ...tmp };
}

async function updateCo2(e: Event) {
  e.preventDefault();
  const tmp = await getRealtimeData(props.beUrl, "co2", timeRange.value);
  // bad performance but i am too tired :D
  if (realtimeData.value.temperature) {
    tmp.temperature = [...realtimeData.value.temperature];
  }
  realtimeData.value = { ...tmp };
}

async function updateTimeRange(e: Event, newRange: string) {
  e.preventDefault();

  timeRange.value = newRange;
  const tmp = await getRealtimeData(props.beUrl, "all", newRange);
  realtimeData.value = { ...tmp };
}

type Interval = "1d" | "12h" | "6h" | "1h" | "30m" | "5m" | "1m" | "30s";
const currentInterval: Ref<Interval> = ref("30s");
const intervals: { label: string; value: Interval }[] = [
  { label: "30 seconds", value: "30s" },
  { label: "1 minute", value: "1m" },
  { label: "5 minutes", value: "5m" },
  { label: "30 minutes", value: "30m" },
  { label: "1 hour", value: "1h" },
  { label: "6 hours", value: "6h" },
  { label: "12 hours", value: "12h" },
  { label: "1 day", value: "1d" },
];
</script>

<template>
  <div
    class="flex flex-col rounded-3xl gap-4 items-center justify-center bg-primary-bg text-primary-text"
  >
    <div
      class="flex flex-col lg:flex-row h-screen lg:h-[30rem] items-center justify-center px-4 lg:px-10 w-full"
    >
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

    <ul
      class="selection gray-1 flex flex-row gap-x-8 p-2 mx-2 mb-2 rounded-2xl flex-wrap bg-gray-1 justify-around"
    >
      <li v-for="i in intervals" :key="i.label" class="rounded-full">
        <button
          class="px-3 py-1 rounded-full text-sm"
          @click="
            (ev) => {
              updateTimeRange(ev, i.value);
              currentInterval = i.value;
            }
          "
          :class="{ 'bg-black text-primary-bg': currentInterval === i.value }"
        >
          {{ i.label }} ago
        </button>
      </li>
    </ul>
  </div>
</template>
