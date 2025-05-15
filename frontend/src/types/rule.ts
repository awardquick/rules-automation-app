export type Condition = { field: string };
export type Action = { documentType: string; description: string };


export type RuleContextType = {
    conditions: Condition[];
    actions: Action[];
    addCondition: (condition: Condition) => void;
    addAction: (action: Action) => void;
};

export type SectionHeaderProps = {
    title: string;
    color: 'primary' | 'success'; // 'primary' for purple, 'success' for green
  };

export type HeaderProps = {
    onCancel: () => void;
    onSave: () => void;
    onBack: () => void;
  };
  