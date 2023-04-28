<script setup lang="ts">
import Selection from '../components/Selection.vue';

/**
 * HomeView component properties
 * @interface HomeViewProps
 * @member {string} [url] url to send request to, if not set: do nothing
 * @member {WebSocket} [wsConnection] websocket connection to listen to, if not set: do nothing
 */
interface HomeViewProps {
  url?: string,
  wsConnection?: WebSocket
}

const props = defineProps<HomeViewProps>();
</script>

<template>
  <div class="flex flex-col lg:w-2/6 md:w-3/6 sm:w-4/6 w-full mx-auto">
    <!-- Mode -->
    <Selection class="py-2" 
              label="Mode" 
              :optionsDisplay="['Auto', 'Override']" 
              :options="['Ai', 'Override']"
              :url="`${props.url}/mode`"
              :wsConnection="props.wsConnection"
              propertyName="current_mode" />
    <!-- Door - Servo -->
    <Selection class="py-2" 
              label="Door" 
              :optionsDisplay="['Open', 'Close']"
              :options="['2', '0']"
              :url="`${props.url}/servo`"
              :wsConnection="props.wsConnection"
              propertyName="servo_multiple" />
    <!-- Window - Servo -->
    <Selection class="py-2" 
              label="Window" 
              :optionsDisplay="['Open', 'Close']"
              :options="['2', '0']"
              :url="`${props.url}/servo`"
              :wsConnection="props.wsConnection"
              propertyName="servo_multiple" />
  </div>
</template>

<style scoped>
</style>