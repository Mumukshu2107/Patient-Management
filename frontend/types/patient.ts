export interface Patient {
  id: number;
  name: string;
  age: number;
  contact_no: string;
  height: number;
  weight: number;
  blood_group: string;
  status: number;
  current_hospital_id: number | null;
}