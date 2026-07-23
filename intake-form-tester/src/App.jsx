import { useState } from 'react'
import axios from 'axios'
import './App.css'

const DEFAULT_BASE_URL = 'http://127.0.0.1:8000'

const SAMPLE_VALUES = {
  patient_info: {
    first_name: 'John',
    last_name: 'Doe',
    email: 'john.doe@example.com',
    phone_number: '5551112233',
  },
  family_history: {
    diabetes: 'YES',
  },
  insurance: [
    {
      insurance_type: 'RX',
      primary_insured: true,
      insurance_carrier: 'Test Carrier',
    },
  ],
}

function normalizeSectionTitle(sectionId, title) {
  if (title) {
    return title
  }

  return sectionId
    .split('_')
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

function getValueByPath(values, path) {
  if (!path || typeof path !== 'string') {
    return undefined
  }

  return path.split('.').reduce((acc, segment) => {
    if (acc === null || acc === undefined) {
      return undefined
    }

    return acc[segment]
  }, values)
}

function isFieldVisible(showWhen, contextValues, rootValues = contextValues) {
  if (!showWhen) {
    return true
  }

  return Object.entries(showWhen).every(([key, values]) => {
    if (!Array.isArray(values) || values.length === 0) {
      return true
    }

    const currentValue = key.includes('.')
      ? getValueByPath(rootValues, key)
      : contextValues?.[key] ?? getValueByPath(rootValues, key)

    return values.includes(currentValue)
  })
}

function toInitialFormData(schema) {
  const initial = JSON.parse(JSON.stringify(SAMPLE_VALUES))

  ;(schema?.sections || []).forEach((section) => {
    if (Array.isArray(section.groups)) {
      section.groups.forEach((group) => {
        ;(group.fields || []).forEach((field) => {
          if (!Object.prototype.hasOwnProperty.call(initial, field.name)) {
            initial[field.name] = field.component === 'checkbox' ? false : ''
          }
        })
      })
      return
    }

    if (section.repeatable) {
      if (!Array.isArray(initial[section.id])) {
        initial[section.id] = []
      }
      return
    }

    if (!initial[section.id] || typeof initial[section.id] !== 'object') {
      initial[section.id] = {}
    }

    ;(section.fields || []).forEach((field) => {
      if (!Object.prototype.hasOwnProperty.call(initial[section.id], field.name)) {
        initial[section.id][field.name] = field.component === 'checkbox' ? false : ''
      }
    })
  })

  return initial
}

function buildSubmissionPayload(schema, formData) {
  const payload = {}

  ;(schema?.sections || []).forEach((section) => {
    if (section.id === 'conditions' || section.id === 'condition_requests') {
      return
    }

    if (section.repeatable) {
      const sectionRows = Array.isArray(formData[section.id]) ? formData[section.id] : []
      payload[section.id] = sectionRows
      return
    }

    payload[section.id] = formData[section.id] || {}
  })

  const conditionAnswers = []
  const requestedMap = formData.condition_requests || {}

  ;(schema?.sections || []).forEach((section) => {
    if (!Array.isArray(section.groups)) {
      return
    }

    section.groups.forEach((group) => {
      const key = `condition_${group.conditionId}_requested`
      if (requestedMap[key] !== 'YES') {
        return
      }

      ;(group.fields || []).forEach((field) => {
        const answerValue = formData[field.name]
        const answer = { question_id: field.questionId }

        if (field.questionType === 'TEXT') {
          answer.text_answer = answerValue || ''
        } else if (field.questionType === 'NUMBER') {
          answer.number_answer = answerValue === '' ? null : Number(answerValue)
        } else if (field.questionType === 'YES_NO') {
          answer.boolean_answer = answerValue === '' ? null : answerValue === 'YES'
        } else if (field.questionType === 'DATE') {
          answer.date_answer = answerValue || null
        } else if (Array.isArray(answerValue)) {
          answer.selected_choice_ids = answerValue
        } else if (answerValue !== '' && answerValue !== null && answerValue !== undefined) {
          answer.selected_choice_ids = [answerValue]
        }

        conditionAnswers.push(answer)
      })
    })
  })

  payload.condition_answers = conditionAnswers
  payload.condition_requests = requestedMap

  return payload
}

function InputField({ field, value, onChange }) {
  const commonClassName = 'mt-2 w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 shadow-sm outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-200'

  if (field.component === 'textarea') {
    return (
      <textarea
        className={commonClassName}
        rows={3}
        value={value ?? ''}
        onChange={(event) => onChange(event.target.value)}
      />
    )
  }

  if (field.component === 'select') {
    return (
      <select className={commonClassName} value={value ?? ''} onChange={(event) => onChange(event.target.value)}>
        <option value="">Select...</option>
        {(field.options || []).map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    )
  }

  if (field.component === 'checkbox') {
    return (
      <label className="mt-2 flex items-center gap-2 text-sm font-medium text-slate-700">
        <input
          type="checkbox"
          checked={Boolean(value)}
          onChange={(event) => onChange(event.target.checked)}
          className="h-4 w-4 rounded border-slate-300 text-sky-600 focus:ring-sky-300"
        />
        <span>Yes</span>
      </label>
    )
  }

  if (field.component === 'radio') {
    return (
      <div className="mt-2 flex flex-wrap gap-3">
        {(field.options || []).map((option) => (
          <label
            key={option.value}
            className="inline-flex cursor-pointer items-center gap-2 rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm font-medium text-slate-700 hover:border-sky-400"
          >
            <input
              type="radio"
              name={field.name}
              value={option.value}
              checked={value === option.value}
              onChange={(event) => onChange(event.target.value)}
              className="h-4 w-4 border-slate-300 text-sky-600 focus:ring-sky-300"
            />
            {option.label}
          </label>
        ))}
      </div>
    )
  }

  if (field.component === 'date') {
    return <input type="date" className={commonClassName} value={value ?? ''} onChange={(event) => onChange(event.target.value)} />
  }

  return (
    <input
      type={field.component === 'number' ? 'number' : field.component === 'email' ? 'email' : field.component === 'tel' ? 'tel' : 'text'}
      className={commonClassName}
      value={value ?? ''}
      onChange={(event) => onChange(event.target.value)}
    />
  )
}

function App() {
  const [baseUrl, setBaseUrl] = useState(DEFAULT_BASE_URL)
  const [token, setToken] = useState('')
  const [schema, setSchema] = useState(null)
  const [formData, setFormData] = useState({})
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [submittedData, setSubmittedData] = useState(null)

  async function loadSchema() {
    setLoading(true)
    setError('')

    try {
      const cleanBaseUrl = baseUrl.replace(/\/$/, '')
      const response = await axios.get(`${cleanBaseUrl}/api/intake/form/`, {
        headers: token
          ? {
              Authorization: `Bearer ${token}`,
            }
          : {},
      })

      setSchema(response.data)
      setFormData(toInitialFormData(response.data))
      setSubmittedData(null)
    } catch (err) {
      setSchema(null)
      setFormData({})
      const detail = err?.response?.data?.detail
      setError(detail || err.message || 'Could not load form schema.')
    } finally {
      setLoading(false)
    }
  }

  function updateSectionField(sectionId, fieldName, value) {
    setFormData((prev) => ({
      ...prev,
      [sectionId]: {
        ...(prev[sectionId] || {}),
        [fieldName]: value,
      },
    }))
  }

  function updateRootField(fieldName, value) {
    setFormData((prev) => ({
      ...prev,
      [fieldName]: value,
    }))
  }

  function addRepeatableRow(section) {
    const emptyRow = {}
    ;(section.fields || []).forEach((field) => {
      emptyRow[field.name] = field.component === 'checkbox' ? false : ''
    })

    setFormData((prev) => ({
      ...prev,
      [section.id]: [...(prev[section.id] || []), emptyRow],
    }))
  }

  function updateRepeatableField(sectionId, index, fieldName, value) {
    setFormData((prev) => {
      const rows = [...(prev[sectionId] || [])]
      rows[index] = {
        ...(rows[index] || {}),
        [fieldName]: value,
      }
      return {
        ...prev,
        [sectionId]: rows,
      }
    })
  }

  function removeRepeatableRow(sectionId, index) {
    setFormData((prev) => {
      const rows = [...(prev[sectionId] || [])]
      rows.splice(index, 1)
      return {
        ...prev,
        [sectionId]: rows,
      }
    })
  }

  function handleSubmit(event) {
    event.preventDefault()
    if (!schema) {
      return
    }

    const payload = buildSubmissionPayload(schema, formData)
    setSubmittedData(payload)
    console.log('Submitted payload:', payload)
  }

  return (
    <main className="mx-auto min-h-screen w-full max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
      <div className="mb-6 rounded-2xl border border-slate-200 bg-white/90 p-6 shadow-sm backdrop-blur">
        <h1 className="text-3xl font-bold tracking-tight text-slate-900">Intake Form Tester</h1>
        <p className="mt-2 text-sm text-slate-600">
          Schema-driven intake form with conditional fields, repeatable sections, and structured card layout.
        </p>
      </div>

      <section className="mb-6 rounded-2xl border border-slate-200 bg-white/90 p-6 shadow-sm backdrop-blur">
        <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
          <label className="text-sm font-semibold text-slate-700">
            Django Base URL
          <input
            type="text"
            className="mt-2 w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 shadow-sm outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-200"
            value={baseUrl}
            onChange={(event) => setBaseUrl(event.target.value)}
            placeholder="http://127.0.0.1:8000"
          />
        </label>

          <label className="text-sm font-semibold text-slate-700">
          JWT Access Token
          <textarea
            className="mt-2 w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 shadow-sm outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-200"
            value={token}
            onChange={(event) => setToken(event.target.value)}
            rows={3}
            placeholder="Paste access token for /api/intake/form/"
          />
        </label>
        </div>

        <button
          type="button"
          onClick={loadSchema}
          disabled={loading}
          className="mt-4 inline-flex items-center rounded-xl bg-sky-600 px-4 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-sky-700 disabled:cursor-not-allowed disabled:bg-sky-400"
        >
          {loading ? 'Loading schema...' : 'Load Form Schema'}
        </button>

        {error ? <p className="mt-3 text-sm font-medium text-rose-600">{error}</p> : null}
      </section>

      {schema ? (
        <form onSubmit={handleSubmit} className="space-y-6">
          {(schema.sections || []).map((section) => {
            if (Array.isArray(section.groups)) {
              return (
                <section key={section.id} className="rounded-2xl border border-slate-200 bg-white/90 p-6 shadow-sm backdrop-blur">
                  <h2 className="text-xl font-semibold text-slate-900">{normalizeSectionTitle(section.id, section.title)}</h2>
                  <div className="mt-4 space-y-4">
                    {section.groups.map((group) => {
                      const groupVisible = isFieldVisible(group.showWhen, formData, formData)
                      if (!groupVisible) {
                        return null
                      }

                      return (
                        <article key={group.id} className="rounded-xl border border-slate-200 bg-slate-50 p-4">
                          <h3 className="text-base font-semibold text-slate-800">{group.title}</h3>
                          <div className="mt-3 grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
                            {(group.fields || []).map((field) => {
                              if (!isFieldVisible(field.showWhen, formData, formData)) {
                                return null
                              }

                              return (
                                <div key={field.name} className="rounded-lg bg-white p-3 shadow-sm ring-1 ring-slate-100">
                                  <label className="text-sm font-medium text-slate-700">
                                    {field.label}
                                    {field.required ? ' *' : ''}
                                  </label>
                                  <InputField
                                    field={field}
                                    value={formData[field.name]}
                                    onChange={(value) => updateRootField(field.name, value)}
                                  />
                                </div>
                              )
                            })}
                          </div>
                        </article>
                      )
                    })}
                  </div>
                </section>
              )
            }

            if (section.repeatable) {
              const rows = Array.isArray(formData[section.id]) ? formData[section.id] : []
              return (
                <section key={section.id} className="rounded-2xl border border-slate-200 bg-white/90 p-6 shadow-sm backdrop-blur">
                  <div className="flex flex-wrap items-center justify-between gap-3">
                    <h2 className="text-xl font-semibold text-slate-900">{normalizeSectionTitle(section.id, section.title)}</h2>
                    <button
                      type="button"
                      onClick={() => addRepeatableRow(section)}
                      className="inline-flex items-center rounded-xl bg-emerald-600 px-3 py-2 text-sm font-semibold text-white hover:bg-emerald-700"
                    >
                      Add Row
                    </button>
                  </div>

                  <div className="mt-4 space-y-4">
                    {rows.length === 0 ? <p className="text-sm text-slate-500">No entries yet. Click Add Row.</p> : null}
                    {rows.map((row, rowIndex) => (
                      <article key={`${section.id}-${rowIndex}`} className="rounded-xl border border-slate-200 bg-slate-50 p-4">
                        <div className="mb-3 flex items-center justify-between">
                          <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-600">{section.title} #{rowIndex + 1}</h3>
                          <button
                            type="button"
                            onClick={() => removeRepeatableRow(section.id, rowIndex)}
                            className="rounded-lg bg-rose-100 px-3 py-1 text-xs font-semibold text-rose-700 hover:bg-rose-200"
                          >
                            Remove
                          </button>
                        </div>

                        <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
                          {(section.fields || []).map((field) => {
                            if (!isFieldVisible(field.showWhen, row, formData)) {
                              return null
                            }

                            return (
                              <div key={`${section.id}-${rowIndex}-${field.name}`} className="rounded-lg bg-white p-3 shadow-sm ring-1 ring-slate-100">
                                <label className="text-sm font-medium text-slate-700">
                                  {field.label}
                                  {field.required ? ' *' : ''}
                                </label>
                                <InputField
                                  field={field}
                                  value={row[field.name]}
                                  onChange={(value) => updateRepeatableField(section.id, rowIndex, field.name, value)}
                                />
                              </div>
                            )
                          })}
                        </div>
                      </article>
                    ))}
                  </div>
                </section>
              )
            }

            const sectionData = formData[section.id] || {}
            return (
              <section key={section.id} className="rounded-2xl border border-slate-200 bg-white/90 p-6 shadow-sm backdrop-blur">
                <h2 className="text-xl font-semibold text-slate-900">{normalizeSectionTitle(section.id, section.title)}</h2>
                <div className="mt-4 grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
                  {(section.fields || []).map((field) => {
                    if (!isFieldVisible(field.showWhen, sectionData, formData)) {
                      return null
                    }

                    return (
                      <div key={`${section.id}-${field.name}`} className="rounded-lg bg-slate-50 p-3 shadow-sm ring-1 ring-slate-100">
                        <label className="text-sm font-medium text-slate-700">
                          {field.label}
                          {field.required ? ' *' : ''}
                        </label>
                        <InputField
                          field={field}
                          value={sectionData[field.name]}
                          onChange={(value) => updateSectionField(section.id, field.name, value)}
                        />
                      </div>
                    )
                  })}
                </div>
              </section>
            )
          })}

          <div className="flex flex-wrap gap-3">
            <button
              type="submit"
              className="inline-flex items-center rounded-xl bg-indigo-600 px-5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-700"
            >
              Submit (Preview Payload)
            </button>
            <button
              type="button"
              onClick={() => setSubmittedData(null)}
              className="inline-flex items-center rounded-xl bg-slate-200 px-5 py-2.5 text-sm font-semibold text-slate-700 hover:bg-slate-300"
            >
              Clear Output
            </button>
          </div>
        </form>
      ) : null}

      {submittedData ? (
        <section className="mt-6 rounded-2xl border border-slate-200 bg-white/90 p-6 shadow-sm backdrop-blur">
          <h2 className="text-xl font-semibold text-slate-900">Submitted Payload</h2>
          <pre className="mt-3 overflow-auto rounded-xl bg-slate-950 p-4 text-xs text-slate-100">
            {JSON.stringify(submittedData, null, 2)}
          </pre>
        </section>
      ) : null}
    </main>
  )
}

export default App
