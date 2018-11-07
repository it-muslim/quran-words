function leftPad (str, max) {
  str = str.toString();
  return str.length < max ? leftPad("0" + str, max) : str;
  }

function changeUrl() {
  let audio = new Audio();
  audio.src = 'C:/Users/Admin/Desktop/javascript/Quran/HQA files/audio/001001.mp3';
  let syraNumber = 1;
  let ayahNumber = 1; //0
  ayahNumber++;
  audio.play();
		
audio.onended = function() {
  let strSyraNumber = leftPad(syraNumber, 3);
  let strAyahNumber = leftPad(ayahNumber, 3);
  let str = strSyraNumber + strAyahNumber;
  audio.src = 'C:/Users/Admin/Desktop/javascript/Quran/HQA files/audio/001001.mp3'.replace('001001', str);
  audio.play();
  }

}