<template>
  <div class="flex flex-col h-screen w-full bg-gray-950 text-gray-100">
    <!-- Unified Header Bar -->
    <div class="flex items-center justify-between px-4 py-3 border-b border-gray-800 bg-gray-900 w-full">
      <div class="flex items-center gap-4 min-w-0">
        <router-link to="/review"
          class="text-lg font-mono text-gray-500 hover:text-gray-300 tracking-widest uppercase whitespace-nowrap">
          ← Queue
        </router-link>
      </div>
      <div class="flex-1 flex justify-center">
        <span class="text-lg font-mono tracking-widest text-gray-500 uppercase">NoesisPath</span>
      </div>
      <div class="flex items-center gap-2 min-w-0">
        <span class="text-lg text-gray-500 font-mono mr-2">Python 3</span>
        <button
          class="px-6 py-1.5 text-sm bg-yellow-500 hover:bg-yellow-400 text-black rounded-full font-mono transition flex items-center gap-2"
          aria-label="Timer">
          <span aria-hidden="true" class="text-black">⏳</span>
          <span
            :class="{
              'text-gray-700': store.elapsedSeconds < (store.question?.expected_time ?? 0) * 60,
              'text-gray-900': store.elapsedSeconds >= (store.question?.expected_time ?? 0) * 60 && store.elapsedSeconds < (store.question?.expected_time ?? 0) * 120,
              'text-red-700': store.elapsedSeconds >= (store.question?.expected_time ?? 0) * 120,
            }"
            class="text-sm font-semibold">
            {{ store.formatTime(store.elapsedSeconds) }}
          </span>
        </button>
        <button @click="runCode"
          class="px-6 py-1.5 text-sm bg-gray-700 hover:bg-gray-600 rounded-full font-mono transition"
          aria-label="Run Code">
          <span class="mr-1" aria-hidden="true">&#9654;</span> <span class="hidden sm:inline">Run</span>
        </button>
        <button @click="getHint"
          :disabled="store.hintLevel >= 3"
          class="px-6 py-1.5 text-sm bg-blue-600 text-white hover:bg-blue-500 rounded-full font-mono transition disabled:opacity-30 disabled:cursor-not-allowed"
          aria-label="Get Hint">
          <span class="mr-1" aria-hidden="true">💡</span> <span class="hidden sm:inline">Hint {{ store.hintLevel }}/3</span>
        </button>
        <button @click="submitCode"
          :disabled="store.submitting"
          class="px-6 py-1.5 text-sm bg-green-700 hover:bg-green-600 rounded-full font-mono transition disabled:opacity-50"
          aria-label="Submit Code">
          <span class="mr-1" aria-hidden="true">&#10003;</span> <span class="hidden sm:inline">{{ store.submitting ? 'Checking...' : 'Submit' }}</span>
        </button>
      </div>
    </div>
    <div class="flex flex-1 h-full">
      <!-- Left Panel — Question / History -->
      <div class="w-2/5 min-w-0 flex flex-col border-r border-gray-800 overflow-y-auto text-base custom-scrollbar">
        <!-- Tab toggle -->
        <div class="flex border-b border-gray-800 shrink-0">
          <button
            v-for="tab in ['Problem', 'History']" :key="tab"
            @click="activeTab = tab"
            class="px-6 py-3 text-xs tracking-widest uppercase transition"
            :class="activeTab === tab
              ? 'text-white border-b border-white'
              : 'text-gray-600 hover:text-gray-400'">
            {{ tab }}
          </button>
        </div>

        <!-- Problem tab -->
        <div v-if="activeTab === 'Problem'">
          <div v-if="store.loading" class="p-6 text-gray-500 text-sm">Loading...</div>
          <div v-else-if="store.question" class="w-full p-6 flex flex-col gap-6">
            <div class="flex items-center gap-3 mb-3 w-full">
              <span class="text-base px-3 py-1 rounded-full border font-semibold"
                :class="{
                  'border-green-800 text-green-400': store.question.difficulty === 'easy',
                  'border-yellow-800 text-yellow-400': store.question.difficulty === 'medium',
                  'border-red-800 text-red-400': store.question.difficulty === 'hard',
                }">
                {{ store.question.difficulty }}
              </span>
              <span class="text-base text-gray-500 border border-gray-700 px-3 py-1 rounded-full font-semibold">
                {{ store.question.topic }}
              </span>
            </div>
            <h1 class="w-full text-2xl font-bold text-white mb-1.5">{{ store.question.title }}</h1>
            <p class="w-full text-base text-gray-300 leading-relaxed whitespace-normal break-words">
              {{ store.question.description }}
            </p>

            <!-- Examples -->
            <div v-if="store.question.examples && store.question.examples.length" class="flex flex-col gap-3">
              <div class="text-xs tracking-widest text-gray-500 uppercase">Examples</div>
              <div v-for="(ex, i) in store.question.examples" :key="i"
                class="rounded border border-gray-800 bg-gray-900 p-3">
                <div class="text-xs text-gray-500 mb-2">Example {{ i + 1 }}</div>
                <div class="font-mono text-xs text-gray-300">
                  <div><span class="text-gray-500">Input: </span>{{ ex.input }}</div>
                  <div><span class="text-gray-500">Output: </span>{{ ex.output }}</div>
                  <div v-if="ex.explanation">
                    <span class="text-gray-500">Explanation: </span>{{ ex.explanation }}
                  </div>
                </div>
              </div>
            </div>

            <!-- Constraints -->
            <div v-if="store.question.constraints && store.question.constraints.length" class="flex flex-col gap-2">
              <div class="text-xs tracking-widest text-gray-500 uppercase">Constraints</div>
              <ul class="flex flex-col gap-1">
                <li v-for="(c, i) in store.question.constraints" :key="i"
                  class="text-xs font-mono text-gray-400 flex items-start gap-2">
                  <span class="text-gray-600 mt-0.5">•</span>
                  <span>{{ c }}</span>
                </li>
              </ul>
            </div>

            <div v-if="store.question.follow_up" class="mt-2 text-xs text-blue-400 border border-blue-900 bg-blue-950 rounded px-3 py-2">
              💡 Follow up: {{ store.question.follow_up }}
            </div>

            <!-- Output -->
            <div v-if="store.output" class="w-full rounded border p-4"
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
              <div class="mt-2 flex gap-4 text-xs text-gray-500 font-mono">
                <span v-if="store.output.time !== undefined">⏱ {{ store.output.time }}s</span>
                <span v-if="store.output.memory !== undefined">🧠 {{ (store.output.memory / 1024).toFixed(0) }} KB</span>
              </div>
            </div>

            <!-- Feedback panel -->
            <div v-if="store.feedback && store.output?.status !== 'passed'"
              class="rounded border border-orange-800 bg-orange-950 p-4 flex flex-col gap-3">
              <div class="text-xs tracking-widest text-orange-400 uppercase">
                What Happened
              </div>
              <div>
                <div class="text-xs text-gray-500 mb-1">What went wrong</div>
                <p class="text-sm text-gray-200 leading-relaxed">
                  {{ store.feedback.what_went_wrong }}
                </p>
              </div>
              <div>
                <div class="text-xs text-gray-500 mb-1">Missing concept</div>
                <p class="text-sm text-gray-200 leading-relaxed">
                  {{ store.feedback.missing_concept }}
                </p>
              </div>
              <div>
                <div class="text-xs text-gray-500 mb-1">Key insight</div>
                <p class="text-sm text-gray-200 leading-relaxed">
                  {{ store.feedback.key_insight }}
                </p>
              </div>
            </div>

            <!-- Hint -->
            <div v-if="store.hint"
              class="w-full rounded border border-blue-800 bg-blue-950 p-4">
              <div class="text-xs text-blue-400 mb-2 tracking-widest uppercase">
                Hint Level {{ store.hintLevel }}
              </div>
              <p class="text-sm text-blue-200 leading-relaxed">{{ store.hint }}</p>
            </div>
          </div>
        </div>

        <!-- History tab -->
        <div v-if="activeTab === 'History'" class="p-6 flex flex-col gap-3">
          <div v-if="store.history.length === 0" class="text-sm text-gray-600">
            No submissions yet.
          </div>
          <div v-for="attempt in store.history" :key="attempt.id"
            class="border border-gray-800 rounded p-4">
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs text-gray-400">
                Attempt #{{ attempt.attempt_number }}
              </span>
              <span class="text-xs px-2 py-0.5 rounded border"
                :class="{
                  'border-green-800 text-green-400': attempt.status === 'passed',
                  'border-red-800 text-red-400': attempt.status === 'failed',
                  'border-yellow-800 text-yellow-400': attempt.status === 'partial',
                }">
                {{ attempt.status }}
              </span>
            </div>
            <div class="text-xs text-gray-600 mb-3">
              {{ Math.floor(attempt.time_taken / 60) }}m {{ attempt.time_taken % 60 }}s
              · {{ attempt.hints_used }} hints
              · {{ attempt.test_cases_passed }} tests passed
            </div>
            <details class="cursor-pointer">
              <summary class="text-xs text-gray-500 hover:text-gray-300">
                View code
              </summary>
              <pre class="mt-2 text-xs font-mono text-gray-400 bg-gray-900
                rounded p-3 overflow-x-auto whitespace-pre-wrap">{{
                attempt.code_submitted
              }}</pre>
            </details>
          </div>
        </div>
      </div>

      <!-- Right Panel — Editor -->
      <div class="w-3/5 min-w-0 flex flex-col">
        <!-- Monaco Editor -->
        <vue-monaco-editor
          v-model:value="code"
          @change="store.currentCode = code"
          language="python"
          theme="vs-dark"
          :options="{
            fontSize: 18,
            minimap: { enabled: false },
            scrollBeyondLastLine: false,
            fontFamily: 'JetBrains Mono, monospace',
            padding: { top: 16 },
          }"
          class="flex-1"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { usePracticeStore } from '../stores/practice'

const route = useRoute()
const store = usePracticeStore()
const code = ref('')
const activeTab = ref('Problem')

onMounted(async () => {
  await store.loadQuestion(route.params.id)
  code.value = store.question.starter_code || '# Write your solution here\n'
  store.currentCode = code.value
  if (store.currentUserId) {
    await store.loadHistory(store.currentUserId, route.params.id)
  }
})

function runCode() { store.runCode(code.value) }
function getHint() { store.getHint(code.value) }
function submitCode() { store.submitCode(code.value) }
</script>
