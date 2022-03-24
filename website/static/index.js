function deleteNote(noteId){
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({ noteID: noteId})
    }).then((res)=> {
        window.location.href = "/"
    });

}