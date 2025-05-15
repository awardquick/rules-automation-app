export type SectionHeaderProps = {
    title: string;
    color: 'primary' | 'success'; // 'primary' for purple, 'success' for green
  };

export type HeaderProps = {
    onCancel: () => void;
    onSave: () => void;
    onBack: () => void;
  };
