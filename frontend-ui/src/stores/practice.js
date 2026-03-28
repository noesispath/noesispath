import { defineStore } from 'pinia'
import api from '../api'

export const usePracticeStore = defineStore('practice', {
  state: () => ({
    question: null,
    output: null,
    hint: null,
    hintLevel: 0,
    attempts: 0,
    startTime: null,
    loading: false,
    submitting: false,
  }),

  actions: {
    async loadQuestion(id) {
      this.loading = true
      this.output = null
      this.hint = null
      this.hintLevel = 0
      const res = await api.get(`/questions/${id}`)
      this.question = res.data
      this.startTime = Date.now()
      this.loading = false
    },

    async runCode(code) {
      const res = await api.post('/execute', {
        code,
        stdin: this.question.test_cases[0].input
      })
      this.output = res.data
    },

    async getHint(code) {
      if (this.hintLevel >= 3) return
      this.hintLevel++
      const res = await api.post('/hint', {
        question_title: this.question.title,
        question_description: this.question.description,
        user_code: code,
        hint_level: this.hintLevel,
        attempts_so_far: this.attempts
      })
      this.hint = res.data.hint
    },

    async submitCode(code) {
      this.submitting = true
      this.attempts++
      const timeTaken = Math.floor((Date.now() - this.startTime) / 1000)

      // Run against all test cases
      let passed = 0
      for (const tc of this.question.test_cases) {
        const res = await api.post('/execute', {
          code,
          stdin: tc.input
        })
        if (res.data.output?.trim() === tc.expected_output.trim()) {
          passed++
        }
      }

      const status = passed === this.question.test_cases.length
        ? 'passed'
        : passed > 0 ? 'partial' : 'failed'

      // Capture attempt
      await api.post('/attempts', {
        user_id: 1,
        question_id: this.question.id,
        code_submitted: code,
        time_taken: timeTaken,
        hints_used: this.hintLevel,
        hint_levels_used: this.hintLevel > 0
          ? Array.from({length: this.hintLevel}, (_, i) => i + 1)
          : [],
        test_cases_passed: passed,
        total_test_cases: this.question.test_cases.length,
        errors: this.output?.error || null,
        status
      })

      this.output = {
        ...this.output,
        status,
        test_cases_passed: passed,
        total: this.question.test_cases.length
      }
      this.submitting = false
    }
  }
})
