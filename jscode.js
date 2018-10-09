let words = ['It', 'is', 'awfully', 'hard'];
let times = [1000, 2000, 4000, 6000];

function showAyah(words,times){
	let htmlElement = document.querySelector(".ayahWords");
	let wordCount = words.length;
	if(words.length !== times.length){
		throw('Oops!');
	}

	for(let i = 0; i < wordCount; i++) {
		let word = words[i];
		let time = times[i];
		setTimeout(function() {
			htmlElement.innerHTML += " " + word;
		}, time);
	}

}
showAyah(words,times);