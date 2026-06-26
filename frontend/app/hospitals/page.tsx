"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import api from "@/services/api";
import { Hospital } from "@/types/hospital";
import BackToDashboard from "@/components/BackToDashboard";
import Link from "next/link";

export default function HospitalsPage() {
  const [hospitals, setHospitals] =
    useState<Hospital[]>([]);

  const [loading, setLoading] =
    useState(true);

  const router = useRouter();

  useEffect(() => {
    fetchHospitals();
  }, []);

  const fetchHospitals = async () => {
    try {
      const response = await api.get(
        "/hospitals"
      );

      setHospitals(response.data);

    } catch (error) {

      console.error(
        "Error fetching hospitals:",
        error
      );

    } finally {

      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto p-6">

        <h2 className="text-xl font-semibold">
          Loading hospitals...
        </h2>

      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto p-6">

      <BackToDashboard />

      <div className="bg-white rounded-lg shadow-lg p-6">

        <h1 className="text-3xl font-bold mb-6">
          Hospitals
        </h1>

        <div className="overflow-x-auto">

          <table className="w-full border border-gray-300">

            <thead>

              <tr className="bg-gray-100">

                <th className="border p-3">
                  ID
                </th>

                <th className="border p-3">
                  Hospital Name
                </th>

                <th className="border p-3">
                  City
                </th>

                <th className="border p-3">
                  Patient Visit
                </th>

              </tr>

            </thead>

            <tbody>

              {hospitals.length > 0 ? (

                hospitals.map((hospital) => (

                  <tr
                    key={hospital.id}
                    className="hover:bg-gray-50"
                  >

                    <td className="border p-3">
                      {hospital.id}
                    </td>

                    <td className="border p-3">
                      {hospital.name}
                    </td>

                    <td className="border p-3">
                      {hospital.city}
                    </td>

                    <td className="border p-3">
                      <Link href={`/hospitals/${hospital.id}/history`}
                      className="text-blue-600 underline">
                        History                
                      </Link>

                    </td>

                  </tr>

                ))

              ) : (

                <tr>

                  <td
                    colSpan={4}
                    className="text-center p-4"
                  >
                    No hospitals found
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