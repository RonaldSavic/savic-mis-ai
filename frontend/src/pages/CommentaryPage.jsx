import { useEffect, useState } from "react";
import { commentaryService } from "../services/commentaryService.js";

export function CommentaryPage() {
  const [form, setForm] = useState({
    company_code: "1000",
    prior_month: "2026-01",
    current_month: "2026-02",
    currency: "INR",
    question: "Why did gross margin change?",
  });
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [readiness, setReadiness] = useState(null);

  useEffect(() => {
    commentaryService
      .getReadiness(form.company_code, form.currency)
      .then((response) => setReadiness(response.data))
      .catch(() => setReadiness(null));
  }, [form.company_code, form.currency]);

  function update(field, value) {
    setForm((current) => ({ ...current, [field]: value }));
  }

  async function submit(event) {
    event.preventDefault();
    setError(null);
    setResult(null);
    try {
      const response = await commentaryService.analyzeVariance(form);
      setResult(response.data);
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div style={{ padding: "1.5rem", maxWidth: 900 }}>
      <h2 style={{ marginTop: 0 }}>Commentary Analysis</h2>
      <p>
        Deterministic gross-margin variance analysis from the local semantic
        snapshot. No LLM explanation is generated yet.
      </p>
      {readiness && (
        <section aria-label="Data readiness">
          <p>
            Data readiness: <strong>{readiness.status}</strong>; periods: {readiness.available_months.join(", ") || "none"}
          </p>
          <p>Available metrics: {readiness.available_metrics.join(", ") || "none"}</p>
          {readiness.warnings?.length > 0 && (
            <ul role="status">
              {readiness.warnings.map((warning) => <li key={warning}>{warning}</li>)}
            </ul>
          )}
        </section>
      )}
      <form onSubmit={submit} style={{ display: "flex", gap: "0.5rem", flexWrap: "wrap" }}>
        <input aria-label="Company code" value={form.company_code} onChange={(e) => update("company_code", e.target.value)} />
        <input aria-label="Prior month" type="month" value={form.prior_month} onChange={(e) => update("prior_month", e.target.value)} />
        <input aria-label="Current month" type="month" value={form.current_month} onChange={(e) => update("current_month", e.target.value)} />
        <input aria-label="Currency" value={form.currency} maxLength={3} onChange={(e) => update("currency", e.target.value.toUpperCase())} />
        <input aria-label="Question" value={form.question} onChange={(e) => update("question", e.target.value)} style={{ flexBasis: "100%" }} />
        <button type="submit">Analyze</button>
      </form>
      {error && <p role="alert" style={{ color: "var(--color-error, #b91c1c)" }}>{error}</p>}
      {result && (
        <section aria-label="Commentary result" style={{ marginTop: "1.5rem" }}>
          <h3>{result.status}</h3>
          <p>{result.summary}</p>
          {result.variance && <p>Variance: {result.variance} ({result.variance_pct}%)</p>}
          <h4>Evidence</h4>
          <ul>
            {result.evidence.map((item) => (
              <li key={`${item.metric}-${item.period}`}>
                {item.period}: {item.metric} = {item.value} ({item.interpretation})
              </li>
            ))}
          </ul>
          <h4>Caveats</h4>
          <ul>{result.caveats.map((caveat) => <li key={caveat}>{caveat}</li>)}</ul>
          {result.knowledge?.length > 0 && (
            <>
              <h4>Metric definitions</h4>
              <ul>
                {result.knowledge.map((item) => (
                  <li key={item.id}>
                    {item.title}: {item.definition} (score {item.relevance_score ?? "n/a"}; {item.source})
                  </li>
                ))}
              </ul>
            </>
          )}
          {result.sources?.length > 0 && (
            <p><strong>Sources:</strong> {result.sources.join(", ")}</p>
          )}
          {result.retrieval_method && (
            <p><strong>Retrieval:</strong> {result.retrieval_method}</p>
          )}
        </section>
      )}
    </div>
  );
}
