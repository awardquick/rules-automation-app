import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import type { RuleResponse } from "../types/rule";
import type { Condition } from "../types/condition";
import { getRules } from "../api/rule";
import { getConditions } from "../api/condition";

const Home: React.FC = () => {
  const navigate = useNavigate();
  const [rules, setRules] = useState<RuleResponse[]>([]);
  const [conditionTypes, setConditionTypes] = useState<Condition[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        console.log("Fetching rules and conditions...");
        const [rulesData, conditionTypesData] = await Promise.all([
          getRules(),
          getConditions(),
        ]);
        console.log("Rules data:", rulesData);
        console.log("Condition types data:", conditionTypesData);
        setRules(rulesData);
        setConditionTypes(conditionTypesData);
      } catch (error) {
        console.error("Error details:", error);
        setError("Failed to load data. Please try again.");
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  const getConditionName = (conditionTypeId: number) => {
    const conditionType = conditionTypes.find(
      (ct) => ct.id === conditionTypeId
    );
    return conditionType?.name || "Unknown Condition";
  };

  const handleCreateRule = () => {
    navigate("/rules/new");
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-gray-600">Loading rules...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-2xl font-semibold text-gray-900">Rules</h1>
          <button
            onClick={handleCreateRule}
            className="px-4 py-2 bg-[#755DC8] text-white rounded-lg hover:bg-[#6849C2]"
          >
            Create New Rule
          </button>
        </div>

        {error && (
          <div className="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
            {error}
          </div>
        )}

        {rules.length === 0 ? (
          <div className="text-center py-12">
            <h2 className="text-xl font-medium text-gray-900 mb-2">
              No rules yet
            </h2>
            <p className="text-gray-600 mb-4">
              Create your first rule to get started
            </p>
            <button
              onClick={handleCreateRule}
              className="px-4 py-2 bg-[#755DC8] text-white rounded-lg hover:bg-[#6849C2]"
            >
              Create New Rule
            </button>
          </div>
        ) : (
          <div className="grid gap-6">
            {rules.map((rule) => (
              <div
                key={rule.id}
                className="bg-white p-6 rounded-lg shadow border border-gray-200"
              >
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h2 className="text-lg font-semibold text-gray-900">
                      {rule.name}
                    </h2>
                    {rule.description && (
                      <p className="text-gray-600 mt-1">{rule.description}</p>
                    )}
                  </div>
                  <div className="flex items-center gap-2">
                    <span
                      className={`px-2 py-1 rounded text-sm ${
                        rule.is_active
                          ? "bg-green-100 text-green-800"
                          : "bg-gray-100 text-gray-800"
                      }`}
                    >
                      {rule.is_active ? "Active" : "Inactive"}
                    </span>
                  </div>
                </div>

                <div className="space-y-4">
                  <div>
                    <h3 className="text-sm font-medium text-gray-700 mb-2">
                      Conditions
                    </h3>
                    <ul className="space-y-1">
                      {rule.conditions.map((condition, index) => (
                        <li
                          key={index}
                          className="text-sm text-gray-600 flex items-center gap-2"
                        >
                          <span className="text-gray-400">•</span>
                          {getConditionName(condition.condition_type_id)}:{" "}
                          {condition.value}
                          {condition.year && ` in ${condition.year}`}
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div>
                    <h3 className="text-sm font-medium text-gray-700 mb-2">
                      Action
                    </h3>
                    <p className="text-sm text-gray-600">
                      {rule.action}
                      {rule.action_description && (
                        <span className="text-gray-500 ml-2">
                          - {rule.action_description}
                        </span>
                      )}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Home;
