import { createContext, useContext, useState } from "react";
import type { Condition, Action, RuleContextType } from "../types/rule";

const RuleContext = createContext<RuleContextType | undefined>(undefined);

export const RuleProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [conditions, setConditions] = useState<Condition[]>([]);
  const [actions, setActions] = useState<Action[]>([]);

  const addCondition = (condition: Condition) => {
    setConditions([...conditions, condition]);
  };

  const addAction = (action: Action) => {
    setActions([...actions, action]);
  };

  return (
    <RuleContext.Provider
      value={{ conditions, actions, addCondition, addAction }}
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
