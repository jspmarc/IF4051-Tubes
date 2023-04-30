<script setup lang="ts">
import { ref, Ref } from "vue";
import dayjs from "dayjs";
import utc from "dayjs/plugin/utc";
import type RawRealtimeData from "../types/RawRealtimeData";
import type RealtimeData from "../types/RealtimeData";

dayjs.extend(utc);

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
  await fetch("http://localhost:8080/realtime-data?time_range=-30s")
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
    const time = dayjs.utc(datum[0]).local().toDate();

    return {
      time,
      value: datum[1],
    };
  });
}
</script>

<template>
  <h1>data</h1>
  <pre>{{ realtimeData }}</pre>
</template>
