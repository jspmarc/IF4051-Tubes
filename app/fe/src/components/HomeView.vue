<script setup lang="ts">
import { onMounted } from 'vue';
import Selection from '../components/Selection.vue';

const beUrn = import.meta.env.VITE_BACKEND_URN;
const httpBeUrl = `http://${beUrn}`;
const wsBeUrl = `ws://${beUrn}`;
</script>

<template>
  <div class="flex flex-col lg:w-2/6 md:w-3/6 sm:w-4/6 w-full mx-auto">
    <!-- Mode -->
    <Selection class="py-2" 
              label="Mode" 
              :optionsDisplay="['Auto', 'Override']" 
              :options="['Ai', 'Override']"
              :url="`${httpBeUrl}/mode`"
              :wsUrl="`${wsBeUrl}/state/ws`"
              propertyName="current_mode" />
    <!-- Door - Servo -->
    <Selection class="py-2" 
              label="Door" 
              :optionsDisplay="['Open', 'Close']"
              :options="['2', '0']"
              :url="`${httpBeUrl}/servo`"
              :wsUrl="`${wsBeUrl}/state/ws`"
              propertyName="servo_multiple" />
    <!-- Window - Servo -->
    <Selection class="py-2" 
              label="Window" 
              :optionsDisplay="['Open', 'Close']"
              :options="['2', '0']"
              :url="`${httpBeUrl}/servo`"
              :wsUrl="`${wsBeUrl}/state/ws`"
              propertyName="servo_multiple" />
  </div>
</template>

<style scoped>
</style>