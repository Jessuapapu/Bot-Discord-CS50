import { useState, useEffect } from "react";

import { io } from "socket.io-client";

const socket = io('http://localhost:10000/', {
  transports: ["websocket"],})


export default function UsersTable({ data }) {
  const [search, setSearch] = useState("");
  const [selectedUser, setSelectedUser] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);
  // Making the socket instance


  useEffect(() => {
    console.log("Socket ID (cliente):", socket.id);

    socket.on("connect", () => {
      console.log("Conectado al servidor con id:", socket.id);
    });

    socket.on("connected", (data) => {
      console.log('pipi')
      console.log("Evento connected recibido:", data);
    });

    socket.on("response", (data) => {
      console.log("Respuesta del servidor:", data);
    });
  });

  // Filtrado por búsqueda
  const filteredData = data.filter((user) =>
    Object.values(user)
      .join(" ")
      .toLowerCase()
      .includes(search.toLowerCase())
  );

  const openModal = (user) => {
    setSelectedUser(user);
    setModalOpen(true);
  };

  const closeModal = () => {
    setSelectedUser(null);
    setModalOpen(false);
  };

  const handleSave = (e) => {
    e.preventDefault();
    console.log("Datos guardados:", selectedUser);
    closeModal();
  };

  return (
    <div className="relative overflow-x-auto shadow-md sm:rounded-lg">
      {/* Toolbar */}
      <div className="flex flex-col md:flex-row items-center justify-between py-4 px-4 bg-gray-900 space-y-4 md:space-y-0">
        <input
          type="text"
          placeholder="Buscar usuario..."
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
            <th className="px-6 py-3">IdUsuario</th>
            <th className="px-6 py-3">IdDiscord</th>
            <th className="px-6 py-3">Grupo</th>
            <th className="px-6 py-3">IdOffice</th>
            <th className="px-6 py-3">TiempoTotal</th>
            <th className="px-6 py-3">CumplimientoReal</th>
            <th className="px-6 py-3">Acciones</th>
          </tr>
        </thead>
        <tbody>
          {filteredData.map((user) => (
            <tr
              key={user.IdUsuario}
              className="bg-gray-800 border-b border-gray-700 hover:bg-gray-700"
            >
              <td className="px-6 py-4">
                <img
                  src={user.avatar}
                  alt="Avatar"
                  className="w-10 h-10 rounded-full"
                />
              </td>
              <td className="px-6 py-4">{user.IdUsuario}</td>
              <td className="px-6 py-4">{user.IdDiscord}</td>
              <td className="px-6 py-4">{user.grupo}</td>
              <td className="px-6 py-4">{user.IdOffice}</td>
              <td className="px-6 py-4">{user.TiempoTotal}</td>
              <td className="px-6 py-4">{user.cumplimientoReal}</td>
              <td className="px-6 py-4">
                <button
                  className="text-blue-500 hover:underline"
                  onClick={() => openModal(user)}
                >
                  Editar
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Modal de edición */}
      {modalOpen && selectedUser && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
          <form
            className="bg-gray-800 text-white rounded-lg p-6 w-full max-w-2xl"
            onSubmit={handleSave}
          >
            <h3 className="text-xl font-semibold mb-4">Editar Usuario</h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {Object.entries(selectedUser).map(([key, value]) => {
                if (key === "avatar") return null; // no editar avatar
                return (
                  <div key={key} className="flex flex-col">
                    <label className="mb-1">{key}</label>
                    <input
                      type="text"
                      value={value}
                      onChange={(e) =>
                        setSelectedUser({
                          ...selectedUser,
                          [key]: e.target.value,
                        })
                      }
                      className="rounded px-3 py-2 bg-gray-700 border border-gray-600 text-white"
                    />
                  </div>
                );
              })}
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
