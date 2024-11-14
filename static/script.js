document.getElementById("predictionForm").addEventListener("submit", function (e) {
    e.preventDefault();
  
    const data = {
      age: document.getElementById("age").value,
      job_satisfaction: document.getElementById("jobSatisfaction").value,
      years_at_company: document.getElementById("yearsAtCompany").value,
      job_level: document.getElementById("jobLevel").value,
      monthly_income: document.getElementById("monthlyIncome").value,
      total_working_years: document.getElementById("totalWorkingYears").value,
      years_since_last_promotion: document.getElementById("yearsSinceLastPromotion").value,
      overtime: document.getElementById("overtime").value
    };
  
    fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    })
      .then(response => response.json())
      .then(data => {
        const resultModal = document.getElementById("resultModal");
        const modalMessage = document.getElementById("modalMessage");
  
        if (data.prediction === "Yes") {
          modalMessage.innerHTML = "Employee is likely to leave. <span class='sad-emoji'>&#128542;</span>";
        } else {
          modalMessage.innerHTML = "Employee is likely to stay. <span class='happy-emoji'>&#128516;</span>";
        }
  
        resultModal.style.display = "block";
      })
      .catch(error => console.error("Error:", error));
  });
  
  document.querySelector(".close-btn").onclick = function() {
    document.getElementById("resultModal").style.display = "none";
  };
  
  window.onclick = function(event) {
    if (event.target == document.getElementById("resultModal")) {
      document.getElementById("resultModal").style.display = "none";
    }
  };
  