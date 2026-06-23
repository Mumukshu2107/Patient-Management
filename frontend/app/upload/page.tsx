"use client";

import { useState } from "react";
import api from "@/services/api";
import BackToDashboard from "@/components/BackToDashboard";

export default function UploadPage() {

  const [entityType, setEntityType] =
    useState("patient");

  const [file, setFile] =
    useState<File | null>(null);

  const [message, setMessage] =
    useState("");

  const handleUpload = async (
    e: React.FormEvent
  ) => {

    e.preventDefault();

    if (!file) {

      alert("Please select a CSV file");

      return;
    }

    try {

      const formData = new FormData();

      formData.append(
        "entity_type",
        entityType
      );

      formData.append(
        "file",
        file
      );

      const response = await api.post(
        "/upload-data",
        formData,
        {
          headers: {
            "Content-Type":
              "multipart/form-data",
          },
        }
      );

      setMessage(
        response.data.message
      );

      alert(
        `${response.data.records_inserted} records uploaded successfully`
      );

    } catch (error) {

      console.error(error);

      alert("Upload failed");
    }
  };

  return (

    <div className="max-w-3xl mx-auto p-8">
        <BackToDashboard />

      <div className="bg-white p-8 rounded-lg shadow">

        <h1 className="text-3xl font-bold mb-6">
          Upload Data
        </h1>
        

        <form
          onSubmit={handleUpload}
          className="space-y-6"
        >

          <div>

            <label className="block mb-2 font-medium">
              Upload Type
            </label>

            <select
              value={entityType}
              onChange={(e) =>
                setEntityType(
                  e.target.value
                )
              }
              className="w-full border p-3 rounded"
            >

              <option value="patient">
                Upload Patients
              </option>

              <option value="hospital">
                Upload Hospitals
              </option>

            </select>

          </div>

          <div>

            <label className="block mb-2 font-medium">
              CSV File
            </label>

            <input
              type="file"
              accept=".csv"
              onChange={(e) =>
                setFile(
                  e.target.files?.[0] || null
                )
              }
              className="w-full border p-3 rounded"
            />

          </div>

          <button
            type="submit"
            className="
              bg-blue-700
              text-white
              px-6
              py-3
              rounded
            "
          >
            Upload
          </button>

        </form>

        {message && (

          <div className="mt-6 text-green-600 font-medium">
            {message}
          </div>

        )}

      </div>

    </div>
  );
}