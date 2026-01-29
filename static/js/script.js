// difff《ﾃﾞｭﾌﾌ》JavaScript functions

function hideForm() {
    const form = document.getElementById('form');
    const top = document.getElementById('top');
    const news = document.getElementById('news');
    const hideBtn = document.getElementById('hide');
    
    if (form.style.display === 'none') {
        // Show all elements
        top.style.display = 'block';
        form.style.display = 'block';
        news.style.display = 'block';
        hideBtn.value = '結果のみ表示 (印刷用)';
    } else {
        // Hide elements for print mode
        top.style.display = 'none';
        form.style.display = 'none';
        news.style.display = 'none';
        hideBtn.value = '全体を表示';
    }
}

function setColor1() {
    document.getElementById('top').style.borderTop = '5px solid #00BBFF';
    const emList = document.getElementsByTagName('em');
    for (let i = 0; i < emList.length; i++) {
        emList[i].className = 'blue';
    }
}

function setColor2() {
    document.getElementById('top').style.borderTop = '5px solid #00bb00';
    const emList = document.getElementsByTagName('em');
    for (let i = 0; i < emList.length; i++) {
        emList[i].className = 'green';
    }
}

function setColor3() {
    document.getElementById('top').style.borderTop = '5px solid black';
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