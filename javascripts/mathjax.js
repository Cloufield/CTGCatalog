/* Load MathJax only when the page has pymdownx Arithmatex (.arithmatex) output. */
(function () {
  function articleRoot() {
    return document.querySelector("article.md-content__inner");
  }

  function hasMath(article) {
    return article && article.querySelector(".arithmatex");
  }

  function typeset() {
    if (window.MathJax && window.MathJax.typesetPromise) {
      return MathJax.typesetPromise();
    }
    return Promise.resolve();
  }

  function injectMathJax() {
    if (window.__catalogMathJaxInjected) {
      return;
    }
    window.__catalogMathJaxInjected = true;
    window.MathJax = {
      tex: {
        inlineMath: [["\\(", "\\)"]],
        displayMath: [["\\[", "\\]"]],
        processEscapes: true,
        processEnvironments: true,
      },
      options: {
        ignoreHtmlClass: ".*|",
        processHtmlClass: "arithmatex",
      },
    };
    var s = document.createElement("script");
    s.src =
      "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js";
    s.async = true;
    s.onload = function () {
      typeset();
    };
    document.head.appendChild(s);
  }

  document$.subscribe(function () {
    var article = articleRoot();
    if (!hasMath(article)) {
      return;
    }
    if (window.MathJax && window.MathJax.typesetPromise) {
      typeset();
    } else {
      injectMathJax();
    }
  });
})();
