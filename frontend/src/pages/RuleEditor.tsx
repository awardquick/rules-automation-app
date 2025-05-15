import ActionBuilder from "../components/ActionBuilder";
import ConditionBuilder from "../components/ConditionBuilder";
import SectionHeader from "../components/SectionHeader";
import Header from "../components/Header";
import ConditionFooter from "../components/ConditionFooter";
import { useEffect, useState } from "react";
const RuleEditor: React.FC = () => {
  const handleCancel = () => {
    console.log("Cancel clicked");
  };

  const handleSave = () => {
    console.log("Save clicked");
  };

  const handleBack = () => {
    console.log("Back clicked");
  };

  const [matchingApplicants, setMatchingApplicants] = useState<number>(0);

  useEffect(() => {
    const fetchMatchingApplicants = async () => {
      const response = await fetch("/api/applicants/match-count");
      const data = await response.json();
      setMatchingApplicants(data.count); // Assuming API returns { count: number }
    };

    fetchMatchingApplicants();
  }, []);

  return (
    <>
      <Header onCancel={handleCancel} onSave={handleSave} onBack={handleBack} />
      <div className="w-full min-h-screen p-8 bg-gray-50 shadow rounded-lg">
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
