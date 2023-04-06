class BoggleGame {
  constructor() {
    this.form = document.querySelector("#validate-form");
    this.timesPlayedDiv = document.querySelector("#times-played");
    this.highestScoreDiv = document.querySelector("#highest-score");
    this.wordsDiv = document.querySelector("#words");
    this.remainingTime = document.querySelector("#remaining-time");
    this.wordStatus = document.querySelector("#word-status");
    this.input = document.querySelector("#word");
    //TODO: keep score in backend
    this.score = 0;
    this.startGame();
  }

  startGame() {
    //start timer
    this.timer();
    //add submit event listener to form
    this.form.addEventListener("submit", async (e) => {
      e.preventDefault();
      let inputVal = this.input.value;
      try {
        await axios.post("/submitted", { word: inputVal }).then((response) => {
          const word = { val: inputVal, status: response.data.result };
          this.displayStatus(word);
        });
      } catch (err) {
        console.log(err);
      }
      this.input.value = "";
    });
  }

  // show status of word on UI
  displayStatus(word) {
    this.wordStatus.style.visibility = "visible";
    let message = "";
    let messageColor = "";
    const wordLi = document.createElement("li");
    wordLi.innerHTML = `${word.val} +${word.val.length}`;

    if (word.status === "ok") {
      message = "Great word!!";
      messageColor = "goodWord";
      this.score += word.val.length;
      this.wordsDiv.append(wordLi);
    } else if (word.status === "not-word") {
      message = "This word is not a word :(!!";
      messageColor = "badWord";
    } else if (word.status === "already-guessed") {
      message = "This word is already guessed :(";
      messageColor = "badWord";
    } else {
      message = "This word is not on the board :(";
      messageColor = "badWord";
    }

    this.wordStatus.innerHTML = message;
    this.wordStatus.className = messageColor;
    setTimeout(() => {
      this.wordStatus.style.visibility = "hidden";
    }, 2000);
  }
  //timer function including timeout and end game function
  timer() {
    let sec = 60;
    let timeOut = setInterval(() => {
      if (sec > 0) {
        this.remainingTime.innerHTML = `Time left: ${sec} seconds`;
        sec--;
      } else {
        clearTimeout(timeOut);
        this.form.style.visibility = "hidden";
        this.remainingTime.innerHTML = `Time's up! Your score is: ${this.score}`;
        this.wordStatus.style.visibility = "hidden";
        this.endGame();
      }
    }, 1000);
  }
  // end game and send result as post request
  async endGame() {
    try {
      await axios.post("/end", { score: this.score }).then((response) => {
        const { times_played, highest_score } = response.data;
        this.timesPlayedDiv.innerHTML = `Times played: ${times_played}`;
        this.highestScoreDiv.innerHTML = `Highest score: ${highest_score}`;
      });
    } catch (err) {
      console.log(err);
    }
  }
}

const boggleGame = new BoggleGame();
