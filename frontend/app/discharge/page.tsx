"use client";

import { useEffect, useState } from "react";
import api from "@/services/api";
import ProtectedRoute from "@/components/ProtectedRoute";
import BackToDashboard from "@/components/BackToDashboard";

interface Patient {
  id: number;
  name: string;
  status: number;
}

export default function DischargePatientPage() {

  const [patients, setPatients] = useState<Patient[]>([]);
  const [patientId, setPatientId] = useState("");

  useEffect(() => {
    fetchPatients();
  }, []);

  const fetchPatients = async () => {

    try {

      const response = await api.get("/patients");

      const admittedPatients = response.data.filter(
        (patient: Patient) => patient.status === 1
      );

      setPatients(admittedPatients);

    } catch (error) {

      console.error(error);
    }
  };

  const handleDischarge = async (
    e: React.FormEvent
  ) => {

    e.preventDefault();

    try {

      const response = await api.post(
        `/patients/${patientId}/discharge`
      );

      alert(response.data.message);

      setPatientId("");

      fetchPatients();

    } catch (error: any) {

      console.error(error);

      alert(
        error?.response?.data?.detail ||
        "Discharge failed"
      );
    }
  };

  return (
    <ProtectedRoute
      allowedRoles={[
        "SUPER_ADMIN",
        "ADMIN",
        "RECEPTIONIST",
      ]}
    >
      <div className="max-w-2xl mx-auto p-8">
        <BackToDashboard />

        <h1 className="text-3xl font-bold mb-6">
          Discharge Patient
        </h1>

        <form
          onSubmit={handleDischarge}
          className="space-y-4"
        >

          <select
            value={patientId}
            onChange={(e) =>
              setPatientId(e.target.value)
            }
            className="w-full border p-3 rounded"
            required
          >
            <option value="">
              Select Patient
            </option>

            {patients.map((patient) => (

              <option
                key={patient.id}
                value={patient.id}
              >
                ID: {patient.id}-{patient.name} 
              </option>

            ))}
          </select>

          <button
            type="submit"
            className="bg-red-600 text-white px-6 py-3 rounded"
          >
            Discharge Patient
          </button>

        </form>

      </div>
    </ProtectedRoute>
  );
}