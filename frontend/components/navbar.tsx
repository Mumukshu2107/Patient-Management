"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import api from "@/services/api";

export default function Navbar() {

  const [role, setRole] = useState("");
  const [openMenu, setOpenMenu] = useState("");

  const menuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetchUser();

    const handleClickOutside = (event: MouseEvent) => {

      if (
        menuRef.current &&
        !menuRef.current.contains(event.target as Node)
      ) {
        setOpenMenu("");
      }
    };

    document.addEventListener(
      "mousedown",
      handleClickOutside
    );

    return () => {
      document.removeEventListener(
        "mousedown",
        handleClickOutside
      );
    };

  }, []);

  const fetchUser = async () => {

    try {

      const response = await api.get("/me");

      setRole(response.data.role);

    } catch (error) {

      console.error(error);
    }
  };

  const toggleMenu = (menu: string) => {

    if (openMenu === menu) {
      setOpenMenu("");
    } else {
      setOpenMenu(menu);
    }
  };

  const logout = () => {

    localStorage.removeItem("token");

    window.location.href = "/";
  };

  return (

    <nav
      ref={menuRef}
      className="
        bg-blue-700
        text-white
        px-8
        py-4
        flex
        justify-between
        items-center
        shadow-md
      "
    >

      <div className="flex items-center gap-10">

        <h1 className="text-xl font-bold">
          HealthSphere Admin Portal
        </h1>

        <Link
          href="/dashboard"
          className="hover:text-blue-200"
        >
          Dashboard
        </Link>

        {/* PATIENTS */}

        <div className="relative">

          <button
            onClick={() =>
              toggleMenu("patients")
            }
            className="hover:text-blue-200"
          >
            Patients ▼
          </button>

          {openMenu === "patients" && (

            <div
              className="
                absolute
                top-full
                left-0
                mt-2
                w-56
                bg-white
                text-black
                rounded-md
                shadow-lg
                z-50
              "
            >

              <Link
                href="/patients"
                className="
                  block
                  px-4
                  py-3
                  hover:bg-gray-100
                "
              >
                View Patients
              </Link>

              {(role === "SUPER_ADMIN" ||
                role === "ADMIN" ||
                role === "RECEPTIONIST") && (

                <Link
                  href="/patients/new"
                  className="
                    block
                    px-4
                    py-3
                    hover:bg-gray-100
                  "
                >
                  Add Patient
                </Link>

              )}

              {(role === "SUPER_ADMIN" ||
                role === "ADMIN" ||
                role === "RECEPTIONIST") && (

                <Link
                  href="/assign-hospital"
                  className="
                    block
                    px-4
                    py-3
                    hover:bg-gray-100
                  "
                >
                  Admit Patient 
                </Link>

              )}

              {(role === "SUPER_ADMIN" ||
                role === "ADMIN" ||
                role === "RECEPTIONIST") && (

                <Link
                  href="/discharge"
                  className="
                    block
                    px-4
                    py-3
                    hover:bg-gray-100
                  "
                >
                  Discharge Patient
                </Link>

              )}

            </div>

          )}

        </div>

        {/* HOSPITALS */}

        <div className="relative">

          <button
            onClick={() =>
              toggleMenu("hospitals")
            }
            className="hover:text-blue-200"
          >
            Hospitals ▼
          </button>

          {openMenu === "hospitals" && (

            <div
              className="
                absolute
                top-full
                left-0
                mt-2
                w-56
                bg-white
                text-black
                rounded-md
                shadow-lg
                z-50
              "
            >

              <Link
                href="/hospitals"
                className="
                  block
                  px-4
                  py-3
                  hover:bg-gray-100
                "
              >
                View Hospitals
              </Link>

              {(role === "SUPER_ADMIN" ||
                role === "ADMIN") && (

                <Link
                  href="/hospitals/new"
                  className="
                    block
                    px-4
                    py-3
                    hover:bg-gray-100
                  "
                >
                  Add Hospital
                </Link>

              )}

            </div>

          )}

        </div>

        {/* DOCUMENTS */}

        {(role === "SUPER_ADMIN" ||
          role === "ADMIN") && (

          <div className="relative">

            <button
              onClick={() =>
                toggleMenu("documents")
              }
              className="hover:text-blue-200"
            >
              Documents ▼
            </button>

            {openMenu === "documents" && (

              <div
                className="
                  absolute
                  top-full
                  left-0
                  mt-2
                  w-56
                  bg-white
                  text-black
                  rounded-md
                  shadow-lg
                  z-50
                "
              >

                <Link
                  href="/upload"
                  className="
                    block
                    px-4
                    py-3
                    hover:bg-gray-100
                  "
                >
                  Upload Documents
                </Link>

                <Link
                  href="/download"
                  className="
                    block
                    px-4
                    py-3
                    hover:bg-gray-100
                  "
                >
                  Download Documents
                </Link>

              </div>

            )}

          </div>

        )}

        {/* ADMINISTRATION */}

        {role === "SUPER_ADMIN" && (

          <div className="relative">

            <button
              onClick={() =>
                toggleMenu("admin")
              }
              className="hover:text-blue-200"
            >
              Administration ▼
            </button>

            {openMenu === "admin" && (

              <div
                className="
                  absolute
                  top-full
                  left-0
                  mt-2
                  w-56
                  bg-white
                  text-black
                  rounded-md
                  shadow-lg
                  z-50
                "
              >

                <Link
                  href="/users"
                  className="
                    block
                    px-4
                    py-3
                    hover:bg-gray-100
                  "
                >
                  Manage Users
                </Link>

              </div>

            )}

          </div>

        )}

      </div>

      {/* RIGHT SIDE */}

      <div className="flex items-center gap-4">

        <span
          className="
            bg-white
            text-blue-700
            px-3
            py-1
            rounded-full
            text-sm
            font-semibold
          "
        >
          {role}
        </span>

        <Link
          href="/profile"
          className="hover:text-blue-200"
        >
          Profile
        </Link>

        <button
          onClick={logout}
          className="
            bg-red-500
            hover:bg-red-600
            px-4
            py-2
            rounded
          "
        >
          Logout
        </button>

      </div>

    </nav>
  );
}