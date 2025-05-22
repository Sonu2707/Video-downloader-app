function toggleTheme() {
    document.body.classList.toggle("dark");
}
async function startDownload() {
    const url = document.getElementById("urlInput").value;
    const quality = document.getElementById("quality").value;
    const progressBar = document.getElementById("progressBar");
    progressBar.style.display = "block";
    progressBar.value = 20;

    const res = await fetch("https://video-downloader-app-ub63.onrender.com/download/", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({url: url, quality: quality})
    });

    progressBar.value = 80;
    const blob = await res.blob();
    const filename = res.headers.get("Content-Disposition").split("filename=")[1];
    const a = document.createElement("a");
    a.href = window.URL.createObjectURL(blob);
    a.download = filename;
    a.click();
    progressBar.value = 100;
}
