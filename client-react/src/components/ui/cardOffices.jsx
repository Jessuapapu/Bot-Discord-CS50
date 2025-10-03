import { useState } from "react";
import UsersTableahora from "./usertableEstu";
import StaffTable from "./stafftable";

export default function JsonTabsOffices({ data }) {
  const [selectedTab, setSelectedTab] = useState("general");
  const [formData, setFormData] = useState(data);

  if (!data || Object.keys(data).length === 0) {
    return <div className="p-4 text-gray-400">Sin datos</div>;
  }

  return (
    <div className="p-6 border border-gray-700 rounded-lg shadow-md bg-gray-900 text-gray-200">
      {/* Tabs */}
      <div className="flex space-x-4 border-b border-gray-700 mb-4">
        {["general", "lista", "editar"].map((tab) => (
          <button
            key={tab}
            onClick={() => setSelectedTab(tab)}
            className={`px-4 py-2 capitalize transition-colors ${
              selectedTab === tab
                ? "border-b-2 border-blue-500 font-semibold text-blue-400"
                : "text-gray-400 hover:text-gray-200"
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* General */}
      {selectedTab === "general" && (
        <div className="space-y-2">
          {Object.entries(data).map(([key, value]) => {
            if (Array.isArray(value) || typeof value === "object") return null;
            return (
              <p key={key}>
                <span className="font-semibold text-blue-400">{key}:</span>{" "}
                {String(value)}
              </p>
            );
          })}
        </div>
      )}

      {/* Lista */}
      {selectedTab === "lista" && (
        <div className="space-y-6">
          {Object.entries(data).map(([key, value]) => {
            if (!Array.isArray(value)) return null;

            return (
              <div key={key}>
                <h3 className="font-bold text-lg text-blue-400 mb-2">{key}</h3>
                {key.toLowerCase() === "staff" ? (
                  <StaffTable
                    data={value}
                    onChange={(updated) =>
                      setFormData({ ...formData, staff: updated })
                    }
                  />
                ) : (
                  <UsersTableahora data={value || []} />
                )}
              </div>
            );
          })}
        </div>
      )}

      {/* Editar */}
      {selectedTab === "editar" && (
        <form
          className="space-y-4"
          onSubmit={(e) => {
            e.preventDefault();
            console.log("Datos guardados:", formData);
          }}
        >
          {Object.entries(formData).map(([key, value]) => {
            if (typeof value === "string" || typeof value === "number") {
              return (
                <div key={key}>
                  <label className="block capitalize text-gray-300 mb-1">
                    {key}
                  </label>
                  <input
                    type="text"
                    value={value}
                    onChange={(e) =>
                      setFormData({ ...formData, [key]: e.target.value })
                    }
                    className="border border-gray-600 bg-gray-800 text-gray-200 p-2 rounded w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              );
            }
            return null;
          })}

          <button
            type="submit"
            className="bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded transition-colors"
          >
            Guardar
          </button>
        </form>
      )}
    </div>
  );
}
