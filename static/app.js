const form = document.querySelector("#validate-form");
const wordsDiv = document.querySelector("#words");

form.addEventListener("submit", async function (e) {
  console.log(e.target);
  e.preventDefault();
  const result = await axios.post("/submitted");

  console.log(result.data);
});
