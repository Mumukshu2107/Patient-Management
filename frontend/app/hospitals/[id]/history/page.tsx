"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import api from "@/services/api";

interface PatientHistory {
  id: number;
  name: string;
  age: number;
  blood_group: string;
  status: number;
}

interface HospitalPatientResponse {
  hospital_id: number;
  hospital_name: string;
  city: string;
  patients: PatientHistory[];
}

export default function HospitalHistoryPage() {

  const params = useParams();
  const router = useRouter();

  const hospitalId = params.id;

  const [history, setHistory] =
    useState<HospitalPatientResponse | null>(null);

  const [loading, setLoading] =
    useState(true);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {

    try {

      const response = await api.get(
        `/hospitals/${hospitalId}/patients`
      );

      setHistory(response.data);

    } catch (error) {

      console.error(
        "Error fetching hospital history:",
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
          onClick={() => router.push("/hospitals")}
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
          ← Back to Hospitals
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
          onClick={() => router.push("/hospitals")}
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
          ← Back to Hospitals
        </button>

        <h2 className="text-xl font-semibold text-red-600">
          Hospital history not found
        </h2>

      </div>
    );
  }

  return (

    <div className="max-w-7xl mx-auto p-6">

      <button
        onClick={() => router.push("/hospitals")}
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
          Hospital Patient History
        </h1>

        <p className="text-gray-600 mb-6">
          Hospital ID: {history.hospital_id}
        </p>

        <p className="text-lg font-medium mb-6">
          Hospital Name: {history.hospital_name}
        </p>

        <p className="text-lg font-medium mb-6">
          City: {history.city}
        </p>

        <div className="overflow-x-auto">

          <table className="w-full border border-gray-300">

            <thead>

              <tr className="bg-gray-100">

                <th className="border p-3">
                  Patient ID
                </th>

                <th className="border p-3">
                  Patient Name
                </th>

                <th className="border p-3">
                  Age
                </th>

                <th className="border p-3">
                  Blood Group
                </th>

                <th className="border p-3">
                  Status
                </th>

              </tr>

            </thead>

            <tbody>

              {history.patients.length > 0 ? (

                history.patients.map((patient) => (

                  <tr
                    key={patient.id}
                    className="hover:bg-gray-50"
                  >

                    <td className="border p-3">
                      {patient.id}
                    </td>

                    <td className="border p-3">
                      {patient.name}
                    </td>

                    <td className="border p-3">
                      {patient.age}
                    </td>

                    <td className="border p-3">
                      {patient.blood_group}
                    </td>

                    <td className="border p-3">

                      {patient.status === 1
                        ? "Admitted"
                        : "Discharged"}

                    </td>

                  </tr>

                ))

              ) : (

                <tr>

                  <td
                    colSpan={5}
                    className="text-center p-4"
                  >
                    No patients found
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