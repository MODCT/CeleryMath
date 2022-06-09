MathJax.Hub.Config({
    messageStyle: "none",
    tex2jax: {preview: "none"},
    "HTML-CSS": {
        preferredFont: "STIX",
        imageFont: null
    },
    CommonHTML: {
        scale: 180,
        minScaleAdjust: 100,
    },
    extensions: ["tex2jax.js","asciimath2jax.js"],
    showMathMenu: true,
    showMathMenuMSIE: false,
    TeX: { extensions: ["AMSmath.js","AMSsymbols.js","noUndefined.js"]},
    jax: ["input/TeX","input/AsciiMath","output/HTML-CSS"]
});