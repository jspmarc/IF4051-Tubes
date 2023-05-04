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
    ctaPrimary: {
      type: Function as PropType<() => void>,
      required: true,
    },
    ctaSecondary: {
      type: Function as PropType<() => void>,
      required: true,
    },
  },
  setup(props) {
    return {
      title: props.title,
      body: props.body,
      readMoreAction: props.ctaPrimary,
      dismissAction: props.ctaSecondary,
    };
  },
});
</script>

<template>
  <div
    class="flex flex-col lg:w-2/6 md:w-3/6 sm:w-4/6 w-full mx-auto min-w-[450px] px-8 py-3 bg-primary-bg rounded-3xl mb-6 items-start"
  >
    <p class="font-semibold text-xl">{{ title }}</p>
    <p class="text-base">{{ body }}</p>

    <div class="flex ml-auto gap-[10px] pt-2.5">
      <button
        class="bg-secondary-button text-primary-text"
        @click="dismissAction"
      >
        Dismiss
      </button>
      <button class="bg-active-button text-active-text" @click="readMoreAction">
        Read more
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
