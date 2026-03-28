<template>
  <div class="flex h-screen bg-gray-950 text-gray-100">
    <!-- Left Panel — Question -->
    <div class="w-2/5 flex flex-col border-r border-gray-800 overflow-y-auto">
      <!-- Header -->
      <div class="flex items-center justify-between px-6 py-4 border-b border-gray-800">
        <router-link to="/review"
          class="text-xs text-gray-500 hover:text-gray-300 tracking-widest uppercase">
          ← Queue
        </router-link>
        <span class="text-xs tracking-widest text-gray-500 uppercase">NoesisPath</span>
      </div>
      <!-- Question -->
      <div v-if="store.loading" class="p-6 text-gray-500 text-sm">Loading...</div>
      <div v-else-if="store.question" class="p-6 flex flex-col gap-6">
        <div>
          <div class="flex items-center gap-3 mb-3">
            <span class="text-xs px-2 py-1 rounded border"
              :class="{
                'border-green-800 text-green-400': store.question.difficulty === 'easy',
                'border-yellow-800 text-yellow-400': store.question.difficulty === 'medium',
                'border-red-800 text-red-400': store.question.difficulty === 'hard',
              }">
              {{ store.question.difficulty }}
            </span>
            <span class="text-xs text-gray-500 border border-gray-700 px-2 py-1 rounded">
              {{ store.question.topic }}
            </span>
          </div>
          <h1 class="text-xl font-bold text-white mb-4">{{ store.question.title }}</h1>
          <p class="text-sm text-gray-300 leading-relaxed whitespace-pre-line">
            {{ store.question.description }}
          </p>
        </div>
        <!-- Output -->
        <div v-if="store.output" class="rounded border p-4"
          :class="{
            'border-green-800 bg-green-950': store.output.status === 'passed',
            'border-red-800 bg-red-950': store.output.status === 'failed',
            'border-yellow-800 bg-yellow-950': store.output.status === 'partial',
            'border-gray-700 bg-gray-900': !store.output.status,
          }">
          <div class="text-xs font-mono text-gray-400 mb-2">Output</div>
          <pre class="text-sm font-mono text-gray-200 whitespace-pre-wrap">{{
            store.output.output || store.output.error
          }}</pre>
          <div v-if="store.output.test_cases_passed !== undefined"
            class="mt-3 text-xs text-gray-400">
            {{ store.output.test_cases_passed }}/{{ store.output.total }} test cases passed
          </div>
        </div>
        <!-- Hint -->
        <div v-if="store.hint"
          class="rounded border border-blue-800 bg-blue-950 p-4">
          <div class="text-xs text-blue-400 mb-2 tracking-widest uppercase">
            Hint Level {{ store.hintLevel }}
          </div>
          <p class="text-sm text-blue-200 leading-relaxed">{{ store.hint }}</p>
        </div>
      </div>
    </div>
    <!-- Right Panel — Editor -->
    <div class="flex-1 flex flex-col">
      <!-- Toolbar -->
      <div class="flex items-center justify-between px-4 py-3 border-b border-gray-800 bg-gray-900">
        <span class="text-xs text-gray-500 font-mono">Python 3</span>
        <div class="flex gap-2">
          <button @click="runCode"
            class="px-4 py-1.5 text-xs bg-gray-700 hover:bg-gray-600 rounded font-mono transition">
            ▶ Run
          </button>
          <button @click="getHint"
            :disabled="store.hintLevel >= 3"
            class="px-4 py-1.5 text-xs border border-blue-700 text-blue-400 hover:bg-blue-900 rounded font-mono transition disabled:opacity-30 disabled:cursor-not-allowed">
            Hint {{ store.hintLevel }}/3
          </button>
          <button @click="submitCode"
            :disabled="store.submitting"
            class="px-4 py-1.5 text-xs bg-green-700 hover:bg-green-600 rounded font-mono transition disabled:opacity-50">
            {{ store.submitting ? 'Checking...' : 'Submit' }}
          </button>
        </div>
      </div>
      <!-- Monaco Editor -->
      <vue-monaco-editor
        v-model:value="code"
        language="python"
        theme="vs-dark"
        :options="{
          fontSize: 14,
          minimap: { enabled: false },
          scrollBeyondLastLine: false,
          fontFamily: 'JetBrains Mono, monospace',
          padding: { top: 16 },
        }"
        class="flex-1"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { usePracticeStore } from '../stores/practice'

const route = useRoute()
const store = usePracticeStore()
const code = ref('# Write your solution here\n\n')

onMounted(() => {
  store.loadQuestion(route.params.id)
})

function runCode() { store.runCode(code.value) }
function getHint() { store.getHint(code.value) }
function submitCode() { store.submitCode(code.value) }
</script>
