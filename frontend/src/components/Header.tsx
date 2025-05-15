import { ArrowLeft } from "lucide-react";

interface HeaderProps {
  onCancel: () => void;
  onSave: () => void;
  onBack: () => void;
  isSaving?: boolean;
}

const Header: React.FC<HeaderProps> = ({
  onCancel,
  onSave,
  onBack,
  isSaving = false,
}) => {
  return (
    <header className="flex justify-between items-center w-full p-6 bg-white border-b border-gray-200">
      {/* Left Section: Back Arrow and Title */}
      <div className="flex items-center gap-2">
        <button onClick={onBack}>
          <ArrowLeft className="text-gray-400 cursor-pointer" size={16} />
        </button>
        <h1 className="text-xl font-semibold text-gray-800">Advanced</h1>
      </div>

      {/* Right Section: Action Buttons */}
      <div className="flex items-center gap-4">
        <button
          onClick={onCancel}
          className="text-gray-700 border border-gray-300 px-4 py-2 rounded hover:bg-gray-100"
        >
          Cancel
        </button>
        <button
          onClick={onSave}
          disabled={isSaving}
          className="text-white bg-[#755DC8] px-4 py-2 rounded hover:bg-[#6849C2] disabled:opacity-50"
        >
          {isSaving ? "Saving..." : "Save and Enable Rule"}
        </button>
      </div>
    </header>
  );
};

export default Header;
