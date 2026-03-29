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
    feedback: null,
    history: [],
    elapsedSeconds: 0,
    timerInterval: null,
    codeSnapshots: [],
    snapshotInterval: null,
    currentCode: '',
    currentUserId: null,
  }),

  actions: {
    startTimer() {
      this.elapsedSeconds = 0
      this.timerInterval = setInterval(() => {
        this.elapsedSeconds++
      }, 1000)
    },

    stopTimer() {
      clearInterval(this.timerInterval)
    },

    formatTime(seconds) {
      const m = Math.floor(seconds / 60)
      const s = seconds % 60
      return `${m}:${s.toString().padStart(2, '0')}`
    },

    startSnapshots() {
      this.codeSnapshots = []
      this.snapshotInterval = setInterval(() => {
        if (this.currentCode) {
          this.codeSnapshots.push({
            timestamp: Math.floor((Date.now() - this.startTime) / 1000),
            code: this.currentCode
          })
        }
      }, 30000)
    },

    stopSnapshots() {
      clearInterval(this.snapshotInterval)
    },

    async loadQuestion(id) {
      this.loading = true
      this.output = null
      this.hint = null
      this.hintLevel = 0
      this.feedback = null

      if (!this.currentUserId) {
        const usersRes = await api.get('/users?limit=1')
        const firstUser = usersRes.data[0]
        if (firstUser) {
          this.currentUserId = firstUser.id
        } else {
          const randomSuffix = Date.now()
          const newUserRes = await api.post('/users', {
            name: `User ${randomSuffix}`,
            email: `user+${randomSuffix}@temp.local`
          })
          this.currentUserId = newUserRes.data.id
        }
      }

      const res = await api.get(`/questions/${id}`)
      this.question = res.data
      this.startTime = Date.now()
      this.loading = false
      this.startTimer()
      this.startSnapshots()
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
      try {
        this.attempts++
        this.stopTimer()
        this.stopSnapshots()

        // Run against all test cases
        let passed = 0
        for (const tc of this.question.test_cases) {
          const res = await api.post('/execute', {
            code,
            stdin: tc.input
          })

          const actual = (res.data.output || '').trim().toLowerCase()
          const expected = (tc.expected_output || '').trim().toLowerCase()

          if (actual === expected) {
            passed++
          }
        }

        const status = passed === this.question.test_cases.length
          ? 'passed'
          : passed > 0 ? 'partial' : 'failed'

        // Capture attempt
        const attemptRes = await api.post('/attempts', {
          user_id: this.currentUserId,
          question_id: this.question.id,
          code_submitted: code,
          time_taken: this.elapsedSeconds,
          hints_used: this.hintLevel,
          hint_levels_used: this.hintLevel > 0
            ? Array.from({length: this.hintLevel}, (_, i) => i + 1)
            : [],
          test_cases_passed: passed,
          total_test_cases: this.question.test_cases.length,
          errors: this.output?.error || null,
          status,
          code_snapshots: this.codeSnapshots
        })

        this.output = {
          ...this.output,
          status,
          test_cases_passed: passed,
          total: this.question.test_cases.length
        }

        // Keep history tab in sync after each submission.
        await this.loadHistory(this.currentUserId, this.question.id)

        if (status !== 'passed') {
          try {
            await this.getSubmissionFeedback(attemptRes.data.id)
          } catch (error) {
            this.feedback = null
          }
        }
      } finally {
        this.submitting = false
      }
    },

    async getSubmissionFeedback(attemptId) {
      const res = await api.post(`/attempts/${attemptId}/feedback`)
      this.feedback = res.data
    },

    async loadHistory(userId, questionId) {
      const res = await api.get(`/attempts/history/${userId}/${questionId}`)
      this.history = res.data
    }
  }
})
