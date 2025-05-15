import ActionBuilder from "../components/ActionBuilder";
import ConditionBuilder from "../components/ConditionBuilder";
import SectionHeader from "../components/SectionHeader";
import Header from "../components/Header";
import ConditionFooter from "../components/ConditionFooter";
import { useEffect, useState } from "react";
import { useRuleContext } from "../context/RuleContext";
import { createRule } from "../api/rule";
import { useNavigate } from "react-router-dom";
import apiClient from "../api/client";

const RuleEditor: React.FC = () => {
  const navigate = useNavigate();
  const { conditions, actions } = useRuleContext();
  const [ruleName, setRuleName] = useState("");
  const [ruleDescription, setRuleDescription] = useState("");
  const [matchingApplicants, setMatchingApplicants] = useState<number>(0);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchMatchingApplicants = async () => {
      try {
        const { data } = await apiClient.post("/applicants/match-count", {
          conditions: conditions.map((condition) => ({
            field: condition.field,
            value: condition.value,
            year: condition.year,
          })),
        });
        setMatchingApplicants(data.count);
      } catch (error) {
        console.error("Failed to fetch matching applicants:", error);
      }
    };

    if (conditions.length > 0) {
      fetchMatchingApplicants();
    } else {
      setMatchingApplicants(0);
    }
  }, [conditions]);

  const handleCancel = () => {
    navigate("/");
  };

  const handleSave = async () => {
    if (!ruleName.trim()) {
      setError("Rule name is required");
      return;
    }

    if (conditions.length === 0) {
      setError("At least one condition is required");
      return;
    }

    if (actions.length === 0) {
      setError("At least one action is required");
      return;
    }

    setIsSaving(true);
    setError(null);

    try {
      const rule = {
        name: ruleName,
        description: ruleDescription,
        conditions: conditions.map((condition) => ({
          condition_type_id: condition.condition_type_id,
          value: condition.value,
          year: condition.year,
        })),
        action: actions[0].type,
        action_description: actions[0].description,
      };

      await createRule(rule);
      navigate("/");
    } catch (error) {
      setError("Failed to save rule. Please try again.");
      console.error("Failed to save rule:", error);
    } finally {
      setIsSaving(false);
    }
  };

  const handleBack = () => {
    navigate("/");
  };

  return (
    <>
      <Header
        onCancel={handleCancel}
        onSave={handleSave}
        onBack={handleBack}
        isSaving={isSaving}
      />
      <div className="w-full min-h-screen p-8 bg-gray-50 shadow rounded-lg">
        {error && (
          <div className="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
            {error}
          </div>
        )}
        <div className="mb-6">
          <input
            type="text"
            placeholder="Rule Name"
            value={ruleName}
            onChange={(e) => setRuleName(e.target.value)}
            className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
          />
          <textarea
            placeholder="Rule Description (optional)"
            value={ruleDescription}
            onChange={(e) => setRuleDescription(e.target.value)}
            className="w-full mt-2 p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
            rows={3}
          />
        </div>
        <div className="border border-gray-300 rounded-lg">
          <SectionHeader title="Conditions" color="primary" />
          <div className="p-6 flex items-start max-w-[1120px]">
            <div className="flex justify-end" style={{ minWidth: "60px" }}>
              <p className="text-gray-500 font-medium m-0 mt-10">If</p>
            </div>
            <div className="flex-1 ml-4">
              <ConditionBuilder />
            </div>
          </div>
          <ConditionFooter matchingApplicants={matchingApplicants} />
        </div>

        <div className="flex">
          <div
            className="w-px bg-gray-200 ml-[32px]"
            style={{ height: "80px" }}
          ></div>
        </div>

        <div className="border border-gray-300 rounded-lg">
          <SectionHeader title="Actions" color="success" />
          <ActionBuilder />
        </div>
      </div>
    </>
  );
};

export default RuleEditor;
