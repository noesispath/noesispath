<template>
  <div class="min-h-screen bg-gray-950 text-gray-100 p-8">
    <div class="max-w-2xl mx-auto">
      <div class="mb-8">
        <h1 class="text-2xl font-bold text-white mb-1">NoesisPath</h1>
        <p class="text-sm text-gray-500">Your personalized DSA coach</p>
      </div>
      <!-- Today's Queue -->
      <div class="mb-8">
        <div class="text-xs tracking-widest text-gray-500 uppercase mb-4">
          Today's Review Queue
        </div>
        <div v-if="queue.length === 0"
          class="text-sm text-gray-600 border border-gray-800 rounded p-6 text-center">
          No reviews due today. Start a new question below.
        </div>
        <div v-for="item in queue" :key="item.id"
          class="flex items-center justify-between p-4 border border-gray-800 rounded mb-2 hover:border-gray-600 transition cursor-pointer"
          @click="$router.push(`/practice/${item.question_id}`)">
          <div>
            <div class="text-sm font-medium text-white">{{ item.question_title }}</div>
            <div class="text-xs text-gray-500 mt-1">{{ item.reason }} · due today</div>
          </div>
          <span class="text-xs text-gray-500">→</span>
        </div>
      </div>
      <!-- All Questions -->
      <div>
        <div class="text-xs tracking-widest text-gray-500 uppercase mb-4">
          All Questions
        </div>
        <div v-for="q in questions" :key="q.id"
          class="flex items-center justify-between p-4 border border-gray-800 rounded mb-2 hover:border-gray-600 transition cursor-pointer"
          @click="$router.push(`/practice/${q.id}`)">
          <div class="flex items-center gap-3">
            <span class="text-xs px-2 py-0.5 rounded border"
              :class="{
                'border-green-800 text-green-400': q.difficulty === 'easy',
                'border-yellow-800 text-yellow-400': q.difficulty === 'medium',
                'border-red-800 text-red-400': q.difficulty === 'hard',
              }">
              {{ q.difficulty }}
            </span>
            <span class="text-sm text-white">{{ q.title }}</span>
          </div>
          <span class="text-xs text-gray-600 border border-gray-800 px-2 py-0.5 rounded">
            {{ q.topic }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'

const questions = ref([])
const queue = ref([])

onMounted(async () => {
  const res = await api.get('/questions/')
  questions.value = res.data

  try {
    const qRes = await api.get('/review-queue/1')
    queue.value = qRes.data
  } catch {
    queue.value = []
  }
})
</script>
