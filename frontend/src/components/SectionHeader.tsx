import type { SectionHeaderProps } from "../types/generic";
import { Play } from "lucide-react";
const colorMap = {
  primary: "#755DC8",
  success: "#28A745",
};

const SectionHeader: React.FC<SectionHeaderProps> = ({ title, color }) => (
  <div className="flex items-center w-full border-b border-gray-300 p-6">
    <div
      className="flex items-center justify-center w-6 h-6 rounded-full mr-2"
      style={{ backgroundColor: colorMap[color] }}
    >
      <Play className="text-white fill-white" size={14} strokeWidth={2} />
    </div>
    <h2 className="text-xl font-semibold text-gray-700">{title}</h2>
  </div>
);

export default SectionHeader;
