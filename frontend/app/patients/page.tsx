"use client";

import { useEffect, useState } from "react";
import api from "@/services/api";
import { Patient } from "@/types/patient";
import Link from "next/link";
import BackToDashboard from "@/components/BackToDashboard";

export default function PatientsPage() {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [searchBy, setSearchBy] =
    useState("name");

  const [searchText, setSearchText] =
    useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchPatients();
  }, []);

  const fetchPatients = async () => {
    try {
      const response = await api.get("/patients");
      setPatients(response.data);
    } catch (error) {
      console.error("Error fetching patients:", error);
    } finally {
      setLoading(false);
    }
  };

  const searchPatient = async () => {

    if (!searchText.trim()) {

      fetchPatients();

      return;
    }

    try {

      const response = await api.get(
        "/search/patient",
        {
          params: {
            search_by: searchBy,
            search_text: searchText,
          },
        }
      );

      if (response.data.patients) {

        setPatients(
          response.data.patients
        );
      }

    } catch (error) {

      console.error(error);

      alert("Search failed");
    }
  };

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto p-6">
        <h2 className="text-xl font-semibold">Loading patients...</h2>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto p-6">
      <BackToDashboard />

      <div className="bg-white rounded-lg shadow-lg p-6">

        <div className="flex justify-between items-center mb-6">

          <h1 className="text-3xl font-bold">
            Patients
          </h1>

          <div className="flex items-center gap-2">

            <select
              value={searchBy}
              onChange={(e) =>
                setSearchBy(e.target.value)
              }
              className="border rounded px-3 py-2"
            >
              <option value="name">
                Name
              </option>

              <option value="contact_no">
                Contact Number
              </option>
            </select>

            <input
              type="text"
              placeholder={
                searchBy === "name"
                  ? "Search patient name..."
                  : "Search contact number..."
              }
              value={searchText}
              onChange={(e) =>
                setSearchText(e.target.value)
              }
              className="border rounded px-3 py-2 w-64"
            />

            <button
              onClick={searchPatient}
              className="
        bg-blue-700
        text-white
        px-4
        py-2
        rounded
        hover:bg-blue-800
      "
            >
              🔍 Search
            </button>

          </div>

        </div>

        <div className="overflow-x-auto">
          <table className="w-full border border-gray-300">

            <thead>
              <tr className="bg-gray-100">
                <th className="border p-3">ID</th>
                <th className="border p-3">Name</th>
                <th className="border p-3">Age</th>
                <th className="border p-3">Contact No</th>
                <th className="border p-3">Blood Group</th>
                <th className="border p-3">Status</th>
                <th className="border p-3">History</th>
              </tr>
            </thead>

            <tbody>
              {patients.length > 0 ? (
                patients.map((patient) => (
                  <tr
                    key={patient.id}
                    className="hover:bg-gray-50"
                  >
                    <td className="border p-3">{patient.id}</td>
                    <td className="border p-3">{patient.name}</td>
                    <td className="border p-3">{patient.age}</td>
                    <td className="border p-3">
                      {patient.contact_no}
                    </td>
                    <td className="border p-3">
                      {patient.blood_group}
                    </td>
                    <td className="border p-3">
                      {patient.status === 1
                        ? "Admitted"
                        : "Discharged"}
                    </td>
                    <td className="border p-3">
                      <Link href={`/patients/${patient.id}/history`}
                        className="text-blue-600 underline">
                        View History
                      </Link>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td
                    colSpan={7}
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