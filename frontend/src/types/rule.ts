import type { Condition, RuleCondition } from "./condition";

export interface Action {
    type: string;
    description: string;
}

export interface RuleContextType {
    conditions: RuleCondition[];
    actions: Action[];
    conditionTypes: Condition[];
    createCondition: (condition: Condition) => Promise<void>;
    addConditionToRule: (condition: RuleCondition) => void;
    addAction: (action: Action) => void;
}

export type RuleConditionInput = {
    condition_type_id: number;
    value: string;
    year?: number;
};

export type RuleCreate = {
    name: string;
    description?: string;
    conditions: RuleConditionInput[];
    action: string;
    action_description?: string;
};

export type RuleResponse = {
    id: number;
    name: string;
    description?: string;
    conditions: RuleConditionInput[];
    action: string;
    action_description?: string;
    is_active: boolean;
    created_at: string;
    updated_at: string;
};
  