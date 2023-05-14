<script lang="ts">
import { defineComponent, PropType } from "vue";

export default defineComponent({
  props: {
    title: {
      type: String as PropType<string>,
      required: true,
    },
    body: {
      type: String as PropType<string>,
      required: true,
    },
    temperature: {
      type: Number as PropType<number>,
      required: true,
    },
    ppm: {
      type: Number as PropType<number>,
      required: true,
    },
    ctaPrimary: {
      type: Function as PropType<() => void>,
      required: true,
    },
    ctaSecondary: {
      type: Function as PropType<() => void>,
      required: true,
    },
    ctaPrimaryText: {
      type: String as PropType<string>,
      required: true,
    },
  },
  setup(props) {
    return {
      title: props.title,
      body: props.body,
      temperature: props.temperature,
      ppm: props.ppm,
      toAlertView: props.ctaPrimary,
      dismissAction: props.ctaSecondary,
      ctaPrimaryText: props.ctaPrimaryText,
    };
  },
});
</script>

<template>
  <div
    class="flex flex-col lg:w-2/6 md:w-3/6 sm:w-4/6 w-full mx-auto min-w-[550px] px-8 py-3 bg-yellow rounded-3xl mb-6 items-center"
  >
    <p class="font-semibold text-xl">{{ title }}</p>
    <p class="text-base">{{ body }}</p>

    <div class="pt-2 flex flex-row">
      <p class="rounded-2xl bg-red px-2.5 h-8 leading-8">{{ temperature }}°C</p>
      <p class="rounded-2xl ml-2.5 bg-red px-2.5 h-8 leading-8">{{ ppm }}ppm</p>
    </div>

    <div class="flex gap-[10px] pt-2.5">
      <button
        class="bg-secondary-button text-primary-text"
        @click="dismissAction"
      >
        Dismiss
      </button>
      <button class="bg-active-button text-active-text" @click="toAlertView">
        {{ ctaPrimaryText }}
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
