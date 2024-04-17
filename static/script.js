window.onload = function () {
  const opts = {
    angle: 0,
    lineWidth: 0.3,
    radiusScale: 1,
    pointer: {
      length: 0.6,
      strokeWidth: 0.039,
      color: "#0000000",
    },
    limitMax: false,
    limitMin: false,
    colorStart: "#6F6EA0",
    colorStop: "#C0C0DB",
    strokeColor: "#EEEEEE",
    generateGradient: true,
    highDpiSupport: true,
  };

  var article_list = {};

  populateArticleList();

  document.getElementById("btn-submit").addEventListener("click", function () {
    const resultContainer = document.querySelector(".result-container");
    resultContainer.style.display = "block";
    resultContainer.classList.add("animate-result");

    const target = document.getElementById("sentiment-gauge");
    const gauge = new Gauge(target).setOptions(opts);
    gauge.maxValue = 1000;
    gauge.setMinValue(0);
    gauge.animationSpeed = 32;
    gauge.set(0);

    const sentimentResult = document.getElementById("sentiment-result");
    const url = document.getElementById("val-url").value;
    fetch("/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ url }),
    })
      .then((response) => response.json())
      .then((data) => {
        data.score = data.score < 0 ? data.score * -1 : data.score;

        gauge.set(data.score * 1000);
        const percentage = (data.score * 100).toFixed(2);
        sentimentResult.innerHTML = `${percentage}% is ${data.sentiment}`;

        document.getElementById(
          "word-cloud"
        ).src = `data:image/png;base64,${data.wordcloud}`;
      });
  });
  document
    .getElementById("article-list")
    .addEventListener("change", function () {
      // Get info from the selected article and populate the form using the global article_list
      // Example data: 
      const selectedArticleUrl = this.value;
      const article = article_list.find(
        (article) => article.article_url === selectedArticleUrl
      );

      document.getElementById("val-url").value = article.article_url;

      const resultContainer = document.querySelector(".result-container");
      resultContainer.style.display = "block";
      resultContainer.classList.add("animate-result");

      const target = document.getElementById("sentiment-gauge");
      const gauge = new Gauge(target).setOptions(opts);
      gauge.maxValue = 1000;
      gauge.setMinValue(0);
      gauge.animationSpeed = 32;
      gauge.set(0);
    });

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

        for (const article of data) {
          const option = document.createElement("option");
          option.value = article.article_url;
          option.textContent = article.title;
          articleList.appendChild(option);
        }
      });
  }
};
