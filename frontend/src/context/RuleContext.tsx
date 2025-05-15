import { createContext, useContext, useState, useEffect } from "react";
import type { Condition, RuleCondition } from "../types/condition";
import type { Action, RuleContextType } from "../types/rule";
import { getConditions, addCondition } from "../api/condition";

const RuleContext = createContext<RuleContextType | undefined>(undefined);

export const RuleProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [conditions, setConditions] = useState<RuleCondition[]>([]);
  const [actions, setActions] = useState<Action[]>([]);
  const [conditionTypes, setConditionTypes] = useState<Condition[]>([]);

  useEffect(() => {
    const loadConditions = async () => {
      const fetchedConditions = await getConditions();
      console.log(fetchedConditions);
      setConditionTypes(fetchedConditions);
    };

    loadConditions();
  }, []);

  const createCondition = async (newCondition: Condition) => {
    try {
      const savedCondition = await addCondition(newCondition);
      const ruleCondition: RuleCondition = {
        field: savedCondition.field,
        value: savedCondition.value as string,
        year: savedCondition.year,
        condition_type_id: savedCondition.id,
      };
      setConditions((prev) => [...prev, ruleCondition]);
    } catch (error) {
      console.error("Failed to add condition:", error);
    }
  };

  const addConditionToRule = (condition: RuleCondition) => {
    console.log("Adding condition to rule:", condition);
    setConditions((prev) => {
      const newConditions = [...prev, condition];
      console.log("Updated conditions:", newConditions);
      return newConditions;
    });
  };

  const addAction = (action: Action) => {
    setActions([...actions, action]);
  };

  return (
    <RuleContext.Provider
      value={{
        conditions,
        actions,
        conditionTypes,
        createCondition,
        addConditionToRule,
        addAction,
      }}
    >
      {children}
    </RuleContext.Provider>
  );
};

export const useRuleContext = () => {
  const context = useContext(RuleContext);
  if (!context) {
    throw new Error("useRuleContext must be used within a RuleProvider");
  }
  return context;
};
