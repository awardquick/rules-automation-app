export type Condition = {
  id: number;
  name: string;
  field: string;
  description: string;
  data_type: "boolean" | "enum" | "year_boolean";
  options?: string[];
  year_field?: string;
  value?: string | boolean;
  year?: number;
};

export type RuleCondition = {
  field: string;
  value: string;
  year?: number;
  condition_type_id: number;
};