"use client";

import { useEffect, useState } from "react";
import api from "@/services/api";
import ProtectedRoute from "@/components/ProtectedRoute";
import BackToDashboard from "@/components/BackToDashboard";

interface Patient {
  id: number;
  name: string;
}

interface Hospital {
  id: number;
  name: string;
  city: string;
}

export default function AssignHospitalPage() {

  const [patients, setPatients] = useState<Patient[]>([]);
  const [hospitals, setHospitals] = useState<Hospital[]>([]);

  const [patientId, setPatientId] = useState("");
  const [hospitalId, setHospitalId] = useState("");

  useEffect(() => {
    fetchPatients();
    fetchHospitals();
  }, []);

  const fetchPatients = async () => {

    try {

      const response = await api.get("/patients");

      setPatients(response.data);

    } catch (error) {

      console.error(error);
    }
  };

  const fetchHospitals = async () => {

    try {

      const response = await api.get("/hospitals");

      setHospitals(response.data);

    } catch (error) {

      console.error(error);
    }
  };

  const handleAssign = async (
    e: React.FormEvent
  ) => {

    e.preventDefault();

    try {

      const response = await api.post(
        "/assign-hospital",
        {
          patient_id: Number(patientId),
          hospital_id: Number(hospitalId),
        }
      );

      alert(response.data.message);

      setPatientId("");
      setHospitalId("");

    } catch (error: any) {

      console.error(error);

      alert(
        error?.response?.data?.detail ||
        "Assignment failed"
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
          Assign Hospital
        </h1>
        

        <form
          onSubmit={handleAssign}
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
                Id: {patient.id}- {patient.name} 
              </option>

            ))}
          </select>

          <select
            value={hospitalId}
            onChange={(e) =>
              setHospitalId(e.target.value)
            }
            className="w-full border p-3 rounded"
            required
          >
            <option value="">
              Select Hospital
            </option>

            {hospitals.map((hospital) => (

              <option
                key={hospital.id}
                value={hospital.id}
              >
                Id {hospital.id}- {hospital.name} {hospital.city}
              </option>

            ))}
          </select>

          <button
            type="submit"
            className="bg-blue-700 text-white px-6 py-3 rounded"
          >
            Assign Hospital
          </button>

        </form>

      </div>
    </ProtectedRoute>
  );
}