<script setup lang="ts">
import { ref, defineProps } from "vue";
import { getPassword } from "../helpers/password";
import AlertCard from "./AlertCard.vue";

const props = defineProps<{
  beUrl: string;
}>();
const alerts = ref([]);

async function getData() {
  const password = getPassword();
  const xTokenHeader = password
    ? {
        "X-Token": password,
      }
    : null;
  const res = await fetch(`${props.beUrl}/alert?time_range=-1d`, {
    headers: { ...xTokenHeader },
  });
  const finalRes = await res.json();
  alerts.value = finalRes?.reverse();
}

getData();
</script>

<template>
  <div
    class="flex flex-col lg:w-2/6 md:w-3/6 sm:w-4/6 w-full mx-auto min-w-[550px] text-primary-text bg-primary-bg rounded-3xl p-4 gap-4"
  >
    <div v-show="alerts.length == 0" class="font-bold">No alerts</div>
    <AlertCard v-for="alert in alerts" :key="alert" :alert="alert" />
  </div>
</template>
