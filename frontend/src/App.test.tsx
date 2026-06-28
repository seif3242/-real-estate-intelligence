import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import App from "./App";

describe("App", () => {
  it("renders the app shell heading", () => {
    render(<App />);
    expect(screen.getByText("Real Estate AI Assistant")).toBeInTheDocument();
  });
});
