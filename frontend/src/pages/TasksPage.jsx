import { useCallback, useEffect, useState } from "react";
import { useHasAccess } from "@savic-technologies-pvt-ltd/platform-common";
import { API_RESOURCE_KEY } from "../constants.js";
import { tasksService } from "../services/tasksService.js";

// The example page: list, add, complete and delete tasks. Buttons appear
// only for the actions the user's role grants (Access Matrix); the backend
// checks the same grants again on every call.
export function TasksPage() {
  const canCreate = useHasAccess(API_RESOURCE_KEY, "CREATE");
  const canEdit = useHasAccess(API_RESOURCE_KEY, "EDIT");
  const canDelete = useHasAccess(API_RESOURCE_KEY, "DELETE");

  const [tasks, setTasks] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const [title, setTitle] = useState("");
  const [dueDate, setDueDate] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const res = await tasksService.list({ page_size: 100 });
      setTasks(res.data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  async function run(action) {
    try {
      await action();
      await load();
    } catch (err) {
      setError(err.message);
    }
  }

  async function onAdd(event) {
    event.preventDefault();
    if (!title.trim()) return;
    await run(() => tasksService.create({ title, due_date: dueDate || null }));
    setTitle("");
    setDueDate("");
  }

  return (
    <div style={{ padding: "1.5rem", maxWidth: 760 }}>
      <h2 style={{ marginTop: 0 }}>Tasks</h2>

      {canCreate && (
        <form
          onSubmit={onAdd}
          style={{ display: "flex", gap: "0.5rem", marginBottom: "1rem" }}
        >
          <input
            aria-label="Task title"
            placeholder="New task"
            value={title}
            maxLength={200}
            onChange={(e) => setTitle(e.target.value)}
            style={{ flex: 1 }}
          />
          <input
            aria-label="Due date"
            type="date"
            value={dueDate}
            onChange={(e) => setDueDate(e.target.value)}
          />
          <button type="submit">Add</button>
        </form>
      )}

      {error && (
        <p role="alert" style={{ color: "var(--color-error, #b91c1c)" }}>
          {error}
        </p>
      )}
      {loading && <p>Loading…</p>}
      {!loading && tasks.length === 0 && <p>No tasks yet.</p>}

      <ul style={{ listStyle: "none", padding: 0 }}>
        {tasks.map((task) => (
          <li
            key={task.id}
            style={{
              display: "flex",
              alignItems: "center",
              gap: "0.75rem",
              padding: "0.5rem 0",
              borderBottom: "1px solid var(--color-border, #e5e7eb)",
            }}
          >
            <input
              type="checkbox"
              aria-label={`Done: ${task.title}`}
              checked={task.status === "DONE"}
              disabled={!canEdit}
              onChange={(e) =>
                run(() =>
                  tasksService.update(task.id, {
                    status: e.target.checked ? "DONE" : "OPEN",
                  }),
                )
              }
            />
            <span
              style={{
                flex: 1,
                textDecoration:
                  task.status === "DONE" ? "line-through" : "none",
              }}
            >
              {task.title}
            </span>
            {task.due_date && (
              <span
                style={{
                  fontSize: "0.85rem",
                  color: "var(--color-text-secondary, #6b7280)",
                }}
              >
                due {task.due_date}
              </span>
            )}
            {canDelete && (
              <button
                type="button"
                onClick={() => run(() => tasksService.remove(task.id))}
              >
                Delete
              </button>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
