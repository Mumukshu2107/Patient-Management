import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-100">

      {/* Navbar */}
      <nav className="bg-blue-700 text-white px-8 py-4 flex justify-between items-center">
        <h1 className="text-2xl font-bold"> 
          HealthSphere Admin Portal
        </h1>

        <Link
          href="/login"
          className="bg-white text-blue-700 px-4 py-2 rounded"
        >
          Login
        </Link>
      </nav>

      {/* Hero Section */}
      <section className="text-center py-20 px-6">
        <h2 className="text-5xl font-bold text-blue-700 mb-6">
          HealthSphere Admin Portal
        </h2>

        <p className="text-xl text-gray-600 mb-10">
          Smart Healthcare Management System
        </p>

        <p className="max-w-3xl mx-auto text-gray-700">
          Manage patients, hospitals, admissions,
          discharges, uploads and healthcare
          operations from one centralized platform.
        </p>
      </section>

      {/* Feature Cards */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6 px-10 pb-20">

        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-xl font-semibold mb-2">
            Patient Management
          </h3>

          <p>
            Add, update and manage patient records.
          </p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-xl font-semibold mb-2">
            Hospital Management
          </h3>

          <p>
            Manage hospitals and assignments.
          </p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-xl font-semibold mb-2">
            CSV Operations
          </h3>

          <p>
            Upload and download patient data.
          </p>
        </div>

      </section>

    </main>
  );
}