console.log("JS connected");

const form = document.getElementById("loanForm");
const resultDiv = document.getElementById("result");
function num(id) {
    const v = document.getElementById(id).value;
    return v === "" ? 0 : Number(v);
}

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    resultDiv.className = "result hidden";

    const payload = {
    Gender: document.getElementById("Gender").value,
    Married: document.getElementById("Married").value,
    Dependents: num("Dependents"),
    Education: document.getElementById("Education").value,
    Self_Employed: document.getElementById("Self_Employed").value,
    ApplicantIncome: num("ApplicantIncome"),
    CoapplicantIncome: num("CoapplicantIncome"),
    LoanAmount: num("LoanAmount"),
    Loan_Amount_Term: num("Loan_Amount_Term"),
    Credit_History: num("Credit_History"),
    Property_Area: document.getElementById("Property_Area").value
};


    console.log("Payload sent to API:", payload);

    try {
        const response = await fetch("https://loan-approval-prediction-model-glos.onrender.com/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        console.log("API response:", data);

        let status;
        if (data.prediction === 1 || data.prediction === "Loan Approved") {
            status = "Loan Approved ✅";
            resultDiv.classList.add("success");
        } else {
            status = "Loan Not Approved ❌";
            resultDiv.classList.add("error");
        }

        resultDiv.classList.remove("hidden");
        resultDiv.innerText = status;

    } catch (err) {
        console.error(err);
        resultDiv.classList.remove("hidden");
        resultDiv.classList.add("error");
        resultDiv.innerText = "Prediction failed. Check backend.";
    }
});
console.log("JS LOADED");
