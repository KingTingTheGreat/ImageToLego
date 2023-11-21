const slider = document.getElementById('length');
const sliderValue = document.getElementById('length-value');
sliderValue.textContent = slider.value;
slider.oninput = function() {
    sliderValue.textContent = this.value;
};

var angle = 0;
function rotateImage() {
    angle += 90;
    if (angle >= 360) {
        angle = 0;
    }
    document.getElementById('display-image').style.transform = 'rotate(' + angle + 'deg)';
}