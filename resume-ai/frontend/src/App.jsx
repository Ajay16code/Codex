import { useState } from 'react'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default function App() {
  const [resume, setResume] = useState(null)
  const [jobDescription, setJobDescription] = useState('')
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const onSubmit = async (event) => {
    event.preventDefault()
    if (!resume || !jobDescription.trim()) {
      setError('Please upload a PDF and enter a job description.')
      return
    }

    setLoading(true)
    setError('')
    setResult(null)

    const formData = new FormData()
    formData.append('resume', resume)
    formData.append('job_description', jobDescription)

    try {
      const response = await fetch(`${API_BASE_URL}/analyze`, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error('Analysis failed. Please verify backend is running.')
      }

      const payload = await response.json()
      setResult(payload)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="min-h-screen p-6 md:p-10">
      <section className="mx-auto max-w-4xl rounded-2xl bg-white p-8 shadow-lg">
        <h1 className="text-2xl font-bold text-slate-800">AI Candidate Intelligence Engine</h1>
        <p className="mt-2 text-sm text-slate-500">Upload a candidate resume and evaluate fit against a job description.</p>

        <form className="mt-6 space-y-4" onSubmit={onSubmit}>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Resume PDF</label>
            <input
              type="file"
              accept="application/pdf"
              onChange={(e) => setResume(e.target.files?.[0] ?? null)}
              className="w-full rounded-lg border border-slate-300 p-2"
            />
          </div>

          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Job Description</label>
            <textarea
              rows={7}
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              className="w-full rounded-lg border border-slate-300 p-3"
              placeholder="Paste job description..."
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="rounded-lg bg-indigo-600 px-4 py-2 font-medium text-white hover:bg-indigo-500 disabled:opacity-50"
          >
            {loading ? 'Analyzing...' : 'Analyze Candidate'}
          </button>
        </form>

        {error && <p className="mt-4 rounded-lg bg-red-50 p-3 text-sm text-red-600">{error}</p>}

        {result && (
          <div className="mt-6 grid gap-3 rounded-xl bg-slate-50 p-4 text-sm text-slate-700">
            <p><span className="font-semibold">Prediction:</span> {result.prediction}</p>
            <p><span className="font-semibold">Confidence:</span> {(result.confidence_score * 100).toFixed(2)}%</p>
            <p><span className="font-semibold">Similarity Score:</span> {result.similarity_score.toFixed(4)}</p>
          </div>
        )}
      </section>
    </main>
  )
}
