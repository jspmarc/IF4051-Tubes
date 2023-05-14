<script lang="ts">
import { defineComponent } from "vue";
import AlertCard from "./AlertCard.vue";
import { getAlerts } from "../helpers/GetAlerts";

export default defineComponent({
  components: {
    AlertCard,
  },
  props: {
    beUrl: {
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
      alerts: this.fetchAlerts(),
    };
  },
  methods: {
    async fetchAlerts() {
      const res = await getAlerts(this.beUrl, this.timeRange);
      this.alerts = res;
    },
  },
});
</script>

<template>
  <div
    class="flex flex-col lg:w-2/6 md:w-3/6 sm:w-4/6 w-full mx-auto min-w-[550px] text-primary-text bg-primary-bg rounded-3xl p-4 gap-4"
  >
    <div v-if="alerts.length == 0" class="font-bold">No alerts</div>
    <AlertCard v-for="alert in alerts" :key="alert" :alert="alert" />
  </div>
</template>
