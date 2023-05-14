<script setup lang="ts">
import { ref, defineProps } from "vue";
import { getAlerts } from "../helpers/GetAlerts";
import AlertCard from "./AlertCard.vue";

const props = defineProps<{
  beUrl: string;
  timeRange: string;
}>();

const alerts = ref([]);

const alertRes = await getAlerts(props.beUrl, props.timeRange);
alerts.value = alertRes?.reverse() ?? [];
// console.log(alerts.value);
</script>

<template>
  <div
    class="flex flex-col lg:w-2/6 md:w-3/6 sm:w-4/6 w-full mx-auto min-w-[550px] text-primary-text bg-primary-bg rounded-3xl p-4 gap-4"
  >
    <div v-show="alerts.length == 0" class="font-bold">No alerts</div>
    <AlertCard v-for="alert in alerts" :key="alert" :alert="alert" />
  </div>
</template>
