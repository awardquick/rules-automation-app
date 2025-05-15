import { useState } from "react";
import { useRuleContext } from "../context/RuleContext";

const ConditionBuilder: React.FC = () => {
  const [selectedField, setSelectedField] = useState("");
  const { addCondition, conditions } = useRuleContext();

  return (
    <>
      <div className="p-4 mt-6">
        {/* <h2 className="text-lg font-semibold">Conditions</h2> */}
        <select
          className="border border-gray-300 w-[318px] h-10 px-4 py-2 text-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary text-sm"
          value={selectedField}
          onChange={(e) => setSelectedField(e.target.value)}
        >
          <option value="">Select Field</option>
          <option value="Is Business Owner">Is Business Owner</option>
          <option value="Has Dependents">Has Dependents</option>
        </select>
        <div className="mt-4">
          {conditions.map((condition, idx) => (
            <p key={idx}> • {condition.field} </p>
          ))}
        </div>
        <button
          className="text-[#755DC8] rounded"
          onClick={() =>
            selectedField && addCondition({ field: selectedField })
          }
        >
          Add Condition
        </button>
      </div>
    </>
  );
};

export default ConditionBuilder;
