import { useState } from "react";
import { useRuleContext } from "../context/RuleContext";
import type { Condition, RuleCondition } from "../types/condition";

const ConditionBuilder: React.FC = () => {
  const [selectedField, setSelectedField] = useState("");
  const [selectedValue, setSelectedValue] = useState<string | boolean>("");
  const [selectedYear, setSelectedYear] = useState<number>(
    new Date().getFullYear()
  );
  const { conditionTypes, addConditionToRule } = useRuleContext();
  const [selectedConditions, setSelectedConditions] = useState<RuleCondition[]>(
    []
  );

  const handleAddCondition = () => {
    if (!selectedField || selectedValue === "") return;

    const selectedType = conditionTypes.find(
      (type) => type.field === selectedField
    );
    if (selectedType) {
      const newCondition: RuleCondition = {
        field: selectedField,
        value: selectedValue as string,
        year:
          selectedType.data_type === "year_boolean" ? selectedYear : undefined,
        condition_type_id: selectedType.id,
      };
      setSelectedConditions([...selectedConditions, newCondition]);
      addConditionToRule(newCondition);
      setSelectedField("");
      setSelectedValue("");
      setSelectedYear(new Date().getFullYear());
    }
  };

  const renderValueInput = () => {
    const selectedType = conditionTypes.find(
      (type) => type.field === selectedField
    );
    if (!selectedType) return null;

    switch (selectedType.data_type) {
      case "boolean":
        return (
          <select
            className="border border-gray-300 w-[318px] h-10 px-4 py-2 text-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary text-sm mt-2"
            value={selectedValue as string}
            onChange={(e) => setSelectedValue(e.target.value)}
          >
            <option value="">Select Value</option>
            <option value="true">Yes</option>
            <option value="false">No</option>
          </select>
        );
      case "enum":
        return (
          <select
            className="border border-gray-300 w-[318px] h-10 px-4 py-2 text-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary text-sm mt-2"
            value={selectedValue as string}
            onChange={(e) => setSelectedValue(e.target.value)}
          >
            <option value="">Select Value</option>
            {selectedType.options &&
              selectedType.options.map((option: string) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
          </select>
        );
      case "year_boolean":
        return (
          <div className="flex gap-2 mt-2">
            <select
              className="border border-gray-300 w-[200px] h-10 px-4 py-2 text-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary text-sm"
              value={selectedValue as string}
              onChange={(e) => setSelectedValue(e.target.value)}
            >
              <option value="">Select Value</option>
              <option value="true">Filed</option>
              <option value="false">Did Not File</option>
            </select>
            <input
              type="number"
              className="border border-gray-300 w-[110px] h-10 px-4 py-2 text-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary text-sm"
              value={selectedYear}
              onChange={(e) => setSelectedYear(parseInt(e.target.value))}
              min={2000}
              max={new Date().getFullYear()}
            />
          </div>
        );
      default:
        return null;
    }
  };

  const formatConditionValue = (condition: RuleCondition) => {
    const type = conditionTypes.find((t) => t.field === condition.field);
    if (type?.data_type === "year_boolean") {
      return `${condition.value === "true" ? "Filed" : "Did Not File"} in ${
        condition.year
      }`;
    } else if (type?.data_type === "boolean") {
      return condition.value === "true" ? "Yes" : "No";
    }
    return condition.value;
  };

  return (
    <div className="p-4 mt-6">
      <div className="flex flex-col gap-2">
        <select
          className="border border-gray-300 w-[318px] h-10 px-4 py-2 text-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary text-sm"
          value={selectedField}
          onChange={(e) => setSelectedField(e.target.value)}
        >
          <option value="">Select Field</option>
          {conditionTypes.map((type) => (
            <option key={type.id} value={type.field}>
              {type.name}
            </option>
          ))}
        </select>
        {selectedField && renderValueInput()}
      </div>
      <div className="mt-4">
        {selectedConditions.map((condition, idx) => {
          const type = conditionTypes.find((t) => t.field === condition.field);
          return (
            <div key={idx} className="flex items-center gap-2 mb-2">
              <span className="text-gray-700">• {type?.name}:</span>
              <span className="text-gray-900 font-medium">
                {formatConditionValue(condition)}
              </span>
            </div>
          );
        })}
      </div>
      <button
        className="text-[#755DC8] rounded mt-2"
        onClick={handleAddCondition}
        disabled={!selectedField || selectedValue === ""}
      >
        Add Condition
      </button>
    </div>
  );
};

export default ConditionBuilder;
