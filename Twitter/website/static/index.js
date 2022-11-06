function deleteNote(lista) {
  noteId = lista[1];
  fetch('/delete-note', {
    method: 'POST',
    body: JSON.stringify({ noteId: noteId}),
  }).then((_res) => {
    s = "/note/" + lista[0];
    window.location.href = s;
  });
}

function search(ele) {
  if(event.keyCode == 13) {
      document.getElementById("mbutton").click();
  }
}
