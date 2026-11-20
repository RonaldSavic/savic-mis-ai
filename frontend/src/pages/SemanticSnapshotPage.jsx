import { useEffect, useState } from "react";
import { semanticService } from "../services/semanticService.js";

export function SemanticSnapshotPage() {
  const [document, setDocument] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    semanticService
      .getSnapshot()
      .then((response) => setDocument(response.data))
      .catch((err) => setError(err.message));
  }, []);

  return (
    <div style={{ padding: "1.5rem", maxWidth: 1000 }}>
      <h2 style={{ marginTop: 0 }}>Semantic Snapshot</h2>
      <p>Read-only metrics generated from the local semantic pipeline.</p>
      {error && (
        <p role="alert" style={{ color: "var(--color-error, #b91c1c)" }}>
          {error}
        </p>
      )}
      {!document && !error && <p>Loading…</p>}
      {document && (
        <>
          <p>
            Source files: {document.source_files.join(", ")} · Definitions: {document.definitions_version}
          </p>
          <pre
            style={{
              overflowX: "auto",
              padding: "1rem",
              background: "#f3f4f6",
              borderRadius: "0.25rem",
            }}
          >
            {JSON.stringify(document.records, null, 2)}
          </pre>
        </>
      )}
    </div>
  );
}
