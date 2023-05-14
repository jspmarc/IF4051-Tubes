<script lang="ts">
import dayjs from "dayjs";
import { defineComponent } from "vue";

export default defineComponent({
  props: {
    alert: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    return {
      alert: props.alert,
    };
  },
  methods: {
    formatDesc2(string: string) {
      const regexp = /([^\.].[^\.]+)+/g;
      return [...string.matchAll(regexp)][1][0];
    },
    formatDesc1(string: string) {
      const regexp1 = /([^\.].[^\.]+)+/g;
      const newString = [...string.matchAll(regexp1)][0][0];
      const regexp2 = /([\d-T:+]{25})/g;
      const regexp2Match = newString.match(regexp2);
      if (!regexp2Match)
        return;
      const date = new Date(regexp2Match[0]);
      const newDate = dayjs(date).format("YYYY/MM/DD HH:mm:ss");
      return newString.replace(regexp2, newDate) + ".";
    },
    formatTime(string: string) {
      return dayjs(string).format("HH:mm");
    },
  },
});
</script>

<template>
  <div
    class="flex flex-col w-full bg-gray-1 rounded-xl px-4 py-3 items-start text-left"
  >
    <div class="flex flex-row justify-between w-full">
      <div class="font-bold">
        {{ formatDesc2(alert.alert_description) }}
      </div>
      <div class="text-sm leading-6">{{ formatTime(alert.alert_time) }}</div>
    </div>
    <div class="text-sm text-gray-3">
      {{ formatDesc1(alert.alert_description) }}
    </div>
  </div>
</template>
