import type { RuleCreate, RuleResponse } from "../types/rule";

export const createRule = async (rule: RuleCreate): Promise<RuleResponse> => {
  const response = await fetch("/api/rules", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(rule),
  });

  if (!response.ok) {
    throw new Error("Failed to create rule");
  }

  return response.json();
};

export const getRules = async (): Promise<RuleResponse[]> => {
  const response = await fetch("/api/rules");
  
  if (!response.ok) {
    throw new Error("Failed to fetch rules");
  }

  return response.json();
}; 