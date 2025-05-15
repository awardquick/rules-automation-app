import { Info } from "lucide-react";

const ConditionFooter = ({
  matchingApplicants,
}: {
  matchingApplicants: number;
}) => {
  return (
    <div className="flex items-center w-[1168px] h-12 p-3 pl-[26px] pr-6 gap-4 border-t border-gray-300 rounded-b bg-neutralBg shadow-inner-custom">
      <div className="flex items-center justify-center w-3 h-3 rounded-full bg-gray-400">
        <Info className="text-white" size={12} strokeWidth={2} />
      </div>
      <p className="text-gray-500 text-sm">
        Given conditions match with{" "}
        <span className="font-semibold text-gray-700">
          {matchingApplicants} existing applicants.
        </span>
      </p>
    </div>
  );
};

export default ConditionFooter;
