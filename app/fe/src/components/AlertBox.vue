<script setup lang="ts">
import { defineProps, ref, Ref, defineEmits } from "vue";
import { getAlerts } from "../helpers/GetAlerts";
import dayjs from "dayjs";

const props = defineProps<{
  url: string;
  // ctaPrimary: () => void;
  ctaSecondary: () => void;
  // ctaPrimaryText: string;
}>();

const title: Ref<string> = ref("");
const body: Ref<string> = ref("");

const alertRes = await getAlerts(props.url, "30m");
const latestAlert = alertRes?.reverse()[0];
const emit = defineEmits<{
  (e: "noAlerts", val: string): void;
}>();

if (latestAlert) {
  const regexp1 = /([^\.].[^\.]+)+/g;
  const regexp2 = /([\d-T:+]{25})/g;
  const newString = [...latestAlert.alert_description.matchAll(regexp1)][0][0];
  const date = new Date([...newString.match(regexp2)][0]);
  const newDate = dayjs(date).format("YYYY/MM/DD HH:mm:ss");

  title.value = [...latestAlert.alert_description.matchAll(regexp1)][1][0];
  body.value = newString.replace(regexp2, newDate) + ".";
} else {
  title.value = "";
  body.value = "No alerts";
  emit("noAlerts", "No alerts");
}
</script>

<template>
  <div
    class="flex flex-col lg:w-2/6 md:w-3/6 sm:w-4/6 w-full mx-auto min-w-[550px] px-8 py-3 bg-yellow rounded-3xl mb-6 items-center"
  >
    <p class="font-semibold text-xl">{{ title }}</p>
    <p class="text-base">{{ body }}</p>

    <div class="flex gap-[10px] pt-2.5">
      <button
        class="bg-secondary-button text-primary-text"
        @click="ctaSecondary"
      >
        Dismiss
      </button>
      <!-- <button class="bg-active-button text-active-text" @click="ctaPrimary">
        {{ ctaPrimaryText }}
      </button> -->
    </div>
  </div>
</template>

<style scoped>
button {
  padding: 8px 24px;
  height: 32px;
  border-radius: 30px;
  font-weight: 600;
  font-size: 14px;
  line-height: 14px;
}
</style>
