document.getElementById("pipelineForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const button = e.target.querySelector("button");
  button.disabled = true;
  button.textContent = "מריץ...";

  const profile = {
    business_name: document.getElementById("business_name").value,
    area_sqm: parseInt(document.getElementById("area_sqm").value),
    num_seats: parseInt(document.getElementById("num_seats").value),
    uses_gas: document.getElementById("uses_gas").value === "true",
    delivers: document.getElementById("delivers").value === "true",
    has_meat: document.getElementById("has_meat").value === "true",
    uses_fryer: document.getElementById("uses_fryer").value === "true",
    has_alcohol: document.getElementById("has_alcohol").value === "true",
    serves_dairy: document.getElementById("serves_dairy").value === "true",
    has_seating: document.getElementById("has_seating").value === "true",
    is_open_air: document.getElementById("is_open_air").value === "true",
    uses_gas_grill: document.getElementById("uses_gas_grill").value === "true",
    is_kosher: document.getElementById("is_kosher").value === "true"
  };

  const payload = {
    profile: profile,
    source_doc_path: "data/rew/18-07-2022_4.2A.pdf",
    output_dir: "output/"
  };

  try {
    const response = await fetch("http://127.0.0.1:8000/api/v1/pipeline/run_json", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await response.json();
    document.getElementById("result").innerHTML =
      data.status === "success"
        ? `<h2>✅ דוח נוצר בהצלחה</h2><pre style="white-space: pre-wrap; text-align:right;">${data.report_text}</pre>`
        : `<p style="color:red;">❌ שגיאה: ${data.detail || JSON.stringify(data)}</p>`;
  } catch (err) {
    document.getElementById("result").innerText = "⚠️ שגיאה בחיבור לשרת: " + err;
  } finally {
    button.disabled = false;
    button.textContent = "הרץ פייפליין";
  }
});
