async function sendTask() {
    const task = document.getElementById("task").value;
    const box = document.getElementById("responseBox");

    if (!task.trim()) {
        box.innerHTML = "Please enter a task!";
        box.classList.remove("hidden");
        return;
    }

    box.innerHTML = "Processing...";
    box.classList.remove("hidden");

    const res = await fetch("https://llm-analysis-quiz-8-znsv.onrender.com/quiz", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ task })
    });

    const data = await res.json();
    box.innerHTML = "<b>Response:</b><br><br>" + data.answer;
}
