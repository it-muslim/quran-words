var words = ['It', 'is', 'awfully', 'hard'];
var times = [1000, 2000, 4000, 6000];

function showAyah(words,times){

	var htmlElement = document.querySelector(".ayahWords");
	let wordCount = words.length;

	for(var currentIndex = 0; currentIndex < wordCount; currentIndex++) {
		
		(function(index) {
			let word = words[index];//это необходимо?
			let time = times[index];
			setTimeout(function() {
				htmlElement.innerHTML += " " + word;
			}, time);
		})(currentIndex);

	}
}

showAyah(words,times);