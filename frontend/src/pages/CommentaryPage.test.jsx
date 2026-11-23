import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { CommentaryPage } from "./CommentaryPage.jsx";

vi.mock("../services/commentaryService.js", () => ({
  commentaryService: {
    getReadiness: vi.fn().mockResolvedValue({
      data: {
        status: "READY",
        available_months: ["2026-01", "2026-02"],
        available_metrics: ["gross_margin"],
        warnings: [],
      },
    }),
    analyzeVariance: vi.fn(),
  },
}));

describe("CommentaryPage", () => {
  it("shows data readiness before analysis", async () => {
    render(<CommentaryPage />);
    expect(await screen.findByText(/Data readiness:/)).toBeInTheDocument();
    expect(screen.getByText(/gross_margin/)).toBeInTheDocument();
  });
});
