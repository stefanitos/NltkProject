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
    colorStart: "#157347",
    strokeColor: "#EEEEEE",
    highDpiSupport: true,
  };

  const resultContainer = document.querySelector(".result-container");
  const submitButton = document.getElementById("btn-submit");
  const articleList = document.getElementById("article-list");
  const sentimentResult = document.getElementById("sentiment-result");
  const urlInput = document.getElementById("val-url");
  const wordCloudImage = document.getElementById("word-cloud");

  let articleListData = [];
  const analysisUrl = "/analyze";
  const analysisDataUrl = "/static/analysis.json";

  populateArticleList();

  submitButton.addEventListener("click", async () => {
    await displayResult();
    populateArticleList();
  });

  articleList.addEventListener("change", displayArticleResult);

  async function displayResult() {
    const url = urlInput.value;
    const data = await fetchData(analysisUrl, { url });
    resultContainer.style.display = "block";
    resultContainer.classList.add("animate-result");

    const target = document.getElementById("sentiment-gauge");
    const gauge = createGauge(target, opts);
    updateUI(data, gauge, sentimentResult);
  }

  function displayArticleResult() {
    resultContainer.style.display = "block";
    resultContainer.classList.add("animate-result");

    const target = document.getElementById("sentiment-gauge");
    const gauge = createGauge(target, opts);
    const url = articleList.value;

    const article = articleListData.find(
      (article) => article.article_url === url
    );
    updateUI(article, gauge, sentimentResult);
    urlInput.value = url;
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
    const score = Math.abs(data.score);
    gauge.set(score * 1000);
    const percentage = (score * 100).toFixed(2);
    sentimentResult.textContent = `${percentage}% is ${data.sentiment}`;
    wordCloudImage.src = data.wordcloud;
  }

  async function populateArticleList() {
    const response = await fetch(analysisDataUrl);
    const data = await response.json();
    articleListData = data;

    articleList.innerHTML = `<option value="">Select an article...</option>`;
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
  }
};
