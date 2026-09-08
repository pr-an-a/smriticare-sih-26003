function speakWelcome() {

```
const message =
    "Good morning. Welcome to SmritiCare. " +
    "You have one medicine reminder and four activities today.";

const speech = new SpeechSynthesisUtterance(message);

speech.rate = 0.85;
speech.pitch = 1;

window.speechSynthesis.speak(speech);
```

}
