import { useState } from "react";
import { useRuleContext } from "../context/RuleContext";

const ActionBuilder: React.FC = () => {
  const [type, setType] = useState("");
  const [description, setDescription] = useState("");
  const { addAction, actions } = useRuleContext();

  return (
    <div className="flex flex-col p-4 rounded-lg shadow">
      <div className="flex items-center gap-4">
        <select
          className="border border-gray-300 rounded w-[318px] h-10 px-4 py-2 ml-10 text-gray-700 focus:outline-none focus:ring-2 focus:ring-primary text-sm"
          value={type}
          onChange={(e) => setType(e.target.value)}
        >
          <option value="">Select Document Type</option>
          <option value="Business Tax Documents">Business Tax Documents</option>
          <option value="Personal Tax Documents">Personal Tax Documents</option>
        </select>
        <input
          type="text"
          placeholder="Description of Document"
          className="border border-gray-300 rounded w-[454px] h-10 p-2"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
      </div>
      <div className="ml-10">
        <button
          className="text-[#755DC8] rounded mt-4"
          onClick={() =>
            type &&
            addAction({
              type,
              description,
            })
          }
        >
          Create Document Request
        </button>
      </div>
      <div className="mt-4 ml-10">
        {actions.map((action, idx) => (
          <p key={idx}>
            • {action.type}: {action.description}
          </p>
        ))}
      </div>
    </div>
  );
};

export default ActionBuilder;
