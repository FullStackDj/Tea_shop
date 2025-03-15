var colorPicker = document.getElementById("bgcolor");

function changeBodyColor() {
    var colorVal = colorPicker.value;
    document.body.style.background = colorVal;
    localStorage.setItem("bgColor", colorVal);
}

window.onload = function () {
    var savedColor = localStorage.getItem("bgColor");
    if (savedColor) {
        document.body.style.background = savedColor;
        colorPicker.value = savedColor;
    } else {
        document.body.style.background = "#00ffebff";
    }
};

colorPicker.addEventListener("input", changeBodyColor, false);
