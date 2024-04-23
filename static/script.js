window.onload = function () {
  const opts = {
    angle: 0,
    lineWidth: 0.3,
    radiusScale: 1,
    pointer: {
      length: 0.6,
      strokeWidth: 0.039,
      color: "#000000", // corrected color value
    },
    limitMax: false,
    limitMin: false,
    colorStart: "#6F6EA0",
    colorStop: "#C0C0DB",
    strokeColor: "#EEEEEE",
    generateGradient: true,
    highDpiSupport: true,
  };

  let article_list = [];

  populateArticleList();

  document.getElementById("btn-submit").addEventListener("click", function () {
    displayResult("val-url", "/analyze");
    populateArticleList();
  });

  document
    .getElementById("article-list")
    .addEventListener("change", function () {
      displayResult("article-list");
    });

  function displayResult(inputId, fetchUrl) {
    const resultContainer = document.querySelector(".result-container");
    resultContainer.style.display = "block";
    resultContainer.classList.add("animate-result");

    const target = document.getElementById("sentiment-gauge");
    const gauge = createGauge(target, opts);
    const sentimentResult = document.getElementById("sentiment-result");
    const url = document.getElementById(inputId).value;

    if (fetchUrl) {
      fetchData(fetchUrl, { url }).then((data) =>
        updateUI(data, gauge, sentimentResult)
      );
    } else {
      const article = article_list.find(
        (article) => article.article_url === url
      );
      updateUI(article, gauge, sentimentResult);
      document.getElementById("val-url").value = url;
    }
  }

  function createGauge(target, options) {
    const gauge = new Gauge(target).setOptions(options);
    gauge.maxValue = 1000;
    gauge.setMinValue(0);
    gauge.animationSpeed = 32;
    gauge.set(0);
    return gauge;
  }

  function fetchData(url, body) {
    return fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    }).then((response) => response.json());
  }

  function updateUI(data, gauge, sentimentResult) {
    data.score = data.score < 0 ? data.score * -1 : data.score;
    gauge.set(data.score * 1000);
    const percentage = (data.score * 100).toFixed(2);
    sentimentResult.innerHTML = `${percentage}% is ${data.sentiment}`;
    document.getElementById("word-cloud").src = data.wordcloud;
}

  function populateArticleList() {
    fetch("/static/analysis.json")
      .then((response) => response.json())
      .then((data) => {
        article_list = data;
        const articleList = document.getElementById("article-list");
        const emptyOption = document.createElement("option");
        emptyOption.value = "";
        emptyOption.textContent = "Select an article...";
        articleList.appendChild(emptyOption);

        const articleUrls = new Set();

        for (const article of data) {
          if (!articleUrls.has(article.article_url)) {
            const option = document.createElement("option");
            option.value = article.article_url;
            option.textContent = article.title;
            articleList.appendChild(option);

            articleUrls.add(article.article_url);
          }
        }
      });
  }
};
