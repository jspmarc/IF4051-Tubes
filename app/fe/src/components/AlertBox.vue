<script lang="ts">
import { defineComponent, defineEmits } from "vue";
import { getAlerts } from "../helpers/GetAlerts";
import dayjs from "dayjs";

export default defineComponent({
  emits: ["noAlerts"],
  props: {
    url: {
      type: String,
      required: true,
    },
    timeRange: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      alert: this.fetchAlert(),
    };
  },
  methods: {
    async fetchAlert() {
      const res = await getAlerts(this.url, this.timeRange);
      if (res.length == 0) {
        this.alert = {
          title: "",
          body: "No alerts (you should not be seeing this...)",
        };
        this.$emit("noAlerts");
      } else {
        const latestAlert = res[0];
        const regexp1 = /(.+\d{1,3}.\d{1,2}\S\.)(.+)/g;
        const regexp2 = /([\d-T:+]{25})/g;

        const newString: string = [
          ...latestAlert.alert_description.matchAll(regexp1),
        ][0][1];

        const newStringMatch = newString.match(regexp2);
        if (!newStringMatch || newStringMatch.length == 0) {
          this.$emit("noAlerts");
          return;
        }

        const date = new Date([...newStringMatch][0]);
        const newDate = dayjs(date).format("YYYY/MM/DD HH:mm:ss");
        this.alert = {
          title: [...latestAlert.alert_description.matchAll(regexp1)][0][2],
          body: newString.replace(regexp2, newDate),
        };
      }
    },
  },
});
</script>

<template>
  <div
    class="flex flex-col lg:w-2/6 md:w-3/6 sm:w-4/6 w-full mx-auto min-w-[550px] px-8 py-3 bg-yellow rounded-3xl mb-6 items-center"
  >
    <p class="font-semibold text-xl">{{ alert.title }}</p>
    <p class="text-base">{{ alert.body }}</p>

    <div class="flex gap-[10px] pt-2.5">
      <button
        class="bg-secondary-button text-primary-text"
        @click="$emit('noAlerts')"
      >
        Dismiss
      </button>
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
