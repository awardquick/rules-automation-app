export type ApplicationCreate = {
  applicantName: string;
  applicantEmail: string;
  familyStatus: string;
  businessOwner: boolean;
  filedUsTaxes: boolean;
  taxYear: number;
  submittedAt?: string;
};

export type ApplicationResponse = {
  id: number;
  applicantName: string;
  applicantEmail: string;
  familyStatus: string;
  businessOwner: boolean;
  filedUsTaxes: boolean;
  taxYear: number;
  submittedAt: string;
  createdAt: string;
  updatedAt: string;
};