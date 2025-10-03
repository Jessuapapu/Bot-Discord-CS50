import { useState } from "react";

// Genera la URL de la imagen según staff
const getStaffImage = (staff) => {
  return `https://code-fu.net.ni/wp-content/uploads/2025/07/${staff}-001.webp`;
};

export default function StaffTable({ data = [], onChange }) {
  const [search, setSearch] = useState("");
  const [staffList, setStaffList] = useState(data);
  const [selectedStaff, setSelectedStaff] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);

  // Filtrado
  const filteredStaff = staffList.filter((staff) =>
    staff.toLowerCase().includes(search.toLowerCase())
  );

  const openModal = (staff, index) => {
    setSelectedStaff({ name: staff, index });
    setModalOpen(true);
  };

  const closeModal = () => {
    setSelectedStaff(null);
    setModalOpen(false);
  };

  const handleSave = (e) => {
    e.preventDefault();
    const updated = [...staffList];
    updated[selectedStaff.index] = selectedStaff.name.trim();
    setStaffList(updated);
    onChange?.(updated);
    closeModal();
  };

  const handleDelete = (index) => {
    const updated = staffList.filter((_, i) => i !== index);
    setStaffList(updated);
    onChange?.(updated);
  };

  return (
    <div className="relative overflow-x-auto shadow-md sm:rounded-lg">
      {/* Toolbar */}
      <div className="flex flex-col md:flex-row items-center justify-between py-4 px-4 bg-gray-900 space-y-4 md:space-y-0">
        <input
          type="text"
          placeholder="Buscar staff..."
          className="block w-80 text-sm text-white bg-gray-700 border border-gray-600 rounded-lg pl-10 pr-3 py-2 focus:ring-blue-500 focus:border-blue-500"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      {/* Tabla */}
      <table className="w-full text-sm text-left text-gray-400">
        <thead className="text-xs text-gray-400 uppercase bg-gray-800">
          <tr>
            <th className="px-6 py-3">Avatar</th>
            <th className="px-6 py-3">Código</th>
            <th className="px-6 py-3">Acciones</th>
          </tr>
        </thead>
        <tbody>
          {filteredStaff.length > 0 ? (
            filteredStaff.map((staff, index) => (
              <tr
                key={index}
                className="bg-gray-800 border-b border-gray-700 hover:bg-gray-700"
              >
                <td className="px-6 py-4">
                  <img
                    src={getStaffImage(staff)}
                    alt={staff}
                    className="w-10 h-10 rounded-full"
                    onError={(e) => {
                      // Si falla 2025/07 → intenta con 2024/01
                      e.currentTarget.onerror = null;
                      e.currentTarget.src = `https://code-fu.net.ni/wp-content/uploads/2024/01/${staff}-001.webp`;
                    }}
                  />
                </td>
                <td className="px-6 py-4">{staff}</td>
                <td className="px-6 py-4 space-x-2">
                  <button
                    className="text-blue-500 hover:underline"
                    onClick={() => openModal(staff, index)}
                  >
                    Editar
                  </button>
                  <button
                    className="text-red-500 hover:underline"
                    onClick={() => handleDelete(index)}
                  >
                    Eliminar
                  </button>
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan={3} className="text-center py-4 text-gray-500">
                No hay staff disponible
              </td>
            </tr>
          )}
        </tbody>
      </table>

      {/* Modal de edición */}
      {modalOpen && selectedStaff && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
          <form
            className="bg-gray-800 text-white rounded-lg p-6 w-full max-w-2xl"
            onSubmit={handleSave}
          >
            <h3 className="text-xl font-semibold mb-4">Editar Staff</h3>
            <div className="flex flex-col">
              <label className="mb-1">Código</label>
              <input
                type="text"
                value={selectedStaff.name}
                onChange={(e) =>
                  setSelectedStaff({ ...selectedStaff, name: e.target.value })
                }
                className="rounded px-3 py-2 bg-gray-700 border border-gray-600 text-white"
              />
            </div>
            <div className="flex justify-end mt-6 space-x-2">
              <button
                type="button"
                className="px-4 py-2 rounded bg-gray-600 hover:bg-gray-500"
                onClick={closeModal}
              >
                Cancelar
              </button>
              <button
                type="submit"
                className="px-4 py-2 rounded bg-blue-600 hover:bg-blue-500"
              >
                Guardar
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
}
