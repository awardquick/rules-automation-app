import { render, screen, waitFor, fireEvent } from "@testing-library/react";
import "@testing-library/jest-dom";
import { BrowserRouter } from "react-router-dom";
import RuleEditor from "../RuleEditor";
import { createRule } from "../../api/rule";
import { RuleProvider, useRuleContext } from "../../context/RuleContext";
import { act } from "react";
import { getConditions } from "../../api/condition";

// Mock the API calls
jest.mock("../../api/rule");
jest.mock("../../api/condition");

const mockConditions = [
  { id: 1, name: "Test Condition", field: "test_field", data_type: "boolean" },
];

// Mock the RuleContext
jest.mock("../../context/RuleContext", () => ({
  useRuleContext: jest.fn(() => ({
    conditions: [],
    actions: [],
    conditionTypes: mockConditions,
    addCondition: jest.fn(),
    removeCondition: jest.fn(),
    updateCondition: jest.fn(),
    addAction: jest.fn(),
    removeAction: jest.fn(),
    updateAction: jest.fn(),
  })),
  RuleProvider: ({ children }: { children: React.ReactNode }) => (
    <>{children}</>
  ),
}));

describe("RuleEditor Component", () => {
  beforeEach(() => {
    // Reset all mocks before each test
    jest.clearAllMocks();

    // Setup default mock implementations
    (createRule as jest.Mock).mockResolvedValue({ id: 1 });
    (getConditions as jest.Mock).mockResolvedValue(mockConditions);
  });

  const renderWithRouter = (component: React.ReactNode) => {
    return render(
      <BrowserRouter>
        <RuleProvider>{component}</RuleProvider>
      </BrowserRouter>
    );
  };

  it("renders the rule editor form", async () => {
    await act(async () => {
      renderWithRouter(<RuleEditor />);
    });

    expect(screen.getByPlaceholderText("Rule Name")).toBeInTheDocument();
    expect(
      screen.getByPlaceholderText("Rule Description (optional)")
    ).toBeInTheDocument();
    expect(screen.getByText("Conditions")).toBeInTheDocument();
    expect(screen.getByText("Actions")).toBeInTheDocument();
    expect(screen.getByText("Select Field")).toBeInTheDocument();
  });

  it("shows error when trying to save without a rule name", async () => {
    await act(async () => {
      renderWithRouter(<RuleEditor />);
    });

    const saveButton = screen.getByText("Save and Enable Rule");
    await act(async () => {
      fireEvent.click(saveButton);
    });

    expect(screen.getByText("Rule name is required")).toBeInTheDocument();
  });

  it("shows error when trying to save without conditions", async () => {
    await act(async () => {
      renderWithRouter(<RuleEditor />);
    });

    // Enter rule name
    const nameInput = screen.getByPlaceholderText("Rule Name");
    await act(async () => {
      fireEvent.change(nameInput, { target: { value: "Test Rule" } });
    });

    // Try to save without adding conditions
    const saveButton = screen.getByText("Save and Enable Rule");
    await act(async () => {
      fireEvent.click(saveButton);
    });

    expect(
      screen.getByText("At least one condition is required")
    ).toBeInTheDocument();
  });

  it("handles API errors gracefully", async () => {
    // Mock the RuleContext with a condition and action
    (useRuleContext as jest.Mock).mockImplementation(() => ({
      conditions: [{ condition_type_id: 1, value: "test", year: 2024 }],
      actions: [{ type: "Test Action", description: "Test Description" }],
      conditionTypes: mockConditions,
      addCondition: jest.fn(),
      removeCondition: jest.fn(),
      updateCondition: jest.fn(),
      addAction: jest.fn(),
      removeAction: jest.fn(),
      updateAction: jest.fn(),
    }));

    // Mock the createRule to reject
    (createRule as jest.Mock).mockRejectedValueOnce(new Error("API Error"));

    await act(async () => {
      renderWithRouter(<RuleEditor />);
    });

    // Enter a rule name
    const nameInput = screen.getByPlaceholderText("Rule Name");
    await act(async () => {
      fireEvent.change(nameInput, { target: { value: "Test Rule" } });
    });

    // Try to save
    const saveButton = screen.getByText("Save and Enable Rule");
    await act(async () => {
      fireEvent.click(saveButton);
    });

    await waitFor(() => {
      expect(
        screen.getByText("Failed to save rule. Please try again.")
      ).toBeInTheDocument();
    });
  });

  it("navigates back to home when cancel is clicked", async () => {
    await act(async () => {
      renderWithRouter(<RuleEditor />);
    });

    const cancelButton = screen.getByText("Cancel");
    await act(async () => {
      fireEvent.click(cancelButton);
    });

    expect(window.location.pathname).toBe("/");
  });
});
