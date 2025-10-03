import { useEffect, useState } from "react"
import JsonTabsOffices from "../components/ui/cardOffices"

const connectionString = 'http://localhost:10000'



export default function Home() {
  const [dataOfficesActivas, setDataOfficesActivas] = useState(null)
  const [dataOfficesRevision, setDataOfficesRevision] = useState(null)




  useEffect(() => {
    fetch(connectionString + "/api/OhActivas")
      .then((res) => res.json())
      .then((data) => {
        // Guardamos todo el objeto de offices
        setDataOfficesActivas(data)
      })
      .catch((err) => console.error("Error en fetch:", err))
  }, [])

  useEffect(() => {
    fetch(connectionString + "/api/OhRevision")
      .then((res) => res.json())
      .then((data) => {
        setDataOfficesRevision(data)
      })
      .catch((err) => console.error("Error en fetch:", err))
  }, [])

  return (
    <>
      <div className="p-6 space-y-6">
        <h2 className="text-2xl font-bold mb-4">Offices activas</h2>

        {dataOfficesActivas ? (
          Object.entries(dataOfficesActivas).map(([key, officeData]) => (
            <JsonTabsOffices key={key} data={officeData} />
          ))
        ) : (
          <p> No se encuentran disponlibles (‾◡◝) </p>
        )}
      </div>

      <div className="p-6 space-y-6">
        <h2 className="text-2xl font-bold mb-4">Offices activas</h2>

        {dataOfficesRevision ? (
          Object.entries(dataOfficesRevision).map(([key, officeData]) => (
            <JsonTabsOffices key={key} data={officeData} />
          ))
        ) : (
          <p>No se encuentran disponlibles (‾◡◝)</p>
        )}
      </div>
    </>
  )
}
