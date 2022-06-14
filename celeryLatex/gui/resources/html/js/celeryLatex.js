function updateMath(s){
    document.getElementById("equation").innerText = s;
    MathJax.typeset();
}