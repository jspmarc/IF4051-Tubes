<script setup lang="ts">
import { ref } from "vue";
import { ChartData } from "chart.js";
import { Line } from "vue-chartjs";
import type RealtimeData from "../types/RealtimeData";

const props = defineProps<{
  data: RealtimeData[];
  dataLabel: string;
}>();

const labels: string[] = [];
const data: number[] = [];
props.data.forEach((datum) => {
  const { time } = datum;
  labels.push(
    `${time.date()}-${time.month() + 1}-${time.year()} ${time.hour()}.${time.minute()}.${time.second()}`
  );
  data.push(datum.value);
});

const chartData = ref<ChartData<"line">>({
  labels,
  datasets: [
    {
      label: props.dataLabel,
      data,
    },
  ],
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
};
</script>

<template>
  <div class="h-1/2 w-1/2">
    <Line :data="chartData" :options="chartOptions" />
  </div>
</template>
