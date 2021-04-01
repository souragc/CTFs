function checkCustomMusic(){
    const idCheckboxFile = document.getElementById("checkbox_file");
    const customMusicFileInput = document.getElementById("custom_file_input");
    const customSong = document.getElementById("custom_song");

    if(idCheckboxFile.checked){
        customMusicFileInput.style.display="inline-flex";
    }
    else{
        customMusicFileInput.style.display="none";
        customSong.value = "";
    }
}


function checkWebsiteLyrics(){
    const idCheckboxFile = document.getElementById("checkbox_lyrics");
    const customMusicFileInput = document.getElementById("custom_lyrics");
    const myLyrics = document.getElementById("lyrics");

    if(idCheckboxFile.checked){
        customMusicFileInput.style.display="inline-flex";
        myLyrics.disabled = true;
        myLyrics.value = ""
    }
    else{
        customMusicFileInput.style.display="none";
        myLyrics.disabled = false;

    }
}





async function requestCreateSong(){
    let infoWebLyricsArea = document.getElementById("web_lyrics_info");
    const lyrics = document.getElementById("lyrics");
    const customLyrics = document.getElementById("custom_lyrics_field");
    const customSongInput = document.getElementById("custom_song");  
    const idCheckboxLyrics = document.getElementById("checkbox_lyrics"); 
    const NameSong = document.getElementById("name_song"); 
    let webLyrics = false; 
    let valueLyrics = null;


    infoWebLyricsArea.style.display = "none";

    if(idCheckboxLyrics.checked)
    {
        valueLyrics = customLyrics.value;
        webLyrics = true;
    }
    else{
        valueLyrics = lyrics.value;
    }

    if(valueLyrics == null || valueLyrics == "")
        return;

    if(NameSong == null|| NameSong.value == null || NameSong.value == ""){
        return;
    }

        $("#loadMe").modal({
            backdrop: "static", //remove ability to close modal with click
            keyboard: false, //remove option to close with keyboard
            show: true //Display loader!
          });

    requestedData = await uploadFile(valueLyrics,webLyrics,customSongInput.files[0],NameSong.value);

    jsonInfo  = await requestedData.json()

    $("#loadMe").modal("hide");
    
    const textToPutAnswer = document.getElementById("web_lyrics_created");
    

    if ("web_lyrics" in jsonInfo){
        textToPutAnswer.value = atob(jsonInfo["source_used"])
        infoWebLyricsArea.style.display = "inline-flex";
    }

}


async function uploadFile(lyrics,webLyrics = false,song = undefined,nameSong){


    let info = new FormData()

    info.append("name_song",nameSong);

    if(webLyrics)
    {
        info.append("web_lyrics",true);
    }
    else{
        info.append("web_lyrics",false);
    }
    
    info.append("lyrics",lyrics);

    if(song != undefined){
        info.append("custom_song",song);  
    }

    let request = await fetch("/song",{
        method:"POST",
        body:info,
        
    });

    return request

}