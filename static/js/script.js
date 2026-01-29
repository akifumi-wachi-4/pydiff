// Modern Diff Tool - JavaScript functions

function setColor1() {
    const emList = document.getElementsByTagName('em');
    for (let i = 0; i < emList.length; i++) {
        emList[i].className = 'blue';
    }
}

function setColor2() {
    const emList = document.getElementsByTagName('em');
    for (let i = 0; i < emList.length; i++) {
        emList[i].className = 'green';
    }
}

function setColor3() {
    const emList = document.getElementsByTagName('em');
    for (let i = 0; i < emList.length; i++) {
        emList[i].className = 'black';
    }
}

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    // Set default color scheme
    setColor1();
});