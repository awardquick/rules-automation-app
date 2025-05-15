import { render, screen, waitFor, fireEvent } from "@testing-library/react";
import "@testing-library/jest-dom";
import { BrowserRouter } from "react-router-dom";
import Home from "../Home";
import { getRules } from "../../api/rule";
import { getConditions } from "../../api/condition";
import { act } from "react";

// Mock the API calls
jest.mock("../../api/rule");
jest.mock("../../api/condition");

const mockRules = [
  {
    id: 1,
    name: "Test Rule 1",
    description: "Test Description 1",
    is_active: true,
    conditions: [
      {
        condition_type_id: 1,
        value: "test",
        year: 2024,
      },
    ],
    action: "Test Action 1",
    action_description: "Test Action Description 1",
  },
];

const mockConditions = [{ id: 1, name: "Test Condition", field: "test_field" }];

describe("Home Component", () => {
  beforeEach(() => {
    jest.clearAllMocks();
    // Make the API calls return promises that don't resolve immediately
    (getRules as jest.Mock).mockImplementation(() => new Promise(() => {}));
    (getConditions as jest.Mock).mockImplementation(
      () => new Promise(() => {})
    );
  });

  const renderWithRouter = (component: React.ReactNode) => {
    return render(<BrowserRouter>{component}</BrowserRouter>);
  };

  it("shows loading state initially", async () => {
    await act(async () => {
      renderWithRouter(<Home />);
    });

    expect(screen.getByText("Loading rules...")).toBeInTheDocument();
  });

  it("renders rules when data is loaded", async () => {
    // Reset mocks to resolve with data
    (getRules as jest.Mock).mockResolvedValue(mockRules);
    (getConditions as jest.Mock).mockResolvedValue(mockConditions);

    await act(async () => {
      renderWithRouter(<Home />);
    });

    // Wait for the rules to be loaded
    await waitFor(() => {
      expect(screen.getByText("Test Rule 1")).toBeInTheDocument();
    });

    expect(screen.getByText("Test Description 1")).toBeInTheDocument();
    expect(screen.getByText("Test Action 1")).toBeInTheDocument();

    // Check for action description with dash
    const actionDescription = screen.getByText((content, element) => {
      return element?.textContent === "- Test Action Description 1";
    });
    expect(actionDescription).toBeInTheDocument();

    expect(
      screen.getByText("Test Condition: test in 2024")
    ).toBeInTheDocument();
  });

  it("shows empty state when no rules exist", async () => {
    // Reset mocks to resolve with empty data
    (getRules as jest.Mock).mockResolvedValue([]);
    (getConditions as jest.Mock).mockResolvedValue(mockConditions);

    await act(async () => {
      renderWithRouter(<Home />);
    });

    await waitFor(() => {
      expect(screen.getByText("No rules yet")).toBeInTheDocument();
      expect(
        screen.getByText("Create your first rule to get started")
      ).toBeInTheDocument();
    });
  });

  it("handles API errors gracefully", async () => {
    // Mock both API calls to reject
    (getRules as jest.Mock).mockRejectedValueOnce(new Error("API Error"));
    (getConditions as jest.Mock).mockRejectedValueOnce(new Error("API Error"));

    await act(async () => {
      renderWithRouter(<Home />);
    });

    await waitFor(() => {
      expect(
        screen.getByText("Failed to load data. Please try again.")
      ).toBeInTheDocument();
    });
  });

  it("navigates to create rule page when button is clicked", async () => {
    // Reset mocks to resolve with data
    (getRules as jest.Mock).mockResolvedValue(mockRules);
    (getConditions as jest.Mock).mockResolvedValue(mockConditions);

    await act(async () => {
      renderWithRouter(<Home />);
    });

    // Wait for loading to complete
    await waitFor(() => {
      expect(screen.getByText("Test Rule 1")).toBeInTheDocument();
    });

    const createButton = screen.getByText("Create New Rule");
    await act(async () => {
      fireEvent.click(createButton);
    });

    expect(window.location.pathname).toBe("/rules/new");
  });
});
