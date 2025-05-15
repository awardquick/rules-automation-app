import { createContext, useContext, useState, useEffect } from "react";
import type { Condition, RuleCondition } from "../types/condition";
import type { Action, RuleContextType } from "../types/rule";
import { getConditions } from "../api/condition";

const RuleContext = createContext<RuleContextType | undefined>(undefined);

export const RuleProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [conditions, setConditions] = useState<RuleCondition[]>([]);
  const [actions, setActions] = useState<Action[]>([]);
  const [conditionTypes, setConditionTypes] = useState<Condition[]>([]);

  useEffect(() => {
    const loadConditions = async () => {
      try {
        const fetchedConditions = await getConditions();
        setConditionTypes(fetchedConditions);
      } catch (error) {
        console.error("Failed to load conditions:", error);
      }
    };

    loadConditions();
  }, []);

  // const createCondition = async (newCondition: Condition) => {
  //   try {
  //     const savedCondition = await addCondition(newCondition);
  //     const ruleCondition: RuleCondition = {
  //       field: savedCondition.field,
  //       value: savedCondition.value as string,
  //       year: savedCondition.year,
  //       condition_type_id: savedCondition.id,
  //     };
  //     setConditions((prev) => [...prev, ruleCondition]);
  //   } catch (error) {
  //     console.error("Failed to add condition:", error);
  //   }
  // };

  const addConditionToRule = (condition: RuleCondition) => {
    setConditions((prev) => {
      // Check if condition already exists
      const exists = prev.some(
        (c) =>
          c.field === condition.field &&
          c.value === condition.value &&
          c.year === condition.year
      );

      if (exists) {
        return prev;
      }

      return [...prev, condition];
    });
  };

  const removeCondition = (index: number) => {
    setConditions((prev) => prev.filter((_, i) => i !== index));
  };

  const addAction = (action: Action) => {
    setActions((prev) => {
      // Check if action already exists
      const exists = prev.some(
        (a) => a.type === action.type && a.description === action.description
      );

      if (exists) {
        return prev;
      }

      return [...prev, action];
    });
  };

  const removeAction = (index: number) => {
    setActions((prev) => prev.filter((_, i) => i !== index));
  };

  return (
    <RuleContext.Provider
      value={{
        conditions,
        actions,
        conditionTypes,
        addConditionToRule,
        removeCondition,
        addAction,
        removeAction,
      }}
    >
      {children}
    </RuleContext.Provider>
  );
};

export const useRuleContext = () => {
  const context = useContext(RuleContext);
  if (context === undefined) {
    throw new Error("useRuleContext must be used within a RuleProvider");
  }
  return context;
};
