<script setup lang="ts">
import { ref, watch } from "vue";
import { ChartData } from "chart.js";
import { Line } from "vue-chartjs";
import {
  getAverageAnnotation,
  getMaximumAnnotation,
  getMinimumAnnotation,
} from "../helpers/Chart";
import type RealtimeData from "../types/RealtimeData";

const props = defineProps<{
  data: RealtimeData[];
  dataLabel: string;
  mean?: number;
  min?: number;
  max?: number;
}>();

const labels: string[] = [];
const data: number[] = [];
props.data.forEach((datum) => {
  const { time } = datum;
  labels.push(time.format("DD-MM-YYYY HH:mm:ss"));
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

const averageAnnotation = getAverageAnnotation(props.mean);
watch(
  () => props.mean,
  (newState) => {
    const averageAnnotation =
      chartOptions.value.plugins.annotation.annotations.average;
    if (averageAnnotation && newState) {
      averageAnnotation.value = newState;
      chartOptions.value = { ...chartOptions.value };
    }
  }
);

const minAnnotation = getMinimumAnnotation(props.mean);
watch(
  () => props.min,
  (newState) => {
    const minAnnotation =
      chartOptions.value.plugins.annotation.annotations.minimum;
    if (minAnnotation && newState) {
      minAnnotation.value = newState;
      chartOptions.value = { ...chartOptions.value };
    }
  }
);

const maxAnnotation = getMaximumAnnotation(props.mean);
watch(
  () => props.max,
  (newState) => {
    const maxAnnotation =
      chartOptions.value.plugins.annotation.annotations.average;
    if (maxAnnotation && newState) {
      maxAnnotation.value = newState;
      chartOptions.value = { ...chartOptions.value };
    }
  }
);

const chartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    annotation: {
      annotations: {
        average: averageAnnotation,
        minimum: minAnnotation,
        maximum: maxAnnotation,
      },
    },
  },
});
</script>

<template>
  <div class="h-1/2 w-1/2">
    <Line :data="chartData" :options="chartOptions" />
  </div>
</template>
