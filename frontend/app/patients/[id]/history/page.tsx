"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import api from "@/services/api";

interface HospitalHistory {
  hospital_id: number;
  hospital_name: string;
  hospital_city: string;
  status: number;
  admit_time: string;
  discharge_time: string;
}

interface PatientHistoryResponse {
  patient_id: number;
  patient_name: string;
  hospital_history: HospitalHistory[];
}

export default function PatientHistoryPage() {

  const params = useParams();
  const router = useRouter();

  const patientId = params.id;

  const [history, setHistory] =
    useState<PatientHistoryResponse | null>(null);

  const [loading, setLoading] =
    useState(true);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {

    try {

      const response = await api.get(
        `/patients/${patientId}/hospitals`
      );

      setHistory(response.data);

    } catch (error) {

      console.error(
        "Error fetching patient history:",
        error
      );

    } finally {

      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto p-6">

        <button
          onClick={() => router.push("/patients")}
          className="
            mb-6
            flex
            items-center
            gap-2
            bg-gray-200
            hover:bg-gray-300
            px-4
            py-2
            rounded
            font-medium
          "
        >
          ← Back to Patients
        </button>

        <h2 className="text-xl font-semibold">
          Loading history...
        </h2>

      </div>
    );
  }

  if (!history) {
    return (
      <div className="max-w-7xl mx-auto p-6">

        <button
          onClick={() => router.push("/patients")}
          className="
            mb-6
            flex
            items-center
            gap-2
            bg-gray-200
            hover:bg-gray-300
            px-4
            py-2
            rounded
            font-medium
          "
        >
          ← Back to Patients
        </button>

        <h2 className="text-xl font-semibold text-red-600">
          Patient history not found
        </h2>

      </div>
    );
  }

  return (

    <div className="max-w-7xl mx-auto p-6">

      <button
        onClick={() => router.push("/patients")}
        className="
          mb-6
          flex
          items-center
          gap-2
          bg-gray-200
          hover:bg-gray-300
          px-4
          py-2
          rounded
          font-medium
        "
      >
        ← Back
      </button>

      <div className="bg-white rounded-lg shadow-lg p-6">

        <h1 className="text-3xl font-bold mb-2">
          Patient Hospital History
        </h1>

        <p className="text-gray-600 mb-6">
          Patient ID: {history.patient_id}
        </p>

        <p className="text-lg font-medium mb-6">
          Patient Name: {history.patient_name}
        </p>

        <div className="overflow-x-auto">

          <table className="w-full border border-gray-300">

            <thead>

              <tr className="bg-gray-100">

                <th className="border p-3">
                  Hospital ID
                </th>

                <th className="border p-3">
                  Hospital Name
                </th>

                <th className="border p-3">
                  City
                </th>

                <th className="border p-3">
                  Status
                </th>

                <th className="border p-3">
                  Admit Time
                </th>

                <th className="border p-3">
                  Discharge Time
                </th>

              </tr>

            </thead>

            <tbody>

              {history.hospital_history.length > 0 ? (

                history.hospital_history.map(
                  (record) => (

                    <tr
                      key={`${record.hospital_id}-${record.admit_time}`}
                      className="hover:bg-gray-50"
                    >

                      <td className="border p-3">
                        {record.hospital_id}
                      </td>

                      <td className="border p-3">
                        {record.hospital_name}
                      </td>

                      <td className="border p-3">
                        {record.hospital_city}
                      </td>

                      <td className="border p-3">

                        {record.status === 1
                          ? "Currently Admitted"
                          : "Discharged"}

                      </td>

                      <td className="border p-3">
                        {record.admit_time}
                      </td>

                      <td className="border p-3">
                        {record.discharge_time}
                      </td>

                    </tr>
                  )
                )

              ) : (

                <tr>

                  <td
                    colSpan={6}
                    className="text-center p-4"
                  >
                    No hospital history found
                  </td>

                </tr>

              )}

            </tbody>

          </table>

        </div>

      </div>

    </div>
  );
}