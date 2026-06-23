"use client";

import api from "@/services/api";
import BackToDashboard from "@/components/BackToDashboard";

export default function DownloadPage() {

  const downloadFile = async (
    type: string
  ) => {

    try {

      const response = await api.get(
        `/download/${type}s`,
        {
          responseType: "blob",
        }
      );

      const blob = new Blob(
        [response.data],
        {
          type: "text/csv",
        }
      );

      const url =
        window.URL.createObjectURL(
          blob
        );

      const link =
        document.createElement("a");

      link.href = url;

      link.download =
        `${type}s.csv`;

      document.body.appendChild(
        link
      );

      link.click();

      link.remove();

    } catch (error) {

      console.error(error);

      alert(
        `Failed to download ${type}s`
      );
    }
  };

  return (

    <div className="max-w-3xl mx-auto p-8">
        <BackToDashboard />

      <div className="bg-white p-8 rounded-lg shadow">

        <h1 className="text-3xl font-bold mb-6">
          Download 
        </h1>
        

        <div className="space-y-4">

          <button
            onClick={() =>
              downloadFile(
                "patient"
              )
            }
            className="
              w-full
              bg-blue-700
              text-white
              p-4
              rounded
            "
          >
            Download Patients CSV
          </button>

          <button
            onClick={() =>
              downloadFile(
                "hospital"
              )
            }
            className="
              w-full
              bg-green-700
              text-white
              p-4
              rounded
            "
          >
            Download Hospitals CSV
          </button>

        </div>

      </div>

    </div>
  );
}