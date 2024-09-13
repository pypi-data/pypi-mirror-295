<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="bg-white shadow-lg rounded-lg p-8 max-w-md w-full">
      <h1 class="text-xl font-bold text-red-600 mb-4">
        {{ context.error_message }}
      </h1>

      <p class="text-gray-500 text-sm mb-4">{{ context.instructions }}</p>

      <div className="bg-gray-100 p-4 rounded-md mb-4">
        <code className="text-sm font-mono text-gray-800"
          >python manage.py init</code
        >
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    context: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style scoped>
/* Add any component-specific styles here */
</style>
